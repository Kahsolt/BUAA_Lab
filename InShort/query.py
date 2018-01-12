#!/usr/bin/env python3

import urllib.parse
import requests
import re

URLBASE_SEARCH_ENGINE = [
    # 'https://www.google.com/search?q=',
    # 'http://www.bing.com/search?q=',
    'http://search.yahoo.com/search?p=',
    # 'http://duckduckgo.com/?q=',
    # 'http://www.baidu.com/s?wd=',

    # 'http://www.zhihu.com/search?q=',
    'http://zhidao.baidu.com/search?word=',
]

def goWeb(keywords):
    kw = ' '.join(keywords)
    qkw = urllib.parse.quote(kw)

    for urlbase in URLBASE_SEARCH_ENGINE:
        url = urlbase + qkw
        resp = requests.get(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
        )
        if resp.status_code == 200:
            fn = 'WebData/' + (re.findall('.*//(.*)/.*', urlbase)[0] or 'page') + '.html'
            fout=open(fn,'wb')
            fout.write(resp.content)
            fout.close()
        else:
            raise Exception("Web access error")

    return


if __name__ == '__main__':
    goWeb(['北京', '海淀', '天气'])