from django.contrib import admin
from .models import Generate, Scan  # Import the Scan model
from .models import HelpRequest
admin.site.register(Generate)
admin.site.register(HelpRequest)
