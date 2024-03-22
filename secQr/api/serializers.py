from rest_framework import serializers
from ..models import Generate
from ..models import Scan
class GenerateModelSerializer(serializers.ModelSerializer):
    app_prefix = serializers.CharField(max_length=50, required=False)

    class Meta:
        model = Generate
        fields = ['id', 'description', 'link', 'qr_code', 'date', 'app_prefix']

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['id', 'url', 'result', 'scanned_at']

    def validate(self, data):
        url = data['url']
        expected_app_prefix = "secQr"  # Adjust as needed
        scan = Scan(url=url)
        result = scan.verify_qr_code(expected_app_prefix)
        data['result'] = result
        return data