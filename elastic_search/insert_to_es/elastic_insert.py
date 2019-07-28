import os
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch()


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时约 {:.2f} 秒'.format(time.time() - start))
        return res

    return wrapper


@timer
def gen(all_obj):
    """
    使用生成器批量写入数据
     All_info ->
     """
    action = ({
        "_index": "autohome",
        "_type": "doc",
        "_source": {

            "title": i.title,
            "tags": i.tags,
            "url": i.url,
            "img_url": i.img_url,
            "summary": i.summary
        }
    } for i in all_obj)
    helpers.bulk(es, action)



if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elastic_search.settings")
    import django

    django.setup()
    from web import models

    all_obj = models.All_info.objects.all()
    gen(all_obj)
