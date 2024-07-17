from django.shortcuts import render
from rest_framework import viewsets,pagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .import models
from .import serializers
from user.models import UserAccount
# Create your views here.
class PetPagination(pagination.PageNumberPagination):
    page_size=1
    page_size_query_param=page_size
    max_page_size=100

class PetViewSet(viewsets.ModelViewSet):
    queryset=models.Pet.objects.all()
    serializer_class=serializers.PetSerializer
    pagination_class=PetPagination
    
class ReviewViewSet(viewsets.ModelViewSet):
    queryset=models.Review.objects.all()
    serializer_class=serializers.ReviewSerializer
    
class SexViewSet(viewsets.ModelViewSet):
    queryset=models.Sex.objects.all()
    serializer_class=serializers.SexSerializer
    
class SpeciesViewSet(viewsets.ModelViewSet):
    queryset=models.Species.objects.all()
    serializer_class=serializers.SpeciesSerializer
    
class ColorViewSet(viewsets.ModelViewSet):
    queryset=models.Color.objects.all()
    serializer_class=serializers.ColorSerializer
    
class BreedViewSet(viewsets.ModelViewSet):
    queryset=models.Breed.objects.all()
    serializer_class=serializers.BreedSerializer
    
class SizeViewSet(viewsets.ModelViewSet):
    queryset=models.Size.objects.all()
    serializer_class=serializers.SizeSerializer
    
class StatusViewSet(viewsets.ModelViewSet):
    queryset=models.Pet.objects.all()
    serializer_class=serializers.StatusSerializer
    
class AdoptPetAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AdoptSerializer

    def post(self, request, pet_id):
        pet = get_object_or_404(models.Pet, id=pet_id)
        user = request.user
        bank_account = get_object_or_404(UserAccount, user=user)  # Make sure this import is correct

        available_status = models.Status.objects.filter(slug='available-to-adopt').first()  # Adjusted to use slugs
        adopted_status = models.Status.objects.filter(slug='adopted').first()  # Adjusted to use slugs

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
        pet.save()

        # Create adoption record
        adoption = models.Adopt.objects.create(user=user, pet=pet)
        serializer = serializers.AdoptSerializer(adoption)

        return Response(serializer.data, status=status.HTTP_201_CREATED)