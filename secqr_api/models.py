from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import datetime
from pyzbar.pyzbar import decode as pyzbar_decode
import re
import requests
from django.conf import settings
import hashlib
import requests
from django.contrib.auth.models import User

api_key = "a759ba9c8a836e1bde3da7da0567d32842fa186ffaf1999f5cdbeff92e519fa8"
url = 'https://www.virustotal.com/vtapi/v2/url/report'
User = settings.AUTH_USER_MODEL

class Scan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    app_prefix = models.CharField(max_length=50, default='SecQR', editable=False)
    link = models.CharField(max_length=200, blank=True, null=True)
    link_status = models.CharField(max_length=20, default='NONE')
    scanned_at = models.DateTimeField(auto_now_add=True)
    verify_qr_legitimacy = models.CharField(max_length=30, default='NONE')
    malware_detected = models.TextField(default='NONE')
    malware_detected_tool = models.TextField(default='NONE')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='scan_images/', blank=True, null=True)

    def __str__(self):
        if self.link:
            return self.link
        else:
            return f"Scan object {self.pk}"

    def save(self, *args, **kwargs):
        if not self.image and not self.link:
            raise ValidationError("Either image or link field is required.")

        try:
            if self.image:
                img = Image.open(self.image)
                decoded_objects = pyzbar_decode(img)
                url_pattern = r'(https?://\S+)'

                for obj in decoded_objects:
                    data = obj.data.decode('utf-8')
                    urls_found = re.findall(url_pattern, data)
                    if urls_found:
                        url_validator = URLValidator()
                        try:
                            url_validator(urls_found[0])
                            self.link = urls_found[0]
                            break
                        except ValidationError:
                            continue

                if not self.link:
                    raise ValidationError("No valid URL found in the QR code data.")

            url_status, malware_detected, malware_detected_tool = self.scan_url()
            self.malware_detected = malware_detected
            self.malware_detected_tool = malware_detected_tool
            self.link_status = url_status

            verify_qr = self.verify_qr_code()
            self.verify_qr_legitimacy = verify_qr

            super().save(*args, **kwargs)
        except Exception as e:
            # Handle any unexpected errors
            raise ValidationError(f"Error saving scan: {e}")

    def scan_url(self):
        try:
            url = 'https://www.virustotal.com/vtapi/v2/url/report'
            params = {'apikey': api_key, 'resource': self.link}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                response_json = response.json()
                if 'positives' in response_json:
                    positives = response_json['positives']
                    if positives <= 4:
                        malware_detected, detected_malware_tool = self.extract_detected_malware(response_json)
                        return "SAFE", malware_detected, detected_malware_tool
                    elif 5 <= positives <= 9:
                        malware_detected, detected_malware_tool = self.extract_detected_malware(response_json)
                        return "NOT THAT SAFE", malware_detected, detected_malware_tool
                    elif positives >= 10:
                        malware_detected, detected_malware_tool = self.extract_detected_malware(response_json)
                        return "MALICIOUS", malware_detected, detected_malware_tool
                else:
                    return "NOT FOUND", [], []
            elif response.status_code == 403:
                return "INACTIVE/MALICIOUS", [], []
            else:
                return "Error", [], []
        except Exception as e:
            # Handle any unexpected errors
            raise ValidationError(f"Error scanning URL: {e}")

    def extract_detected_malware(self, response_json):
        malware_detected = set()
        detected_malware_tool = []

        for tool, scan in response_json.get('scans', {}).items():
            if scan.get('detected'):
                result = scan.get('result')
                cleaned_result = result.replace("site", "")
                malware_detected.add(cleaned_result)
                detected_malware_tool.append(tool)

        return list(malware_detected), detected_malware_tool

    def verify_qr_code(self):
        try:
            if '###' in self.link:
                link, link_hash = self.link.split('###')
                combined_data = f"{self.app_prefix}{link}"
                recalculated_hash = hashlib.sha256(combined_data.encode()).hexdigest()

                if recalculated_hash == link_hash:
                    return "Generated by SecQR APP"
                else:
                    return "Generated by Third Party"
            else:
                return "Generated by Third Party APP"
        except Exception as e:
            # Handle any unexpected errors
            raise ValidationError(f"Error verifying QR code: {e}") 
###################################################################################
###################################################################################
###################################################################################
class Generate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    qr_code = models.ImageField(blank=True, upload_to='qrcodes/')
    date = models.DateField(auto_now_add=True)
    _app_prefix_hidden = models.CharField(max_length=50, default='SecQR', editable=False)
    app_prefix = models.CharField(max_length=50, default='SecQR', editable=False)  # New field to store app prefix
    url_status = models.CharField(max_length=20,default='NONE')
    generation_status = models.CharField(max_length=20,default='NONE')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.link)

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the instance is being created, set the app_prefix
            self.app_prefix = self._app_prefix_hidden
        # Validate the link before generating QR code
        validate_url = URLValidator()
        try:
            validate_url(self.link)
        except ValidationError:
            self.url_status = "INVALID URL"
            self.generation_status="FAILED"
            super().save(*args, **kwargs) 
            return



        # Scan the URL to check for malicious content
        url_status = self.scan_url()

        if url_status == "SAFE":
            self.url_status="SAFE"
            # If the URL is not malicious, generate QR code
            self.generate_qr_code()
            
            
        elif url_status == "NOT THAT SAFE":
            self.url_status="NOT THAT SAFE"
            self.generation_status="FAILED"
            super().save(*args, **kwargs) 
            return
        elif url_status == "MALICIOUS":
            self.url_status="MALICIOUS"
            self.generation_status="FAILED"
            super().save(*args, **kwargs) 
            return
        else:
            self.url_status=url_status
            self.generation_status="FAILED"
            super().save(*args, **kwargs) 
            return
        
        self.url_status = url_status
        self.generation_status="SUCCESS"
        super().save(*args, **kwargs)

        
    def scan_url(self):
        url = 'https://www.virustotal.com/vtapi/v2/url/report' # VirusTotal API endpoint
        params = {'apikey': api_key, 'resource': self.link}

        # Perform the VirusTotal API request to scan the URL
        response = requests.get(url, params=params)
        # Check if the request was successful
        if response.status_code == 200:
            response_json = response.json()
            if 'positives' in response_json:
                positives = response_json['positives']
                if positives <= 4:
                    return "SAFE"
                elif 5 <= positives <= 9:
                    return "NOT THAT SAFE"
                elif positives >= 10:
                    return "MALICIOUS"
            else:
                return "NOT FOUND"
        elif response.status_code == 403:
            return "INACTIVE/MALICIOUS"
        else:
            return "Error"
        
    def generate_qr_code(self):
        if not self.qr_code:
            # Generate QR code with padding set to 0
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10, # Adjust box size as needed
                border=0,     # Set border to 0
            )

            # Concatenate the app_prefix with the link
            combined_data = f"{self.app_prefix}{self.link}"

            # Calculate the SHA-256 hash of the combined data
            link_hash = hashlib.sha256(combined_data.encode()).hexdigest()

            # Include the hashed link in the QR code data
            qr_data = f"{self.link}###{link_hash}"
            qr.add_data(qr_data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Resize the QR code image
            qr_img = qr_img.resize((370, 370)) # Adjust size if needed

            # Open the logo image
            logo_path = 'media/images/logo.png' # Adjust path to your logo image
            logo_img = Image.open(logo_path)

            # Calculate the size ratio between the QR code and logo
            qr_width, qr_height = qr_img.size
            logo_width, logo_height = logo_img.size
            size_ratio = min(logo_width / qr_width, logo_height / qr_height)

            # Resize the logo image while preserving its original quality
            new_logo_width = int(qr_width * size_ratio)
            new_logo_height = int(qr_height * size_ratio)
            logo_img = logo_img.resize((new_logo_width, new_logo_height))

            # Create a transparent image the same size as the logo image
            transparent_img = Image.new('RGBA', logo_img.size, (255, 255, 255, 0))

            # Calculate the position to paste the QR code onto the logo image
            position = ((new_logo_width - qr_width) // 2, (new_logo_height - qr_height) // 4) # Center position

            # Paste the QR code onto the transparent image
            transparent_img.paste(qr_img, position)

            # Composite the transparent image onto the logo image
            logo_img = Image.alpha_composite(logo_img.convert('RGBA'), transparent_img)

            # Save the QR code image
            buffer = BytesIO()
            logo_img.save(buffer, format='PNG')
            filename = f"secQRResult_{self.date}.png"

            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)
            
###################################################################################
###################################################################################
###################################################################################
class HelpRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title