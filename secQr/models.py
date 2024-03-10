from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import datetime

class Generate(models.Model):
    description = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    qr_code = models.ImageField(blank=True, upload_to='qrcodes/')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.link)

    def save(self, *args, **kwargs):
        # Validate the link before generating QR code
        validate_url = URLValidator()
        try:
            validate_url(self.link)
        except ValidationError:
            raise ValidationError("Invalid URL")

        if not self.qr_code:
            # Generate QR code with padding set to 0
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,  # Adjust box size as needed
                border=0,     # Set border to 0
            )
            qr.add_data(f"{self.description}: {self.link}")
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Resize the QR code image
            qr_img = qr_img.resize((370, 370))  # Adjust size if needed

            # Open the logo image
            logo_path = 'media/images/logo.png'  # Adjust path to your logo image
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
            position = ((new_logo_width - qr_width) // 2, (new_logo_height - qr_height) // 4)  # Center position

            # Paste the QR code onto the transparent image
            transparent_img.paste(qr_img, position)

            # Composite the transparent image onto the logo image
            logo_img = Image.alpha_composite(logo_img.convert('RGBA'), transparent_img)

            # Save the combined image as PNG
            buffer = BytesIO()
            logo_img.save(buffer, format='PNG')
            filename = f"secQRResult_{self.date}.png"
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)
