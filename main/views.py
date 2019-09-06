import json
import math
import time
from operator import itemgetter

import jieba
import jieba.analyse
import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from main import handle
from main.models import NewsPage, KeyWord


# Create your views here.

def index(request):
    return render(request, 'search/index.html')


def news(request):
    titlelist = []
    for page in NewsPage.objects.order_by('-time'):
        newstitle = {
            'id': page.id,
            'title': page.title,
            'time': page.time.strftime("%Y-%m-%d %H:%M:%S"),
            'source': page.source_name,
            'body': json.loads(page.body),
        }
        titlelist.append(newstitle)
    return render(request, 'search/news.html', locals())


def teams(request):
    return render(request, 'search/teams.html')


def search(request):
    start_time = time.clock()
    jieba.analyse.set_stop_words('main/stop_words.txt')
    jieba.analyse.set_idf_path('main/idf.txt.big')
    sentence = request.GET['search']
    tags = jieba.analyse.extract_tags(sentence, withWeight=True)
    words = []
    weight = {}
    search_mod = 0.0
    for tag in tags:
        if KeyWord.objects.filter(word=tag[0]).count():
            words.append(tag[0])
            weight[tag[0]] = tag[1]
            search_mod += tag[1] ** 2
    pages = []
    for word in words:
        pages.extend(KeyWord.objects.filter(word=word)[0].newspage_set.all())
    pages = list(set(pages))
    page_rank = []
    for page in pages:
        page_to_cmp = {'page': {
            'id': page.id,
            'title': page.title,
            'time': page.time.strftime("%Y-%m-%d %H:%M:%S"),
            'source': page.source_name,
            'body': json.loads(page.body),
        }}
        title = page.title
        body = '\n'.join(json.loads(page.body))
        title_product = 0.0
        title_tags = jieba.analyse.extract_tags(title, topK=5, withWeight=True)
        for tag in title_tags:
            if tag[0] in weight.keys():
                title_product += weight[tag[0]] * tag[1]
        title_product /= math.sqrt(page.title_key_mod * search_mod)
        body_product = 0.0
        body_tags = jieba.analyse.extract_tags(body, topK=20, withWeight=True)
        for tag in body_tags:
            if tag[0] in weight.keys():
                body_product += weight[tag[0]] * tag[1]
        body_product /= math.sqrt(page.body_key_mod * search_mod)
        page_to_cmp['sim'] = title_product * 0.5 + body_product * 0.5
        page_rank.append(page_to_cmp)
    page_rank.sort(key=itemgetter('sim'), reverse=True)
    time_pass = time.clock() - start_time
    result = {
        'keywords': words,
        'page_rank': page_rank,
        'len': len(page_rank),
        'time': '{0:0.4f}'.format(time_pass)
    }
    return render(request, 'search/result.html', {'result': result})


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


def rebuild(request):
    handle.rebuild()
    return JsonResponse({'result': 'ok'})
