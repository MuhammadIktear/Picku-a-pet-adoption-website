from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, pagination, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters as drf_filters
from django_filters import rest_framework as filters
from user.models import UserAccount
from . import models, serializers

class PetPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

class PetFilter(filters.FilterSet):
    species = filters.CharFilter(field_name='species__slug', lookup_expr='iexact')
    sex = filters.CharFilter(field_name='sex__slug', lookup_expr='iexact')
    color = filters.CharFilter(field_name='color__slug', lookup_expr='iexact')
    breed = filters.CharFilter(field_name='breed__slug', lookup_expr='iexact')
    size = filters.CharFilter(field_name='size__slug', lookup_expr='iexact')
    status = filters.CharFilter(field_name='status__slug', lookup_expr='iexact')
    created_by = filters.NumberFilter(field_name='created_by__id', lookup_expr='iexact')
    adopted_by = filters.NumberFilter(field_name='adopted_by__id', lookup_expr='iexact')

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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        user = self.request.user
        pet_id = self.request.data.get('pet')

        if not models.Adopt.objects.filter(user=user, pet_id=pet_id).exists():
            raise serializers.ValidationError("You can only review pets you have adopted.")
        serializer.save(user=user)

class SexViewSet(viewsets.ModelViewSet):
    queryset = models.Sex.objects.all()
    serializer_class = serializers.SexSerializer

class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = models.Species.objects.all()
    serializer_class = serializers.SpeciesSerializer

class ColorViewSet(viewsets.ModelViewSet):
    queryset = models.Color.objects.all()
    serializer_class = serializers.ColorSerializer

class BreedViewSet(viewsets.ModelViewSet):
    queryset = models.Breed.objects.all()
    serializer_class = serializers.BreedSerializer

class SizeViewSet(viewsets.ModelViewSet):
    queryset = models.Size.objects.all()
    serializer_class = serializers.SizeSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer

class AdoptPetAPIView(generics.CreateAPIView):
    serializer_class = serializers.AdoptSerializer

    def post(self, request, pet_id):
        pet = get_object_or_404(models.Pet, id=pet_id)
        user = request.user
        bank_account = get_object_or_404(UserAccount, user=user)

        available_status = models.Status.objects.filter(slug='available-to-adopt').first()
        adopted_status = models.Status.objects.filter(slug='adopted').first()

        if not available_status or not adopted_status:
            return Response({"error": "Status definitions are missing."}, status=status.HTTP_400_BAD_REQUEST)

        if pet.status != available_status:
            return Response({"error": "This pet is not available for adoption."}, status=status.HTTP_400_BAD_REQUEST)

        if bank_account.balance < pet.rehoming_fee:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        bank_account.balance -= pet.rehoming_fee
        bank_account.save()

        # Update the pet's status
        pet.status = adopted_status
        pet.adopted_by = user
        pet.save()

        # Create adoption record
        adoption = models.Adopt.objects.create(user=user, pet=pet)
        serializer = serializers.AdoptSerializer(adoption)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
