from rest_framework import viewsets
from ..models import Generate
from .serializers import GenerateModelSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Scan
from .serializers import ScanSerializer

class GenerateViewSet(viewsets.ModelViewSet):
    authentication_classes=[]
    queryset = Generate.objects.all()
    serializer_class = GenerateModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ScanViewSet(viewsets.ModelViewSet):
    authentication_classes=[]
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Perform the scan after saving the instance
        instance = serializer.instance
        instance.perform_scan()

        return Response(serializer.data, status=status.HTTP_201_CREATED)