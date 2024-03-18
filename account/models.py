from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        
        if not other_fields.get('is_superuser'):
            raise ValueError("is_superuser must be True")
        if not other_fields.get('is_staff'):
            raise ValueError("is_active must be true")
        
        return self.create_user(username, email, password, **other_fields)
    
    def create_user(self, username, email, password, **other_fields):
        if not username:
            raise ValueError("username not provided")
        user = self.model(username=username, email=email, **other_fields)
        
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser, TrackingModel):
    gender_choices = (
        (1, 'male'),
        (2, 'Female')
    )
    username = models.CharField(max_length=20, blank=False, unique=True)
    email = models.EmailField(max_length=122,  blank=False, unique=True)
    first_name = models.CharField(max_length=125 , blank=False,)
    last_name = models.CharField(max_length=32,  blank=False,)
    password = models.CharField(max_length=32)  # Note: Storing password directly in the database is not recommended.
    gender = models.SmallIntegerField(choices=gender_choices, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['gender', 'email', 'first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True  # This method needs to be implemented correctly to check permissions.
