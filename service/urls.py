""" URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('services/<slug:slug>/', views.service, name='service_slug'),
    path('service_dashboard/', views.service_dashboard, name='service_dashboard'),
    path('update_service/<int:id>', views.update_service, name='update_service'),
    path('delete_service/<int:id>', views.delete_service, name='delete_service'),
    path('service_process_dashboard/', views.service_process_dashboard, name='service_process_dashboard'),
    path('update_service_process/<int:id>', views.update_service_process, name='update_service_process'),
    path('delete_service_process/<int:id>', views.delete_service_process, name='delete_service_process'),
    path('user_service_applications/', views.user_subService_dashboard, name='user_service_applications'),
    path('admin_service_applications/', views.admin_subService_dashboard, name='admin_service_applications'),
    path('update_admin_service_app/<int:id>', views.update_admin_subService, name='update_admin_service_app'),
    path('delete_admin_service_app/<int:id>', views.delete_admin_subService, name='delete_admin_service_app'),
    path('apps-by-type/', views.apps_by_type, name='apps-by-type'),
    path('type-dashboard/<int:id>', views.type_dashboard, name='type-dashboard'),
    path('update-type-dashboard/<int:service_id>/<int:app_id>/', views.update_type_dashboard, name='update-type-dashboard'),
    path('delete-type-dashboard/<int:id>', views.delete_type_dashboard, name='delete-type-dashboard'),
    path('clients-table/', views.clients_table, name='clients-table'),
]

