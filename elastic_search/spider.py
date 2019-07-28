import os
import time

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


def work(k):
    response = requests.get(url="https://www.autohome.com.cn/all/{}/#liststart".format(k))
    response.encoding = 'GBK'
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    div_obj = soup_obj.find(name='div',attrs={'id':"auto-channel-lazyload-article"})
    li_list = div_obj.find_all(name='li')

    work_list = []

    for i in li_list:
        no_obj = i.find(name='h3')
        if not no_obj: continue
        title = i.find(name='h3').text
        summary = i.find(name='p').text
        a = "https:" + i.find(name='a').get('href')
        img = 'https:' + i.find(name='img').get('src')
        tags = a.split('/',4)[3]
        print(response.url,title,tags)

        # 将数据添加进数据库
        bk_obj = models.All_info(url=response.url,title = title,tags=tags,summary=summary,img_url=img)
        work_list.append(bk_obj)

    # 批量插入，速度快
    models.All_info.objects.bulk_create(work_list)


def spider(t_count):
    '''
    爬取汽车之家
    :return:
    '''
    t = ThreadPoolExecutor(t_count)
    for k in range(1,6839):
        t.submit(work,k)
    t.shutdown()


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elastic_search.settings")
    import django
    django.setup()
    from web import models

    t_count = cpu_count()*5
    start = time.time()
    print('开始')
    spider(t_count)
    print('结束,用时%s'%(time.time()-start))