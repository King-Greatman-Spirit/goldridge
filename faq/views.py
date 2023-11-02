from django.shortcuts import render, get_object_or_404
from .models import FAQCategory, FAQQuestion

def faq_question(request, id=None):
    if id:
        # Get questions for the selected category
        category = get_object_or_404(FAQCategory, id=id)
        questions = FAQQuestion.objects.filter(category=category)
        context = {
            'category': category,
            'questions': questions,
        }
    else:
        # Display category listing when no specific category is selected
        categories = FAQCategory.objects.all()
        context = {
            'categories': categories,
        }

    return render(request, 'faq/faq.html', context)

