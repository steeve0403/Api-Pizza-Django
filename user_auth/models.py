from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class CustomUser(AbstractUser):
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usage_quota = models.IntegerField(default=200)
    last_request_time = models.DateTimeField(null=True, blank=True)
    request_count = models.IntegerField(default=0)
    tier = models.CharField(max_length=50, default='free')

    groups = models.ManyToManyField(
    'auth.Group',
        related_name='users',
        blank=True,
        help_text='The group this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
    'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'