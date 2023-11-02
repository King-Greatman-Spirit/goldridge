from django.urls import path
from . import views

urlpatterns = [
    path('faq/', views.faq_question, name='faq_categories'),
    path('faq/<int:id>/', views.faq_question, name='faq_question'),
]
