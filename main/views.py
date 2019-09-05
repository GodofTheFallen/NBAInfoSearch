import json

import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from main.handle import handle_tf_idf
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
    newspage = get_object_or_404(NewsPage, id=page_id)
    newsbody = json.loads(newspage.body)
    return render(request, 'search/newspage.html', locals())


def spider_controller(request, spider_name):
    return render(request, 'crawl.html', locals())


def spider_start(request, spider_name):
    page_max = request.POST['page_max']
    if request.method == 'POST':
        # 启动爬虫
        url = 'http://localhost:6800/schedule.json'
        data = {
            'project': 'spiders',
            'spider': spider_name,
            'setting': 'page_max=' + page_max,
        }
        print(requests.post(url=url, data=data))
    return JsonResponse({'result': 'ok'})


def handle(request):
    handle_tf_idf()
    return JsonResponse({'result': 'ok'})
