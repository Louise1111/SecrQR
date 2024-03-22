from rest_framework import serializers
from account.models import User

User
class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class LoginSerializer(serializers.ModelSerializer):
    
    password= serializers.CharField(
        max_length=128, min_length=6 , write_only=True)
    class Meta:
        model=User
        fields=('username', 'password', 'token')
        
        read_only_fields=['token']