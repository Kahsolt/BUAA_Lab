# -*- coding:utf-8 -*-
# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'CQC'
import urllib
import urllib2
import re
import HTMLParser
import isdigit
import os
import random
import requests
import time
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
hdr = {'User-Agent': user_agent}
values = {'username' : 'zhangshaojun96@163.com',  'password' : '123119117zsj' }
proxyselect=['122.72.32.73:80',
'61.134.242.154:8080',
'220.161.239.75:8118',
'114.102.15.48:8118',
'36.249.192.179:8118',
'61.157.43.252:8118',
'1.30.123.246:8118',
'61.160.6.158:81',
'223.240.239.37:8118',
'175.42.102.252:8118',
'36.33.25.99:808',
'182.112.228.38;80',
'183.166.243.124:808']

def removesame(list):
    newlist=[]
    for i in range(len(list)):
        if list[i] not in newlist:
            newlist.append(list[i])
    return newlist

class MyHTMLParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        #print tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        list=value.split("/")
                        if len(list)==4 and list[0]=="" and list[1]=="questions" and isdigit.is_number(list[2])==True:
                            self.links.append(value)
#百度贴吧爬虫类
class BDTB:

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self,baseUrl,page,rankWay):
        self.baseURL = baseUrl
        self.rankWay = '&sort='+rankWay

    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        try:
            f=open(self.rankWay+str(pageNum)+".txt","w")
            url = self.baseURL+ "?page="+ str(pageNum)+self.rankWay
            print url
            random_proxy = random.choice(proxyselect)
            proxies = {'http': 'http://' + random_proxy}
            print proxies
            # data = urllib.urlencode(values)
            # proxy_support = urllib2.ProxyHandler(proxies)
            # opener = urllib2.build_opener(proxy_support)
            # urllib2.install_opener(opener)
            # request = urllib2.Request(url,headers=hdr)
            response = requests.get(url, headers=hdr, proxies=proxies)
            while response.text=="":
                time.sleep(1000)
                response = requests.get(url, headers=hdr, proxies=proxies)
            f.write(response.text)
            return response
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None

if __name__ == "__main__":
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    headers = {'User-Agent': user_agent}

    baseURL = 'https://stackoverflow.com/questions'
    bdtb = BDTB(baseURL,1,"votes")
    for i in range(200000):
        if i<1079:
            continue
        bdtb.getPage(i)
        html_code = open('&sort=votes'+str(i)+'.txt').read()
        hp = MyHTMLParser()
        hp.feed(html_code)
        hp.close()
        print i,":",hp.links
        while len(hp.links)==0:
            time.sleep(1000)
            bdtb.getPage(i)
            html_code = open('&sort=votes' + str(i) + '.txt').read()
            hp = MyHTMLParser()
            hp.feed(html_code)
            hp.links = removesame(hp.links)
            hp.close()
            print i, ":", hp.links
        if os.path.exists('&sort=votes'+str(i))==False:
            os.mkdir('&sort=votes'+str(i))
        for s in hp.links:
            f=open('&sort=votes'+str(i)+"/"+s.split("/")[2]+".txt","w")
            baseurl="https://stackoverflow.com"+s
            print baseurl
            url=baseurl
            random_proxy = random.choice(proxyselect)
            proxies = {'http': 'http://' + random_proxy}
            # data = urllib.urlencode(values)
            # proxy_support = urllib2.ProxyHandler(proxies)
            # opener = urllib2.build_opener(proxy_support)
            # urllib2.install_opener(opener)
            # request = urllib2.Request(url,headers=hdr)
            response = requests.get(url, headers=hdr, proxies=proxies)
            while response.text.find("has performed an unusual high number of requests and has been temporarily")!=-1:
                time.sleep(1000)
                response = requests.get(url, headers=hdr, proxies=proxies)
            f.write(response.text)
