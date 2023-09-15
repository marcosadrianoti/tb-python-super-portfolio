from rest_framework import routers
from django.urls import path, include

from .views import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'profiles/<int: id>', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls))
]
