from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from company.models import Company
from django.urls import reverse
from django.utils.text import slugify


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
