from rest_framework import viewsets
from ..models import Generate
from .serializers import GenerateModelSerializer

class GenerateViewSet(viewsets.ModelViewSet):
    queryset= Generate.objects.all()
    serializer_class= GenerateModelSerializer
    