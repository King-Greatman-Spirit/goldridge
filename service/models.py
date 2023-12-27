from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from company.models import Company
from accounts.models import Account
from django.urls import reverse
from django.utils.text import slugify

# Import the 'uuid' module for generating universally unique identifiers (UUIDs).
import uuid
from django.utils import timezone
from datetime import datetime
import time
from shortuuid import ShortUUID  # Add this import statement
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    service_description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='photos/services')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     value = self.service_name
    #     self.slug = slugify(value, allow_unicode=True)
    #     super().save(*args, **kwargs)

    def update_url(self):
        return reverse('update_service', args=[self.id])

    def delete_url(self):
        return reverse('delete_service', args=[self.id])

    def service_url(self):
        return reverse('service_slug', args=[self.slug])

    def __str__(self):
        return self.service_name

class ServiceProcess(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='1')
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all=False,
        auto_choose=True,
        default=None)
    process_name = models.CharField(max_length=50)
    process_description = models.TextField(max_length=300)
    image = models.ImageField(upload_to='photos/service_process', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def update_url(self):
        return reverse('update_service_process', args=[self.id])

    def delete_url(self):
        return reverse('delete_service_process', args=[self.id])

    class Meta:
        verbose_name = 'ServiceProcess'
        verbose_name_plural = 'Service Processes'

    def __str__(self):
        return self.process_name

class Testimonial(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all = False,
        auto_choose=True,
        default=None)
    description = models.TextField(max_length=100)
    client_full_name = models.CharField(max_length=100, default=True)
    client_location = models.CharField(max_length=50, default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.description


class SubServiceType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all = False,
        auto_choose=True,
        default=None)
    type = models.CharField(max_length=100)
    abbr = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'SubServiceType'
        verbose_name_plural = 'SubService Types'

    def __str__(self):
        return self.type
    
    def update_url(self):
        return reverse('update-subservice-type', args=[self.id])

    def delete_url(self):
        return reverse('delete-subservice-type', args=[self.id])

approval_chioce = (
    (0,'Select Approval'),
    ('Pending','Pending'),
    ('Approved', 'Approved'),
    ('Not Approved', 'Not Approved'),
)

class SubService(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all=False,
        auto_choose=True,
        default=None)
    subServiceType = ChainedForeignKey(
        SubServiceType,
        chained_field="service",
        chained_model_field="service",
        show_all=False,
        auto_choose=True,
        default=None)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, null=True)
    approval = models.CharField(max_length=100, choices=approval_chioce, default='Pending')
    
    approval_note = models.TextField(max_length=500)
    duration = models.IntegerField(blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    char_id = ShortUUIDField(
    length=13,
    max_length=22,  # Adjusted max length to accommodate ShortUUID length
    prefix="acc_",
    alphabet="abcdefghijkmnopqrstuvwxyz1234567890",
    unique=True,
    blank=True,
    null=True
)
    class Meta:
        verbose_name = 'SubService'
        verbose_name_plural = 'SubServices'
        ordering = ['approval', 'created_date']

    def __str__(self):
        return str(self.duration)
    def update_url(self):
        return reverse('update_admin_service_app', args=[self.id])

    def delete_url(self):
        return reverse('delete_admin_service_app', args=[self.id])
    
    # Function to get the URL for updating a type in the dashboard.
    # It uses the reverse function to generate a URL based on the 'update-type-dashboard' URL pattern,
    # appending the service ID and app ID as arguments.
    def get_update_type_url(self):
        return reverse('update-type-dashboard', args=[self.id])

    # Function to get the URL for deleting a type in the dashboard.
    # It uses the reverse function to generate a URL based on the 'delete-type-dashboard' URL pattern,
    # appending the instance's ID as an argument.
    def get_delete_type_url(self):
        return reverse('delete-type-dashboard', args=[self.id])


class Prerequisite(models.Model): 
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all = False,
        auto_choose=True,
        default=None)
    subServiceType =  ChainedForeignKey(
        SubServiceType,
        chained_field="service",
        chained_model_field="service",
        show_all = False,
        auto_choose=True,
        default=None)
    prerequisite = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.prerequisite

transactionType_chioce = (
    (0,'Select Transaction Type'),
    ('credit','credit'),
    ('debit', 'debit'),
)

class Transaction(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all = False,
        auto_choose=True,
        default=None)
    subServiceType =  ChainedForeignKey(
        SubServiceType,
        chained_field="service",
        chained_model_field="service",
        show_all = False,
        auto_choose=True,
        default=None)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transactionType = models.CharField(max_length=100, choices=transactionType_chioce, default=0)
    user_email = models.EmailField(max_length=50)
    cumulativeOut = models.IntegerField(blank=True, null=True)
    cumulativeIn = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
         return str(self.amount)  # Convert to string
    