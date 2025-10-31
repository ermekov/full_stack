from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, RegisterView, MeView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('items', EquipmentViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path('', include(router.urls)),
]