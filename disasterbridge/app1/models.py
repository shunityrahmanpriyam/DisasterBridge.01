from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=[('victim','Victim'),('volunteer','Volunteer'),('donor','Donor'),('admin','Admin')])
    language_preference = models.CharField(max_length=20, default='English')
    verification_status = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)


class AidRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    urgency_level = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)
    voice_message_path = models.FileField(upload_to="voice/", null=True, blank=True)
    priority_score = models.IntegerField(default=0)