from django.shortcuts import render, get_object_or_404, redirect
from .models import FAQCategory, FAQ
from .forms import FAQForm

from django.shortcuts import render, get_object_or_404
from .models import FAQCategory, FAQ
from .forms import FAQForm
from django.contrib import messages


def faq_list(request):
    categories = FAQCategory.objects.all()  # Use .all() to get all categories

    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            # Create a new FAQ instance and populate it with form data
            faq = FAQ(
                category=form.cleaned_data['category'],
                service=form.cleaned_data['service'],
                question=form.cleaned_data['question'],
                answer=form.cleaned_data['answer']
            )
            faq.save()
            messages.success(request, 'Thank you! Your FAQ has been successfully added.')
            return redirect('faq_list')
            # Optionally, you can redirect to a success page or display a success message here
    else:
        form = FAQForm()

    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'faq/faq_list.html', context)



def faq_detail(request, id):
    category = get_object_or_404(FAQCategory, id=id)
    faqs = FAQ.objects.filter(category=category)
    context = {
        'category': category, 
        'faqs': faqs
    }
    return render(request, 'faq/faq_detail.html', context)
