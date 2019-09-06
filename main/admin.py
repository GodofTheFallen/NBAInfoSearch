from django.contrib import admin

from main.models import KeyWord
from main.models import NewsPage


# Register your models here.

class NewsPageAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    fields = (
        ('id', 'url'),
        'title',
        'time',
        ('source_name', 'source_url'),
        'body',
        'keywords',
        'title_key_mod',
        'body_key_mod',
    )
    list_display = ('id', 'title')
    list_filter = ('time', 'source_name')
    readonly_fields = ('id', 'url', 'title', 'time', 'source_name', 'source_url', 'body')
    search_fields = ['id', 'title', 'body']


class StartCrawlAction(admin.ModelAdmin):
    pass


admin.site.register(NewsPage, NewsPageAdmin)
admin.site.register(KeyWord)
