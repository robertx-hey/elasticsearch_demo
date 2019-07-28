from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.http import urlencode

from web import models

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from utils.pagination import Pagination

# Create your views here.
es = Elasticsearch()


def search_data(query, tags=None):
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "title": query
                        }
                    },
                    {
                        "match": {
                            "summary": query
                        }
                    }
                ],
                "filter": {
                    "match": {
                        "tags": tags
                    }
                }
            }
        },
        "highlight": {
            "pre_tags": "<strong class='key' style='color:red'>",
            "post_tags": "</strong>",
            "fields": {
                "*": {},
            }
        },
        "size": 200
    }

    ret_list = es.search(index='autohome', body=body, _source=['title', 'url', 'img_url', 'summary', 'tags'])
    return ret_list


def index(request):
    if request.method == 'POST':
        query = request.POST.get('q')

        ret_list = search_data(query)

        print(ret_list['hits']['hits'], type(ret_list))
        print(ret_list['hits']['total'], type(ret_list))

        total = ret_list['hits']['total']

        # 分页
        page = Pagination(request.GET.get('page', 1), total, 12)

        return JsonResponse({"ret_list": ret_list['hits']['hits'], 'total': total,
                             'page_html': page.page_html})

    return render(request, 'index.html')


def search(request):
    query = request.GET.get('q')
    tags = request.GET.get('type', 'news')
    current_page = request.GET.get('page', 1)

    ret_list = search_data(query, tags)
    total = ret_list['hits']['total']
    count = ret_list['hits']['hits'].__len__()  # type:list

    page_obj = Pagination(current_page, count)

    return JsonResponse({
        "ret_list": ret_list['hits']['hits'][page_obj.start:page_obj.end],
        'total': total,
        'page_html': page_obj.page_html
    })


def my_func(request):
    info = request.path_info
    print(info)
    query = info.split('/My/')[-1]

    ret = models.All_info.objects.filter(url__startswith=query).first()
    print(query, ret)
    return render(request, 'my.html', {'obj': ret})


# 建议器

def suggest_data(query):
    body = {
        "suggest": {
            "text": query,
            "s1": {
                "term": {
                    "field": "word"
                }
            },
            "s2": {
                "phrase": {
                    "field": "word",
                    "highlight": {
                        "pre_tag": "<strong class='key' style='color:red'>",
                        "post_tag": "</strong>"
                    }
                }
            },
            "s3": {
                "completion": {
                    "field": "word"
                }
            }
        }

    }

    ret_list = es.search(index='collins', body=body, _source=['word'])
    return ret_list


# 建议器
def suggest(request):

    query = request.GET.get('q', '')
    print(query)

    ret_list = suggest_data(query)
    print(ret_list)

    s1 = ret_list['suggest']['s1'][-1].get('options') if ret_list['suggest']['s1'] else []
    s2 = ret_list['suggest']['s2'][-1].get('options') if ret_list['suggest']['s2'] else []
    s3 = ret_list['suggest']['s3'][-1].get('options') if ret_list['suggest']['s2'] else []

    all_lst = s1 + s2 + s3
    all_lst.sort(key=lambda x: x.get('_score') if x.get('_score') else x.get('score'), reverse=True)

    msg_list = []
    for i in all_lst:
        msg_list.append(i.get('text'))

    msg_list = list(set(msg_list))[:6]

    return JsonResponse({'msg_list': msg_list})
