from rest_framework import serializers
from .models import Equipment, Comment, EquipmentList, Profile
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
    like_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

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

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_average_rating(self, obj):
        ratings = obj.likes.filter(rating__gt=0).values_list('rating', flat=True)
        return round(sum(ratings) / len(ratings), 2) if ratings else 0

    def validate_file(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("Файл көлемі 5MB-тан аспауы керек.")

        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Рұқсат етілген форматтар: JPG, PNG, PDF.")

        return value

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'equipment', 'author', 'text', 'created_at')
        read_only_fields = ('author', 'created_at')

class EquipmentListSerializer(serializers.ModelSerializer):
    items = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = EquipmentList
        fields = ('id', 'name', 'items', 'created_at')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio']

