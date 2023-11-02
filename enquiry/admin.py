from django.contrib import admin
from .models import Lead, Newsletter
# Register your models here.
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'service', 'channel', 'created_date')
    list_per_page = 20

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    list_per_page = 20

admin.site.register(Lead, LeadAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
