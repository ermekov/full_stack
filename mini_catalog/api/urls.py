from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, RegisterView, MeView, CommentViewSet, EquipmentListViewSet, ProfileListView
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
]