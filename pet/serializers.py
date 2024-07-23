from rest_framework import serializers
from . import models

class PetSerializer(serializers.ModelSerializer):
    sex = serializers.StringRelatedField(many=True)  
    species = serializers.StringRelatedField(many=True)  
    color = serializers.StringRelatedField(many=True)  
    breed = serializers.StringRelatedField(many=True)  
    size = serializers.StringRelatedField(many=True)  
    status = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Pet
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'pet', 'body', 'name', 'email', 'created_on']
    def validate(self, data):
        user = data['user']
        pet = data['pet']
        if not models.Adopt.objects.filter(user=user, pet=pet).exists():
            raise serializers.ValidationError("You can only review pets you have adopted.")
        return data
    
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
        fields = ''
