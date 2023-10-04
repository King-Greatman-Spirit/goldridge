from django.contrib import admin
from .models import Service, ServiceProcess

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service_name',)}
    list_display = ('service_name', 'slug', 'created_date', 'modified_date')


class ServiceProcessAdmin(admin.ModelAdmin):
    list_display = ('process_name', 'service', 'created_date', 'modified_date')


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceProcess, ServiceProcessAdmin)
