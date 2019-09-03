from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'search/index.html')


def news(request):
    return render(request, 'search/news.html')


def teams(request):
    return render(request, 'search/teams.html')


def search(request):
    result = request.GET['search']
    return render(request, 'search/result.html', locals())
