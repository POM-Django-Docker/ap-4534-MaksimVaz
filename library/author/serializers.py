from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    # Serializer for Author
    class Meta:
        model = Author
        fields = '__all__'
