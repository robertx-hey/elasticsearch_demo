


from elasticsearch import Elasticsearch
es = Elasticsearch()


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

if __name__ == '__main__':
    while 1:
        res = input('>>>>:')
        print(suggest_data(res))





        ''''
        
        pyhyon
        python
        
        '''