from rest_framework import serializers
from account.models import User

class RegisterSerializer(serializers.ModelSerializer):
    
    password= serializers.CharField(
        max_length=128, min_length=6 , write_only=True)
    class Meta:
        model=User
        fields=('username','email', 'password','gender', 'email', 'first_name', 'last_name',)
        
        def create(self, validated_data):
            return User.objects.create_user(**validated_data)
         