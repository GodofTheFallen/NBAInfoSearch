from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news', views.news, name='news'),
    path('teams', views.teams, name='teams'),
    path('result', views.search, name='search'),
    path('newspage/<int:page_id>', views.news_page, name='news_page')
]
