from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQCategory, FAQQuestion
from django.contrib.auth.decorators import login_required
from accounts.views import login
from .forms import FAQCategoryForm
from django.contrib import messages

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


@login_required(login_url = 'login')
def faqcategory_dashboard(request):
    faqcategories = FAQCategory.objects.all()
    
    if request.method == 'POST':
        form = FAQCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            data = FAQCategory()
            data.name = form.cleaned_data['name']
            data.save()
            messages.success(request, 'Thank you! Your FAQ Category has been created.')
            return redirect('faqcategory_dashboard')
    else:
        form = FAQCategoryForm()

    context = {
        'form': form,
        'faqcategories': faqcategories
    }

    return render(request, 'faq/category_dashboard.html', context)

@login_required(login_url = 'login')
def delete_faqcategory(request, id):
    deleted_faqcategory = FAQCategory.objects.get(id=id)
    deleted_faqcategory.delete()
    return redirect('faqcategory_dashboard')

@login_required(login_url = 'login')
def update_faqcategory(request, id):
    faqcategories = FAQCategory.objects.all()

    updated_faqcategory = get_object_or_404(FAQCategory, id=id)
    form = FAQCategoryForm(request.POST or None, request.FILES or None, instance=updated_faqcategory)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('faqcategory_dashboard')

    context = {
        'form': form,
        'faqcategories': faqcategories,
        'updated_faqcategory': updated_faqcategory
    }
    return render(request, 'faq/category_dashboard.html', context)
