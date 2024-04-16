from django.contrib import admin
from .models import User
from secqr_api.models import Scan  # Import the Scan model
# Register your models here.
admin.site.register(User)
admin.site.register(Scan)
