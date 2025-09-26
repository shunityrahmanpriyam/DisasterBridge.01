from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


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

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    language_preference = models.CharField(max_length=20, null=True, blank=True)
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
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    urgency_level = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="pending")
    request_date = models.DateTimeField(auto_now_add=True)
    voice_message_path = models.CharField(max_length=255, null=True, blank=True)
    priority_score = models.IntegerField(default=0)

    def __str__(self):
        return f"AidRequest {self.request_id} by {self.user.name}"


class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'donor'})
    request = models.ForeignKey(AidRequest, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    donation_date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=100, null=True, blank=True)
    transaction = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Donation {self.donation_id} - {self.amount}"


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
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="unread")

    def __str__(self):
        return f"Notification {self.notification_id} for {self.user.name}"


class VolunteerAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'volunteer'})
    request = models.ForeignKey(AidRequest, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="assigned_by_admin")
    assignment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="assigned")

    def __str__(self):
        return f"Assignment {self.assignment_id} - {self.volunteer.name}"

