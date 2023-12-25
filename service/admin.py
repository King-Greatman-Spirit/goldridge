from django.contrib import admin
from .models import ( Service, ServiceProcess, Testimonial,  
    SubServiceType, SubService, Prerequisite, Transaction 
)

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service_name',)}
    list_display = ('service_name', 'slug', 'created_date', 'modified_date')


class ServiceProcessAdmin(admin.ModelAdmin):
    list_display = ('process_name', 'service', 'created_date', 'modified_date')

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('service', 'client_full_name', 'client_location', 'created_date')

class SubServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('service', 'type', 'abbr')

class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'subServiceType', 'user', 'created_date')
    
class PrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('service', 'subServiceType', 'prerequisite')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('service', 'subServiceType', 'user', 'transactionType', 'created_date')


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceProcess, ServiceProcessAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(SubServiceType, SubServiceTypeAdmin)
admin.site.register(SubService, SubServiceAdmin)
admin.site.register(Prerequisite, PrerequisiteAdmin)
admin.site.register(Transaction, TransactionAdmin)
