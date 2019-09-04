import ast

from django.shortcuts import render

from main.models import NewsPage


# Create your views here.

def index(request):
    return render(request, 'search/index.html')


def news(request):
    titlelist = []
    for page in NewsPage.objects.order_by('-time')[0:10]:
        newstitle = {
            'id': page.id,
            'title': page.title,
            'time': page.time.strftime("%Y-%m-%d %H:%M:%S"),
            'source': page.source_name,
        }
        titlelist.append(newstitle)
    return render(request, 'search/news.html', locals())


def teams(request):
    return render(request, 'search/teams.html')


def search(request):
    result = request.GET['search']
    return render(request, 'search/result.html', locals())


def news_page(request, page_id):
    newspage = NewsPage.objects.get(id=page_id)
    newsbody = ast.literal_eval(newspage.body)
    return render(request, 'search/newspage.html', locals())
