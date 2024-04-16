from rest_framework import viewsets
from ..models import Generate
from .serializers import GenerateModelSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Scan
from .serializers import ScanSerializer
from ..models import HelpRequest
from .serializers import HelpSerializer
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

    # Optionally override create method to handle custom behavior when creating a new Scan object
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Perform additional operations if needed
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class HelpListCreateViewSet(viewsets.ModelViewSet):
    authentication_classes=[]
    queryset = HelpRequest.objects.all()
    serializer_class = HelpSerializer

class HelpRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = HelpRequest.objects.all()
    serializer_class = HelpSerializer