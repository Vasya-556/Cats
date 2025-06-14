from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet, TargetViewSet

router = DefaultRouter()
router.register(r'spycats', SpyCatViewSet)
router.register(r'missions', MissionViewSet)
router.register(r'targets', TargetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]