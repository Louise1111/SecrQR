from rest_framework import routers
from .views import GenerateViewSet
from django.urls import path, include

router  =routers.DefaultRouter()
router.register(r'generate', GenerateViewSet )

urlpatterns = [
    path('', include (router.urls))
]