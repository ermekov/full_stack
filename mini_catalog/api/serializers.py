from rest_framework import serializers
from .models import Equipment
from django.contrib.auth.models import User
import os
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class EquipmentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Equipment
        fields ='__all__'
        read_only_fields = ('id', 'created_at', 'author')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Файл көлемі 5MB-тан аспауы керек.")

        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Рұқсат етілген форматтар: JPG, PNG, PDF.")

        return value