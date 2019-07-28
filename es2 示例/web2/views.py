
from django.shortcuts import render, HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from django.http.response import JsonResponse
from web2 import models



es = Elasticsearch()
# Create your views here.

class Pagination:

    def __init__(self, current_page, all_count, per_num=20, max_show=11):
        # 基本的URL
        # self.base_url = request.path_info
        # 当前页码
        try:
            # self.current_page = int(request.GET.get('page', 1))
            self.current_page = int(current_page)
            if self.current_page <= 0:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1
        # 最多显示的页码数
        self.max_show = max_show
        half_show = max_show // 2

        # 每页显示的数据条数
        self.per_num = per_num
        # 总数据量
        self.all_count = all_count

        # 总页码数
        self.total_num, more = divmod(all_count, per_num)
        if more:
            self.total_num += 1

        # 总页码数小于最大显示数：显示总页码数
        if self.total_num <= max_show:
            self.page_start = 1
            self.page_end = self.total_num
        else:
            # 总页码数大于最大显示数：最多显示11个
            if self.current_page <= half_show:
                self.page_start = 1
                self.page_end = max_show
            elif self.current_page + half_show >= self.total_num:
                self.page_end = self.total_num
                self.page_start = self.total_num - max_show + 1
            else:
                self.page_start = self.current_page - half_show
                self.page_end = self.current_page + half_show

    @property
    def start(self):
        return (self.current_page - 1) * self.per_num

    @property
    def end(self):
        return self.current_page * self.per_num

    @property
    def show_li(self):
        # 存放li标签的列表
        html_list = []

        # first_li = '<li><a href="{}?page=1">首页</a></li>'.format(self.base_url)
        # html_list.append(first_li)

        if self.current_page == 1:
            prev_li = '<li class="disabled"><a>上一页</a></li>'
        else:
            prev_li = '<li><a href="javascript:;" page={}>上一页</a></li>'.format(self.current_page - 1)
        html_list.append(prev_li)
        for num in range(self.page_start, self.page_end + 1):
            if self.current_page == num:
                li_html = '<li class="active"><a href="javascript:;" page={0}>{0}</a></li>'.format(num)
            else:
                li_html = '<li><a href="javascript:;" page={0}>{0}</a></li>'.format(num)
            html_list.append(li_html)

        if self.current_page == self.total_num:
            next_li = '<li class="disabled"><a>下一页</a></li>'
        else:
            next_li = '<li><a href="javascript:;" page={}>下一页</a></li>'.format(self.current_page + 1)
        html_list.append(next_li)

        # last_li = '<li><a href="#" page>尾页</a></li>'.format(self.total_num, self.base_url)
        # html_list.append(last_li)
        return ''.join(html_list)





def filter_msg(search_msg, action_type, current_page):

    if action_type == 'all':   # 查询全部
        body = {
            "size": 10000,
            "query": {
                "match":{
                    "title": search_msg
                }
            },
            "highlight":{
                "pre_tags": "<b style='color:red;'>",
                "post_tags": "</b>",
                "fields":{
                    "title": {}
                }
            }
        }
    else:
        body = {
            "size": 10000,
            "query": {
                "bool":{
                    "must":[
                        {
                            "match":{
                                "title": search_msg
                            }
                        },
                        {
                            "match":{
                                "tags": action_type
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "pre_tags": "<b style='color:red;'>",
                "post_tags": "</b>",
                "fields": {
                    "title": {}
                }
            }
        }
    res = es.search(index='s18', body=body, filter_path=['hits.total', 'hits.hits'])
    page_obj = Pagination(current_page ,res['hits']['total'])
    print(11111111, search_msg, action_type, current_page)
    res['page'] = page_obj.show_li
    res['data_msg'] = res['hits']['hits'][page_obj.start:page_obj.end]
    res['hits']['hits'] = ''
    return res


def index(request):
    # if request.method == 'POST':
    #     search_msg = request.POST.get("search_msg")
    #     res = filter_msg(search_msg)
    #     return JsonResponse(res)
    # else:
    #     return render(request, 'index.html')


    if request.method == 'GET':
        flag = request.GET.get('flag', 'aaa')
        if flag == 'aaa': # 正常请求，给页面
            obj = models.Article.objects.filter(pk__lte=10)
            return render(request, 'index.html', {'all_obj': obj})
        else:
            search_msg = request.GET.get("search_msg")
            action_type = request.GET.get('action_type')
            current_page = request.GET.get('current_page')

            print(11111111, search_msg, action_type, current_page)
            res = filter_msg(search_msg, action_type, current_page)
            return JsonResponse(res)



def search_suggest(search_msg):

    body = {
        "suggest": {
            "text": search_msg,
            "s1": {
                "term": {
                    "field": "title",
                    "size": 3
                }
            },
            "s2": {
                "phrase": {
                    "field": "title",
                    "size": 3,
                    "highlight": {
                        "pre_tag": "<b style='color:red'>",
                        "post_tag": "</b>"
                    }
                }
            },
            "s3": {
                "completion": {
                    "field": "title",
                    "size": 3
                }
            }
        }
    }

    res = es.search(index='my_suggest', body=body)
    l = []
    s1 = res['s1']
    s2 = res['s2'][0]
    s3 = res['s3'][0]
    if s3:
        for i in s3['options']:
            l.append(i.get('text'))
    if s1:
        for i in s1[0]['options']:

            l.append(i.get('text'))
    if s2:
        for i in s2['options']:
            if i.get('text') not in l:
                l.append(i.get('highlighted'))
    return l


def suggest(request):
    if request.method == 'POST':
        search_msg = request.POST.get("search_msg")
        res = search_suggest(search_msg)
        print(res)
        return JsonResponse(res, safe=False)
    else:
        return render(request, 'index.html')


    # if request.method == 'GET':
    #     flag = request.GET.get('flag', 'aaa')
    #     if flag == 'aaa': # 正常请求，给页面
    #         obj = models.Article.objects.filter(pk__lte=10)
    #         return render(request, 'index.html', {'all_obj': obj})
    #     else:
    #         search_msg = request.GET.get("search_msg")
    #         action_type = request.GET.get('action_type')
    #         current_page = request.GET.get('current_page')
    #
    #         print(11111111, search_msg, action_type, current_page)
    #         res = filter_msg(search_msg, action_type, current_page)
    #         return JsonResponse(res)




def search(request):
    ''' 备胎 '''
    if request.method == 'GET':
        search_msg = request.GET.get("search_msg")
        res = filter_msg(search_msg)
        return JsonResponse(res)






def es2(request):


    body = {
        "mappings":{
            "doc":{
                "properties":{
                    "title":{
                        "type":"text",
                        "analyzer": "ik_smart"
                    },
                    "summary": {
                        "type": "text"
                    },
                    "a_url": {
                        "type": "keyword"
                    },
                    "img_url":{
                        "type": "keyword"
                    },
                    "tags": {
                        "type": "text"
                    }
                }
            }
        }
    }

    # print(es.indices.delete(index='s18'))
    # print(es.indices.exists(index='s18'))
    # es.indices.create(index='s18', body=body)
    # print(es.indices.get_mapping(index='s18'))

    # count = models.Article.objects.count()
    # print(count)
    query_obj = models.Article.objects.all()

    action = (
        {
            "_index": "s18",
            "_type": "doc",
            "_source": {
                "title": i.title,
                "summary": i.summary,
                "a_url": i.a_url,
                "img_url": i.img_url,
                "tags": i.tags

            }
        } for i in query_obj)
    # print(action, next(action))
    import time
    s = time.time()

    helpers.bulk(es, action)
    print(time.time() - s)


    return HttpResponse('OK')


def filter_msg2(request):

    d = request.META['PATH_INFO'].split('/f/', 1)[-1]
    print(11, d, type(d))
    obj = models.Article.objects.filter(title=d).first()
    print(obj, type(obj), obj.title)
    return render(request, 'desc.html', {"obj": obj})








