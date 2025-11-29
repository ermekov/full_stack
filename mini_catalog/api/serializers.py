from rest_framework import serializers
from .models import Equipment, Comment, EquipmentList, Profile, Like, Rating, History, Follow, Notification, Category, Tag, Favorite, CommentLike, CommentRating, TagSubscription, CategorySubscription
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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class EquipmentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    rating = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'
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

    def get_avg_rating(self, obj):
        ratings = obj.ratings.all().values_list('value', flat=True)
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

    def get_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return round(sum(r.value for r in ratings) / ratings.count(), 2)
        return 0


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
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

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'user', 'action', 'created_at']

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'item', 'is_public', 'created_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagSubscription
        fields = '__all__'

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'

class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentRating
        fields = '__all__'

class TagSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagSubscription
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class CategorySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySubscription
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
