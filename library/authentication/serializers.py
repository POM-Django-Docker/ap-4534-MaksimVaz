from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    # Serializer for User
    class Meta:
        model = CustomUser
        exclude = ['password']
