from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import upload_image
from .views import ReportScanAPIView
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register(r'generate', views.GenerateViewSet)
router.register(r'scan', views.ScanViewSet)
router.register(r'help', views.HelpListCreateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', upload_image, name='upload_image'),

    path('report/<int:pk>/', ReportScanAPIView.as_view(), name='report_scan'),

]