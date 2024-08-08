from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, pagination, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import filters as drf_filters
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError,PermissionDenied
from user.models import UserProfile
from . import models, serializers
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, generics, mixins

class PetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

class PetFilter(filters.FilterSet):
    species = filters.CharFilter(field_name='species__slug', lookup_expr='iexact')
    sex = filters.CharFilter(field_name='sex__slug', lookup_expr='iexact')
    color = filters.CharFilter(field_name='color__slug', lookup_expr='iexact')
    breed = filters.CharFilter(field_name='breed__slug', lookup_expr='iexact')
    size = filters.CharFilter(field_name='size__slug', lookup_expr='iexact')
    status = filters.CharFilter(field_name='status__slug', lookup_expr='iexact')
    created_by = filters.NumberFilter(field_name='created_by__id', lookup_expr='exact')
    adopted_by = filters.NumberFilter(field_name='adopted_by__id', lookup_expr='exact')
    permission_classes = [AllowAny]
    

    class Meta:
        model = models.Pet
        fields = ['species', 'sex', 'color', 'breed', 'size', 'status', 'created_by', 'adopted_by']

class PetViewSet(viewsets.ModelViewSet):
    queryset = models.Pet.objects.all()
    serializer_class = serializers.PetSerializer
    pagination_class = PetPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]
    filterset_class = PetFilter
    search_fields = ['species__slug', 'sex__slug', 'color__slug', 'breed__slug', 'size__slug', 'status__slug','name']
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class PetDetailView(generics.RetrieveAPIView):
    queryset = models.Pet.objects.all()
    serializer_class = serializers.PetSerializer
    permission_classes = [AllowAny]
        
        
class ReviewCreateView(generics.CreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        pet_id = self.kwargs.get('pet_id')
        pet = models.Pet.objects.get(id=pet_id)
        user = self.request.user
        if pet.adopted_by != user:
            raise PermissionDenied("You are not authorized to review this pet.")
        
        serializer.save(pet=pet, author=user)

class SexViewSet(viewsets.ModelViewSet):
    queryset = models.Sex.objects.all()
    serializer_class = serializers.SexSerializer
    permission_classes = [AllowAny]

class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = models.Species.objects.all()
    serializer_class = serializers.SpeciesSerializer
    permission_classes = [AllowAny]

class ColorViewSet(viewsets.ModelViewSet):
    queryset = models.Color.objects.all()
    serializer_class = serializers.ColorSerializer
    permission_classes = [AllowAny]

class BreedViewSet(viewsets.ModelViewSet):
    queryset = models.Breed.objects.all()
    serializer_class = serializers.BreedSerializer
    permission_classes = [AllowAny]

class SizeViewSet(viewsets.ModelViewSet):
    queryset = models.Size.objects.all()
    serializer_class = serializers.SizeSerializer
    permission_classes = [AllowAny]

class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer
    permission_classes = [AllowAny]


class AdoptAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdoptSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            pet_id = request.data.get('pet')
            pet = models.Pet.objects.get(id=pet_id)

            if pet.adopted_by:
                return Response({'error': 'Pet already adopted'}, status=status.HTTP_400_BAD_REQUEST)

            available_status = models.Status.objects.filter(slug='available-to-adopt').first()
            adopted_status = models.Status.objects.filter(slug='adopted').first()

            if not available_status or not adopted_status:
                return Response({"error": "Status definitions are missing."}, status=status.HTTP_400_BAD_REQUEST)

            if pet.status != available_status:
                return Response({"error": "This pet is not available for adoption."}, status=status.HTTP_400_BAD_REQUEST)

            user_profile = UserProfile.objects.get(user=user)
            if user_profile.balance < pet.rehoming_fee:
                return Response({'error': 'Insufficient balance to adopt this pet'}, status=status.HTTP_400_BAD_REQUEST)

            pet.adopted_by = user
            pet.status = adopted_status
            pet.save()

            user_profile.balance -= pet.rehoming_fee
            user_profile.save()

            # Save the adoption record
            serializer.save(user=user)

            # Retrieve the creator's UserProfile
            creator_profile = UserProfile.objects.get(user=pet.created_by)
            creator_profile.balance += pet.rehoming_fee
            creator_profile.save()
            creator_user = pet.created_by 

            # Send emails
            self.send_emails(pet, user,creator_user, user_profile, creator_profile)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_emails(self, pet, adopter, creator_user,user_profile, creator_profile):
        creator_phone = creator_profile.mobile_no 
        adopter_phone=user_profile.mobile_no
        creator_balance = creator_profile.balance
        current_balance=user_profile.balance
        print(f"Creator Phone: {creator_phone}")
        print(f"Creator Balance: {creator_balance}")
        try:
            send_mail(
                'Pet Adopted',
                f'Your pet {pet.name} has been adopted.\nAdopter contact details:\nEmail: {adopter.email}\nPhone: {adopter_phone}\nYour current balance: ${creator_balance}',
                settings.EMAIL_HOST_USER,
                [creator_user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to pet creator: {e}")

        try:
            send_mail(
                'Adoption Confirmation',
                f'Congratulations! You have adopted {pet.name}.\nContact details of the pet creator:\nEmail: {creator_user.email}\nPhone: {creator_phone}\nYour current balance: ${current_balance}',
                settings.EMAIL_HOST_USER,
                [adopter.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to adopter: {e}")


