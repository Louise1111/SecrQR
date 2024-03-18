from account import views
from django.urls import path


urlpatterns = [
    
    path('register', views.RegisterApiView.as_view(), name="register")
]
