from rest_framework import serializers
from . import models
from rest_framework.permissions import IsAuthenticated,AllowAny

class PetSerializer(serializers.ModelSerializer):
    sex = serializers.StringRelatedField(many=True)  
    species = serializers.StringRelatedField(many=True)  
    color = serializers.StringRelatedField(many=True)  
    breed = serializers.StringRelatedField(many=True)  
    size = serializers.StringRelatedField(many=True)  
    status = serializers.StringRelatedField(many=False)
    permission_classes = [AllowAny]

    class Meta:
        model = models.Pet
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = models.Review
        fields = ['id', 'pet', 'body', 'name', 'email', 'created_on']


class SexSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]    
    class Meta:
        model = models.Sex
        fields = '__all__'

class SpeciesSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = models.Species
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = models.Color
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = models.Breed
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = models.Size
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    permission_classes = [AllowAny]
    class Meta:
        model = models.Status
        fields = '__all__'
        
class AdoptSerializer(serializers.ModelSerializer):
    permission_classes = [IsAuthenticated]
    class Meta:
        model = models.Adopt
        fields = ['full_name', 'email', 'phone_no', 'address', 'pet', 'adopt_date']

