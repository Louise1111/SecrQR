from rest_framework import viewsets
from ..models import Generate
from .serializers import GenerateModelSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models import Scan
from .serializers import ScanSerializer
from ..models import HelpRequest
from rest_framework.parsers import MultiPartParser
from .serializers import HelpSerializer
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from ..utils import send_report_email
class ReportScanAPIView(APIView):
    def post(self, request, pk):
        try:
            scan = Scan.objects.get(pk=pk)
            link = scan.link
            send_report_email(link)
            scan.report = 'Yes'
            scan.save()
            return Response({'message': 'Link has been reported', 'link': link}, status=status.HTTP_200_OK)
        except Scan.DoesNotExist:
            return Response({'error': 'link not found'}, status=status.HTTP_404_NOT_FOUND)
@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            # Create a new Scan instance with the uploaded image
            scan = Scan(image=request.FILES['image'])
            scan.save()

            # Perform the scan operation on the uploaded image
            # Here, you can call the scan_url method of the Scan model
            url_status, malware_detected, malware_detected_tool = scan.scan_url()

            # Return the scan result along with the success message
            return JsonResponse({
                'message': 'Image uploaded successfully',
                'scan_result': {
                    'url_status': url_status,
                    'malware_detected': malware_detected,
                    'malware_detected_tool': malware_detected_tool
                }
            })
        except Exception as e:
            # Return error response in case of any exception
            return JsonResponse({'error': str(e)}, status=400)
    else:
        # Return error response for invalid request
        return JsonResponse({'error': 'Invalid request'}, status=400)
class GenerateViewSet(viewsets.ModelViewSet):

    queryset = Generate.objects.all()
    serializer_class = GenerateModelSerializer
    parser_classes = [MultiPartParser]
    def get_queryset(self):
        # Filter the queryset to include only scans associated with the authenticated user
        user = self.request.user
        if user.is_authenticated:
            return Generate.objects.filter(user=user)
        else:
            # Return an empty queryset if the user is not authenticated
            return Generate.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Create a mutable copy of the request data
            mutable_data = request.data.copy()

            # Associate the authenticated user with the Generate object's user field
            mutable_data['user'] = request.user.id
            
            serializer = self.get_serializer(data=mutable_data)
            if serializer.is_valid():
                # Perform additional operations if needed
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return error response if user is not authenticated
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
class ScanViewSet(viewsets.ModelViewSet):
    
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    parser_classes = [MultiPartParser]
    def get_queryset(self):
        # Filter the queryset to include only scans associated with the authenticated user
        user = self.request.user
        if user.is_authenticated:
            return Scan.objects.filter(user=user)
        else:
            # Return an empty queryset if the user is not authenticated
            return Scan.objects.none()

    def create(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Create a mutable copy of the request data
            mutable_data = request.data.copy()

            # Associate the authenticated user with the Scan object's user field
            mutable_data['user'] = request.user.id
            
            serializer = self.get_serializer(data=mutable_data)
            if serializer.is_valid():
                # Perform additional operations if needed
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return error response if user is not authenticated
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
class HelpListCreateViewSet(viewsets.ModelViewSet):
    authentication_classes=[]
    queryset = HelpRequest.objects.all()
    serializer_class = HelpSerializer

class HelpRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = HelpRequest.objects.all()
    serializer_class = HelpSerializer