from rest_framework import serializers
from . import models

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'pet', 'author', 'body', 'created_at']

class PetSerializer(serializers.ModelSerializer):
    sex = serializers.StringRelatedField(many=True)  
    species = serializers.StringRelatedField(many=True)  
    color = serializers.StringRelatedField(many=True)  
    breed = serializers.StringRelatedField(many=True)  
    size = serializers.StringRelatedField(many=True)  
    status = serializers.StringRelatedField(many=False)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = models.Pet
        fields = ['id', 'name', 'species', 'breed', 'color', 'size', 'sex', 'status', 'image', 'created_by', 'adopted_by', 'created_at', 'rehoming_fee', 'details', 'reviews']



class SexSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Sex
        fields = '__all__'

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Species
        fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Breed
        fields = '__all__'

class SizeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Size
        fields = '__all__'

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'
        
class AdoptSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Adopt
        fields = ['full_name', 'email', 'phone_no', 'address', 'pet', 'adopt_date']

