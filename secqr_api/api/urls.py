from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'generate', views.GenerateViewSet)
router.register(r'scan', views.ScanViewSet)
router.register(r'help', views.HelpListCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),

]