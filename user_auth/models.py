from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class ServicePlan(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_requests_per_day = models.IntegerField(default=100)
    max_api_keys = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True, blank=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    api_key_expires_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=365))
    usage_quota = models.IntegerField(default=200)
    last_request_time = models.DateTimeField(null=True, blank=True)
    request_count = models.IntegerField(default=0)
    tier = models.CharField(
        max_length=50,
        choices=[
            ('free', 'Free'),
            ('premium', 'Premium'),
            ('enterprise', 'Enterprise')
        ],
        default='free'
    )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_device = models.CharField(max_length=255, null=True, blank=True)

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
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['api_key']),
        ]


class RefreshToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.token


class UserActivityLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('api_key_renewal', 'API Key Renewal'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"


class UserSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Session for {self.user.username} - {self.session_token}"

    def is_expired(self):
        return timezone.now() > self.expires_at


class APIKey(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.key} for {self.user.username}"


class UserNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


class ArchivedUser(models.Model):
    original_user_id = models.IntegerField()
    archived_data = models.JSONField()
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Archived data for user {self.original_user_id}"
