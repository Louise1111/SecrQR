from rest_framework import serializers
from ..models import Generate
from ..models import Scan
from ..models import HelpRequest

class GenerateModelSerializer(serializers.ModelSerializer):
    app_prefix = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = Generate
        fields = ['id','user', 'description', 'link', 'qr_code', 'date', 'app_prefix', 'url_status', "generation_status",'created_at']

class ScanSerializer(serializers.ModelSerializer):
    app_prefix = serializers.CharField(max_length=50, required=False)
    class Meta:
        model = Scan
        fields = ['id','user', 'app_prefix', 'link', 'link_status', 'scanned_at', 'verify_qr_legitimacy', 'malware_detected', 'malware_detected_tool', 'created_at', 'image','report']
        
class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = ['id', 'title', 'description', 'created_at']