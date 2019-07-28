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
def gen(f):
    """
    使用生成器批量写入数据
     All_info ->
     """
    action = ({
        "_index": "collins",
        "_type": "doc",
        "_source": {
            "word": line.strip()
        }
    } for line in f)
    helpers.bulk(es, action)


if __name__ == '__main__':
    print('开始')
    f = open('../new_suggest_data.txt', 'r', encoding='utf-8')
    gen(f)
    f.close()
    # print(es.indices.get_mapping(index='collins'))
    # print(es.count(index='collins'))
    #
    # print(es.search(index='collins', body={
    #     "query":{
    #         "match":{
    #             "word":"apple"
    #         }
    #     }
    # }))







