
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, name, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, name=name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, name, role="admin", password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, phone_number, name, role, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    ROLE_CHOICES = [
        ("victim", "Victim"),
        ("volunteer", "Volunteer"),
        ("donor", "Donor"),
        ("admin", "Admin"),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('bn', 'Bangla'),
    ]


    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # language_preference = models.CharField(max_length=20, null=True, blank=True)
    language_preference = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en')
    verification_status = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "name", "role"]

    def __str__(self):
        return f"{self.name} ({self.role})"



class AidRequest(models.Model):
    URGENCY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    CATEGORY_CHOICES = [
        ("food", "Food"),
        ("shelter", "Shelter"),
        ("medical", "Medical"),
        ("clothes", "Clothes"),
        ("other", "Other"),
    ]

    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    urgency = models.CharField(
        max_length=20,
        choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')],
        default='Medium'
    )
    voice_message = models.FileField(upload_to="aid/voice/", null=True, blank=True)
    photo = models.ImageField(upload_to="aid/photos/", null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    assigned_volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'volunteer'},
        related_name='assigned_requests'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Request {self.request_id} - {self.user.name}"



class Donation(models.Model):
    DONATION_TYPE_CHOICES = [
        ('money', 'Money'),
        ('items', 'Items'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('visa', 'Visa'),
    ]

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donation_type = models.CharField(
        max_length=20,
        choices=DONATION_TYPE_CHOICES,
        default='money'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    items_title = models.CharField(max_length=255, blank=True, null=True)
    items_description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    pickup_date = models.DateField(blank=True, null=True)
    pickup_time = models.TimeField(blank=True, null=True)
    pickup_address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.donor.email} - {self.donation_type}"


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=50)
    target_id = models.IntegerField()
    rating = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback {self.feedback_id} by {self.user.name}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('Aid Request', 'Aid Request'),
        ('Donation', 'Donation'),
        ('Volunteer Assignment', 'Volunteer Assignment'),
        ('System', 'System'),
    ]
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]
    ACTION_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    action_status = models.CharField(max_length=10, choices=ACTION_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.user.username} ({self.status})"


class VolunteerAssignment(models.Model):
    STATUS_CHOICES = [
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    assignment_id = models.AutoField(primary_key=True)
    volunteer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'volunteer'},
        related_name="volunteer_assignments"
    )
    request = models.ForeignKey(
        AidRequest,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_by_admin"
    )
    assignment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="assigned")

    def __str__(self):
        return f"Assignment {self.assignment_id} - {self.volunteer.name}"

    class Meta:
        unique_together = ('volunteer', 'request')


class LiveUpdate(models.Model):
    CATEGORY_CHOICES = [
        ("Relief", "Relief"),
        ("Medical", "Medical"),
        ("Shelter", "Shelter"),
        ("Other", "Other"),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    volunteer_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="updates/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.location})"
