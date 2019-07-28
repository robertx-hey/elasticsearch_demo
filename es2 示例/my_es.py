'''
pip install elasticsearch
'''
from elasticsearch import Elasticsearch

es = Elasticsearch()

'''
PUT p1/doc/1
{
  "name":"娄鲲鹏"
}


'''

# -------- 创建一篇文档 --------------
# print(es.index(index='p1', doc_type='doc', id=1, body={"name":"lou"}))
# print(es.get(index='p1', doc_type='doc', id=1))
# print(es.delete(index='p1', doc_type='doc', id=2))
# print(es.index(index='p1', doc_type='doc', id=1, body={"name":"lou2"}))


# body = {
#     "query":{
#         "match":{
#             "name":"lou2"
#         }
#     }
# }
# print(es.search(index='p1', body=body, filter_path=['hits.hits']))
# print(es.search(index='p1', body=body, filter_path=['hits.hits._source']))
# print(es.search(index='p1', body=body, filter_path=['hits.hits._source', 'hits.total']))
# print(es.search(index='p1', body=body, filter_path=['hits.*']))
# print(es.search(index='p1', body=body, filter_path=['hits.hits._*']))

# print(es.get_source(index='p1', doc_type='doc', id=1))   # {'name': 'lou2'}

# for i in range(2, 11):
#     print(es.index(index='p1', doc_type='doc', body={'name': 'lou%s'% i}))


# print(es.count(index='p1', doc_type='doc', body={
#     "query":{
#         "match":{
#             "name":"lou2"
#         }
#     }
# }))


# print(es.create(index='p2', doc_type='doc', id='1', body={"name": '王五', "age": 20}))
# print(es.get(index='p2', doc_type='doc', id='1'))

# print(es.delete_by_query(index='p1', body={
#     "query": {
#         "match": {
#             "name": "lou2"
#         }
#     }
# }))

# print(es.index(index='p1', doc_type='doc', id=1, body={"name":"louxxx"}))

# print(es.exists(index='p1', doc_type='doc', id=1))
# print(es.exists(index='p2', id=1))



# print(es.info())


# print(es.ping())

# print(es.indices.exists(index='p1'))




body = {
    "mappings":{
        "doc": {
            "properties":{
                "name":{
                    "type":"text"
                },
                "age":{
                    "type":"long"
                }
            }
        }
    }
}

# print(es.indices.delete(index='p3'))

# print(es.indices.create(index='p3', body=body))
# print(es.indices.get_mapping(index='p3'))
# print(es.indices.get_settings(index='p3'))
# print(es.indices.analyze(body={"analyzer": "ik_smart", "text": "娄坤萌真猛"}))
# print(es.indices.put_alias(index='p1', name='p11'))
# print(es.indices.get_alias(index='p1'))
# print(es.indices.delete_alias(index='p1', name='p11'))
# print(es.indices.get(index='p1'))
# print(es.indices.get(index=['p1', 'p2']))

# print(es.indices.close(index='p1'))
# print(es.indices.open(index='p1'))
#
# print(es.cat.indices(index='p1'))


# print(es.cluster.get_settings())
# print(es.cluster.health())

# print(es.cluster.state())

# print(es.cluster.stats())

# print(es.cat.count(format='json'))



# 'https://www.autohome.com.cn/news/201905/936562.html#pvareaid=102624'
# print('https://www.autohome.com.cn/use/201905/936562.html#pvareaid=102624'.split('/', 4)[3])

# print(es.count(index='s18')['count'])


from elasticsearch import helpers

import time
s = time.time()

# with open(r'new_suggest_data.txt', 'r', encoding='utf8') as f:
#     actions = ({
#         "_index": "my_suggest",
#         "_type": "doc",
#         "_source": {
#             "title": i.strip()
#         }
#     } for i in f)
#     helpers.bulk(es, actions=actions)
# print(time.time() - s)



def foo(search_msg):
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
                    "size": 3,
                    "skip_duplicates": True
                }
            }
        }
    }

    res = es.search(index='my_suggest', body=body)['suggest']

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

if __name__ == '__main__':
    while 1:
        res = input('>>>: ').strip()
        print(foo(res))
# for i in []:
#     print(1111111111, i)








