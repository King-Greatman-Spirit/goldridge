
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
    path('', views.company, name='company'),
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),
    path('update_company/<int:id>', views.update_company, name='update_company'),
    path('delete_company/<int:id>', views.delete_company, name='delete_company'),
    path('business_overview/', views.business_overview, name='business_overview'),
    path('update_business_overview/<int:id>', views.update_business_overview, name='update_business_overview'),
    path('delete_business_overview/<int:id>', views.delete_business_overview, name='delete_business_overview'),
]
