from django.urls import reverse
from django.db import models
from service.models import Service, ServiceProcess  # Import Service and ServiceProcess models

class FAQCategory(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'FAQCategory'
        verbose_name_plural = 'FAQCategories'

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs', blank=True, null=True)
    service_process = models.ForeignKey(ServiceProcess, on_delete=models.CASCADE, related_name='faqs', blank=True, null=True)
    question = models.CharField(max_length=500)
    answer = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    def get_url(self):
        return reverse('faq_detail', args=[str(self.category.id)])
