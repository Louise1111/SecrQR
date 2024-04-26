from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
User
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('id','username', 'email', 'password', 'first_name', 'last_name','image')

    def create(self, validated_data):
        try:
            return User.objects.create_user(**validated_data)
        except Exception as e:
         
            raise serializers.ValidationError("An error occurred while creating the user.")
        
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'token', 'image')
        read_only_fields = ['token']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = authenticate(username=username, password=password)

                if not user:
                    raise serializers.ValidationError("Unable to log in with provided credentials.")

                refresh = RefreshToken.for_user(user)
                attrs['token'] = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            except Exception as e:
                # Handle any exceptions that might occur during login
                # For example, you could log the error or raise a ValidationError
                raise serializers.ValidationError("An error occurred during login.")

        return attrs



class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    
    
class UserPictureSerializer(serializers.Serializer):
    image = serializers.ImageField()

