from django.urls import path
from . import views

urlpatterns = [
    path('faq/', views.faq_question, name='faq_categories'),
    path('faq/<int:id>/', views.faq_question, name='faq_question'),
    path('faqcategory_dashboard/', views.faqcategory_dashboard, name='faqcategory_dashboard'),
    path('delete_faqcategory/<int:id>', views.delete_faqcategory, name='delete_faqcategory'),
    path('update_faqcategory/<int:id>', views.update_faqcategory, name='update_faqcategory'),
]
