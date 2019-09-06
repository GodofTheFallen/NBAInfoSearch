import json
import math
import re

import jieba
import jieba.analyse
from django.db import transaction

from main.models import KeyWord
from main.models import NewsPage


# handle data in the database

@transaction.atomic
def rebuild():
    keywords = {}
    corpus = []
    for item in NewsPage.objects.all():
        article = '\n'.join([item.title, '\n'.join(json.loads(item.body))])
        corpus.append(article)

    for sentence in corpus:
        data = list(set(jieba.lcut_for_search(sentence)))
        for word in data:
            if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]+$', word) is None:
                continue
            if word in keywords.keys():
                keywords[word] += 1
            else:
                keywords[word] = 1
    
    total = len(corpus)

    idf = open('main/idf.txt.big', 'w', encoding='utf-8')

    count = 0
    keyword_items = {}
    keyword_list = []
    
    for word in keywords.keys():
        keyword_list.append(KeyWord(id=count, word=word, idf=math.log(total / keywords[word])))
        keyword_items[word] = count
        count += 1
        idf.write(word + ' {0:.8f}'.format(math.log(total / keywords[word])) + '\n')
    
    idf.close()
    
    jieba.analyse.set_stop_words('main/stop_words.txt')
    jieba.analyse.set_idf_path('main/idf.txt.big')
    
    current = 0
    item_list = NewsPage.objects.all()
    item_keyword_list = []
    for item in item_list:
        item_keyword_list.append(set())
        print(current)
        current += 1
        title = item.title
        body = '\n'.join(json.loads(item.body))
        title_tags = jieba.analyse.extract_tags(title, topK=5, withWeight=True)
        title_mod = 0
        for tag in title_tags:
            if tag[0] in keyword_items.keys():
                item_keyword_list[-1].add(keyword_items[tag[0]])
                title_mod += tag[1] ** 2
        item.title_key_mod = title_mod
        body_tags = jieba.analyse.extract_tags(body, topK=20, withWeight=True)
        body_mod = 0
        for tag in body_tags:
            if tag[0] in keyword_items.keys():
                item_keyword_list[-1].add(keyword_items[tag[0]])
                body_mod += tag[1] ** 2
        item.body_key_mod = body_mod
    current = 0
    with transaction.atomic():
        KeyWord.objects.all().delete()
        KeyWord.objects.bulk_create(keyword_list)
        for item in item_list:
            print(current)
            item.save()
            item.keywords.clear()
            for word in item_keyword_list[current]:
                item.keywords.add(KeyWord.objects.get(id=word))
            current += 1
