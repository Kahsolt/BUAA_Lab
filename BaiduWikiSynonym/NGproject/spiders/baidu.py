# -*- coding: utf-8 -*-

import scrapy
import re
import urllib.parse
from NGproject.items import WordItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baike.baidu.com']
    start_urls = [
        'https://baike.baidu.com/item/苹果',
        # 'http://baike.baidu.com/',
    ]
    words = ['']

    def parse(self, response):
        print('[INFO] Visiting %s' % (response.url))

        word, qword = BaiduSpider.getWord(response.url)
        if word not in self.words:
            self.words.append(word)
            print("[INFO] Looking up word: %s" % (word))

            ul = response.xpath('//ul[@class="polysemantList-wrapper cmn-clearfix"]/li')
            if not ul == []:
                print("[INFO] Get synonym of %s!" % (word))

                span = ul.xpath('span')
                if len(span) > 1:
                    print('Bad Page! Links lacking...')
                    span = span[0]
                item = WordItem()
                item['word'] = word
                item['item'] = span.xpath('text()').extract_first()
                item['link'] = re.findall('.*baike.baidu.com(.*)', response.url)[0]
                yield item

                anchors = ul.xpath('a')
                for a in anchors:
                    item = WordItem()
                    item['word'] = word
                    item['item'] = a.xpath('text()').extract_first()
                    item['link'] = a.css('a::attr("href")').extract_first()
                    yield item

        # follow links
        for a in response.css('a::attr("href")').extract():
            if a.startswith('/item'):
                word, qword = BaiduSpider.getWord(response.urljoin(a))
                if word not in self.words:
                    yield response.follow(response.urljoin(a), self.parse)

    @classmethod
    def getWord(cls, url):
        qword = re.findall('.*baike.baidu.com/item/([^/?#]*).*', url)[0] or ''
        word = urllib.parse.unquote(qword)
        return word, qword