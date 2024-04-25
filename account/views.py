from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from account.serializers import RegisterSerializer, LoginSerializer
from rest_framework import response, status , permissions
from django.contrib.auth import authenticate
from django.http import JsonResponse
# Create your views here.



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
    