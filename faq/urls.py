from django.urls import path
from . import views

urlpatterns = [
    path('faq/', views.faq_list, name='faq_list'),
    path('faq/<int:id>/', views.faq_detail, name='faq_detail'),

]
