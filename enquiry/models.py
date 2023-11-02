from django.db import models
from service.models import Service

# Create your models here.
channel_chioce = (
    (0,'Select How you heard about us'),
    ('Facebook','Facebook'),
    ('Instagram', 'Instagram'),
    ('Google','Google'),
    ('word of mouth','Word of Mouth'),
    ('youtube','Youtube'),
    ('Tictok','Tictok'),
    ('Marketer','Marketer'),
    ('others','Others'),
)


class Lead(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    company_name = models.CharField(max_length=50,  blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=100, choices=channel_chioce, default=0)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
