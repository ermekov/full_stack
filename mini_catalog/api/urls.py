from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, RegisterView, MeView, CommentViewSet, EquipmentListViewSet, ProfileListView, \
    CommentListCreateView, CommentDeleteView, LikeCreateView, RatingCreateView, AddItemToListView, ProfileUpdateView, \
    SubscribeTagView, SubscribeCategoryView, RecommendationsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('items', EquipmentViewSet)
router.register('lists', EquipmentListViewSet, basename='list')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path('', include(router.urls)),
    path('profile/', ProfileListView.as_view()),
    path('items/<int:equipment_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path("items/<int:item_id>/comments/", CommentListCreateView.as_view()),
    path("comments/<int:pk>/", CommentDeleteView.as_view()),
    path("items/<int:item_id>/like/", LikeCreateView.as_view()),
    path("items/<int:item_id>/rating/", RatingCreateView.as_view()),
    path("lists/<int:list_id>/add/", AddItemToListView.as_view()),
    path("users/profile/", ProfileUpdateView.as_view()),
    path("subscribe/tag/<int:id>/", SubscribeTagView.as_view(), name="subscribe-tag"),
    path("subscribe/category/<int:id>/", SubscribeCategoryView.as_view(), name="subscribe-category"),
    path("users/<int:user_id>/recommendations/", RecommendationsView.as_view(), name="recommendations"),
]