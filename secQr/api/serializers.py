from rest_framework import serializers
from ..models import Generate

class GenerateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model= Generate
        fields = ('id', 'description', 'link','qr_code', 'date')