from django.shortcuts import render, redirect
from blog.models import Article, Author, Paragraph
from enquiry.forms import LeadForm
# Create your views here.

def article(request, article_id):
    article = Article.objects.get(id=article_id)
    paragraphs = Paragraph.objects.filter(article=article).order_by('id')
    articles = Article.objects.all().order_by('-id')[:3]
    title = "Article: {}".format(article.article_title)
    form = LeadForm()

    context = {
        'article': article,
        'paragraphs': paragraphs,
        'articles': articles,
        'title': title,
        'form': form,

    }

    return render(request, 'blog/article.html', context)

def blog(request, keyword=None):
    title="Blog"
    if keyword != None:
        article_ids = []
        articles = Article.objects.all()
        for article in articles:
            for paragraph in Paragraph.objects.filter(article=article):
                if keyword in paragraph.paragraph_content:
                    if article.id not in article_ids:
                        article_ids.append(article.id)

        articles = Article.objects.filter(id__in=article_ids).order_by('-id')
        latest_articles = Article.objects.filter().order_by('-id')[:3]
    else:
        articles = Article.objects.filter().order_by('-id')
        latest_articles = articles[:3]

    display_paragraph = {}
    for article in articles:
        for paragraph in Paragraph.objects.filter(article=article):
            display_paragraph[article.id] = ' '.join(paragraph.paragraph_content.split(' ')[:60]) + '...'
            break

    context = {
        'articles': articles,
        'display_paragraph': display_paragraph,
        'latest_articles': latest_articles,
        'title': title,

    }

    return render(request, 'blog/blog.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        title = title = "Blog Search: {}".format(keyword)
        if keyword:
            article_ids = []
            articles = Article.objects.all()
            for article in articles:
                for paragraph in Paragraph.objects.filter(article=article):
                    if keyword in paragraph.paragraph_content:
                        if article.id not in article_ids:
                            article_ids.append(article.id)

            articles = Article.objects.filter(id__in=article_ids).order_by('-id')

            display_paragraph = {}
            for article in articles:
                for paragraph in Paragraph.objects.filter(article=article):
                    display_paragraph[article.id] = ' '.join(paragraph.paragraph_content.split(' ')[:60]) + '...'
                    break

            latest_articles = Article.objects.filter().order_by('-id')[:3]

            context = {
                'articles': articles,
                'display_paragraph': display_paragraph,
                'latest_articles': latest_articles,
                'title': title,
            }

            return render(request, 'blog/blog.html', context)
    return redirect('blog')

