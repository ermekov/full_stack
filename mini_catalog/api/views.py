from django.db.models import Avg, Count
from django.shortcuts import render
from rest_framework import permissions, generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.db.models import Q

from .models import Equipment, Comment, EquipmentList, Profile, History, Follow, Tag, Like, Rating, Category
from .serializers import EquipmentSerializer, RegisterSerializer, UserSerializer, CommentSerializer, \
    EquipmentListSerializer, ProfileSerializer, LikeSerializer, RatingSerializer, HistorySerializer, FollowSerializer, \
    NotificationSerializer, FavoriteSerializer, CommentLikeSerializer, CommentRatingSerializer, \
    TagSubscriptionSerializer, CategorySubscriptionSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter
    ]

    search_fields = ['name', 'description', 'tags']
    filterset_fields = ['available_from', 'categories__name', 'tags__name']
    ordering_fields = ['created_at', 'name']


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user

        if user.is_authenticated:
            user_tags = Tag.objects.filter(items__in=[f.item for f in user.favorites.all()])
            favorite_ids = [f.item.id for f in user.favorites.all()]

            queryset = queryset.filter(
                Q(tags__in=user_tags) | Q(id__in=favorite_ids)
            )

        return queryset.distinct()

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Вы не можете редактировать чужую запись")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужую запись")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        item_id = self.kwargs.get('item_id')
        return Comment.objects.filter(item_id=item_id).order_by('-created_at')

    def perform_create(self, serializer):
        item_id = self.kwargs.get('item_id')
        serializer.save(author=self.request.user, item_id=item_id)

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Comment.objects.filter(item_id=item_id)

    def perform_create(self, serializer):
        item_id = self.kwargs['item_id']
        serializer.save(author=self.request.user, item_id=item_id)

class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class EquipmentListViewSet(viewsets.ModelViewSet):
    serializer_class = EquipmentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EquipmentList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileListView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddItemToListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, list_id):
        lst = EquipmentList.objects.get(id=list_id, user=request.user)
        item_id = request.data.get("item_id")
        item = Equipment.objects.get(id=item_id)
        lst.items.add(item)
        return Response({"status": "added"})



class UserHistoryView(generics.ListAPIView):
    serializer_class = HistorySerializer

    def get_queryset(self):
        return History.objects.filter(user_id=self.kwargs['user_id'])

class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_to_follow = User.objects.get(id=self.kwargs['id'])
        serializer.save(follower=self.request.user, following=user_to_follow)

# Список подписчиков
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['id'])
        return Follow.objects.filter(following=user)

# Список уведомлений
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()

class AddFavoriteView(generics.CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        item = Equipment.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, item=item)

class RecommendationsView(generics.ListAPIView):
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_tags = Tag.objects.filter(items__in=[f.item for f in user.favorites.all()])
        favorite_ids = [f.item.id for f in user.favorites.all()]

        recommended = Equipment.objects.filter(
            Q(tags__in=user_tags) | Q(id__in=favorite_ids)
        ).annotate(
            like_count=Count('likes'),
            avg_rating=Avg('ratings__value')
        ).order_by('-avg_rating')

        return recommended.distinct()
class CommentLikeView(generics.CreateAPIView):
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = Comment.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, comment=comment)

class CommentRatingView(generics.CreateAPIView):
    serializer_class = CommentRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        comment = Comment.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, comment=comment)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Comment.objects.filter(item_id=item_id).annotate(
            like_count=Count('likes'),
            avg_rating=Avg('ratings__value')
        )

class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = User.objects.get(id=id)
        data = {
            "objects_count": Equipment.objects.filter(author=user).count(),
            "comments_count": Comment.objects.filter(author=user).count(),
            "likes_count": Like.objects.filter(user=user).count(),
            "ratings_count": Rating.objects.filter(user=user).count(),
            "follows_count": Follow.objects.filter(follower=user).count(),
        }
        return Response(data)

class GlobalStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "total_objects": Equipment.objects.count(),
            "total_comments": Comment.objects.count(),
            "total_likes": Like.objects.count(),
            "total_ratings": Rating.objects.count(),
            "total_users": User.objects.count(),
            "categories_count": Category.objects.count()
        }
        return Response(data)

class SubscribeTagView(generics.CreateAPIView):
    serializer_class = TagSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        tag = Tag.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, tag=tag)

class SubscribeCategoryView(generics.CreateAPIView):
    serializer_class = CategorySubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        category = Category.objects.get(id=self.kwargs['id'])
        serializer.save(user=self.request.user, category=category)

