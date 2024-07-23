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
        fields = ['pet', 'body']  # Include only fields to be provided by the client

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None

        if user is None:
            raise serializers.ValidationError("User must be authenticated to create a review.")

        # Retrieve pet instance from validated_data
        pet = validated_data.get('pet')

        # Retrieve or set user name and email
        user_name = user.get_full_name() or 'Anonymous'
        user_email = user.email or 'no-reply@example.com'

        # Create review with automatic fields
        review = models.Review.objects.create(
            user=user,
            name=user_name,
            email=user_email,
            **validated_data
        )
        return review

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
