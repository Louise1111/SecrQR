from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from account.serializers import RegisterSerializer, LoginSerializer
from rest_framework import response, status , permissions
from django.contrib.auth import authenticate
from django.http import JsonResponse 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from .serializers import LogoutSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect


from .serializers import UserPictureSerializer

class UserPictureUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserPictureSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data.get('image')
            user = request.user  
            user.upload_picture(image)
            return Response({'message': 'Profile picture uploaded successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AuthUserAPIView(GenericAPIView):
    
    permission_classes=(permissions.IsAuthenticated,)
    
    def get(self, request):
        user=request.user
        serializer= RegisterSerializer(user)
        return response.Response({'user': serializer.data})
        

class RegisterApiView(GenericAPIView):
    authentication_classes = []  # for authentication to avoid using the custom authentication
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginApiView(GenericAPIView):
    authentication_classes=[]
    
    serializer_class=LoginSerializer
    
    def post(self, request):
        username=request.data.get('username',None)
        password=request.data.get('password',None)
        
        user=authenticate(username=username, password=password)
        
        if user:
            serializer=self.serializer_class(user)
            
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid Credentials, Please Try again"}, status=status.HTTP_401_UNAUTHORIZED)






class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def post(self, request):
        # Perform logout
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    
# views.py

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from .utils import generate_otp, send_otp_email

@api_view(['POST'])
@authentication_classes([])  # Exclude this endpoint from token authentication
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'No user found with this email address'}, status=status.HTTP_404_NOT_FOUND)

    # Generate OTP and send it via email
    otp = generate_otp()
    send_otp_email(email, otp)

    # Store the OTP in session for verification
    request.session['forgot_password_email'] = email
    request.session['forgot_password_otp'] = otp

    return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])  # Exclude this endpoint from token authentication
def verify_otp(request):
    otp_entered = request.data.get('otp')
    if not otp_entered:
        return Response({'error': 'OTP is required'}, status=status.HTTP_400_BAD_REQUEST)

    otp_in_session = request.session.get('forgot_password_otp')
    if not otp_in_session:
        return Response({'error': 'OTP session expired or not found'}, status=status.HTTP_400_BAD_REQUEST)

    if otp_entered != otp_in_session:
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'OTP verification successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])  # Exclude this endpoint from token authentication
def reset_password(request):
    new_password = request.data.get('new_password')
    if not new_password:
        return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

    email = request.session.get('forgot_password_email')
    if not email:
        return Response({'error': 'Email not found in session'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found with this email'}, status=status.HTTP_404_NOT_FOUND)

    # Reset password
    user.set_password(new_password)
    user.save()

    # Clear session
    del request.session['forgot_password_email']
    del request.session['forgot_password_otp']

    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)

