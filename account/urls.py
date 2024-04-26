from account import views
from django.urls import path
from .views import LogoutAPIView
from .views import forgot_password, verify_otp, reset_password
from .views import UserPictureUploadView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('register/', views.RegisterApiView.as_view(), name="register"),
    path('login/', views.LoginApiView.as_view(), name="login"),
    path('user/', views.AuthUserAPIView.as_view(), name="user"),
    path('logout/', LogoutAPIView.as_view(), name='logout'),



    path('forgot-password/', forgot_password, name='forgot_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('reset-password/', reset_password, name='reset_password'),

    path('upload-picture/', UserPictureUploadView.as_view(), name='upload_picture'),


]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

