from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  

class CustomUser(AbstractUser):
    username = None  
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('instructor', 'Instructor')],
        default='instructor',
    )
    department = models.ForeignKey(
        'academics.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
