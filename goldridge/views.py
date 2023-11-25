from django.shortcuts import render, redirect
from company.models import Company, CompanyOverview
from service.models import Service, ServiceProcess, Testimonial
from staff.models import Staff
from blog.models import Article, Author, Paragraph
from enquiry.forms import LeadForm


def home(request):
    title = "Home"
    company = Company.objects.get(id=1, is_client=False)
    company_overview = CompanyOverview.objects.get(company=company)
    services = Service.objects.filter(company=company)
    staffs = Staff.objects.filter(company=company)[:3]
    Testimonials = Testimonial.objects.filter(company=company)


    # articles = Article.objects.all().order_by('-id')[:3]
    # display_paragraph = {}
    # for article in articles:
    #     for paragraph in Paragraph.objects.filter(article=article):
    #         display_paragraph[article.id] = ' '.join(paragraph.paragraph_content.split(' ')[:18]) + '...'
    #         break

    form = LeadForm()


    context = {
        'company': company,
        'company_overview': company_overview,
        'services': services,
        'staffs': staffs,
        # 'articles': articles,
        # 'display_paragraph': display_paragraph,
        'title': title,
        'form': form,
        'Testimonials': Testimonials,
    }

    return render(request, 'home.html', context)

