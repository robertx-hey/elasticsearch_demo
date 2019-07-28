'''
https://www.autohome.com.cn/all/

文章的：
    title
    summary
    a_url
    img_url
    tags


pip install requests
pip install BeautifulSoup4
pip install -i https://pypi.doubanio.com/simple/ requests


'''


import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


def work(k):
    response = requests.get(url='https://www.autohome.com.cn/all/{}/#liststart'.format(k))
    # print(response.headers)
    # print(response.encoding)
    # print(response.status_code)
    # print(response.text)
    response.encoding = 'GBK'
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    div_obj = soup_obj.find(name='div', attrs={"id": "auto-channel-lazyload-article"})
    li_list = div_obj.find_all(name='li')
    for i in li_list:
        no_obj = i.find(name='h3')
        if not no_obj: continue
        title = i.find(name='h3').text
        summary = i.find(name='p').text
        a = 'https:' + i.find(name='a').get('href')
        img = 'https:' + i.find(name='img').get('src')
        tags = a.split('/', 4)[3]
        print(response.url, title, tags)

def spider():
    """ 爬取汽车之家 """
    t = ThreadPoolExecutor(10)
    for k in range(1, 6839):
        t.submit(work, k)
    t.shutdown()





# ------------------------ 爬取柯林斯 --------------------


def worker(n):
    response = requests.get(url='https://www.collinsdictionary.com/browse/english/words-starting-with-{}'.format(chr(n[0])))
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    ul_obj = soup_obj.find(name='ul', attrs={'class': "columns2 browse-list"})
    for i in ul_obj:
        if i.find('a') != -1:
            desc_obj = requests.get(url=i.find('a').get('href'))
            soup_obj2 = BeautifulSoup(desc_obj.text, 'html.parser')
            ul_obj2 = soup_obj2.find(name='ul', attrs={'class': "columns2 browse-list"})
            for k in ul_obj2:
                if k.find('a') != -1:
                    res = k.find('a').text
                    if '-' in res or '&' in res or len(res) == 1:
                        continue
                    else:
                        print(desc_obj.url, res)
                        n[1].write('{}\n'.format(res))

def collins():
    f = open('d.txt', 'a', encoding='utf-8')
    t = ThreadPoolExecutor(cpu_count() * 5)
    for i in range(ord('a'), ord('z') + 1):
        t.submit(worker, (i, f))
    t.shutdown()
    f.close()








if __name__ == '__main__':
    import time
    start = time.time()
    # spider()

    collins()
    # print(cpu_count() * 5)
    # import re

    # res = re.compile('[-|&]')
    # print(re.findall(res, '-a'))
    # print(re.findall(res, 'A & M'))



    print(time.time() - start)

    # print(ord('a'), ord('z'))































