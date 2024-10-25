from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=50)
    profilePicUrl = models.URLField(null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='group_user', 
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='permissions_user', 
        blank=True,
    )

    def __str__(self):
        return self.firstName