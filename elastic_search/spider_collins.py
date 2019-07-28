import os
import time

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count


def worker(n):
    response = requests.get(
        url='https://www.collinsdictionary.com/browse/english/words-starting-with-{}'.format(chr(n[0])))
    soup_obj = BeautifulSoup(response.text, 'html.parser')
    ul_obj = soup_obj.find(name='ul', attrs={'class': "columns2 browse-list"})
    for i in ul_obj:
        if i.find('a') != -1:
            desc_obj = requests.get(url=i.find('a').get('href'))
            soup_obj2 = BeautifulSoup(desc_obj.text, 'html.parser')
            ul_obj2 = soup_obj2.find(name='ul', attrs={'class': 'columns2 browse-list'})
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
    start = time.time()
    print('开始')
    collins()
    print('结束,用时%s' % (time.time() - start))
