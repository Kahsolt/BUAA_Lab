#!/usr/bin/env python3

import requests
import socket
import jieba.posseg

from QaBot.settings import *
from QaBot import db


# [AI模块] 纯查询
#   1. 单纯向某个API问问题，比如QA-Snake
#   2. 查询本地缓存的数据库


# Ask Internet !
def search(quest):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(60)
        client.connect((QASNAKE_HOST, QASNAKE_PORT))
        client.send(quest.encode('utf8'))
        ans = client.recv(4096).decode('utf8')
        return ans
    except:
        print('[AI] QA-snake died? Then try the foolish turing bot... :O')

        url = 'http://www.tuling123.com/openapi/api'
        params = {
            'key': "0ef225fd449a4958b0b587e4523f002e",
            'userid': "123",
            'info': quest,
        }
        try:
            req = requests.get(url=url, params=params).json()
            return req.get('text')
        except:
            print('[AI] Network traffic too heavy? :(')
            return None


# Ask Local DB!
def query(quest):
    segSensible = get_keywords(quest)
    print('[Seg] %s' % ' '.join(segSensible))
    anss = db.find_answers(segSensible)
    return '\n'.join(anss)


# Auxciliary function
def get_keywords(quest):
    segs = [list(pair) for pair in jieba.posseg.lcut(quest)]
    segSensible = []
    for w in segs:
        if w[1] in TAG_JIEBA_SENSIBLE:
            segSensible.append(w[0])
    return segSensible


def get_QA_likeness(quest, ans):
    kwQ = get_keywords(quest)
    kwA = get_keywords(ans)
    count = 0
    for kw in kwA:
        if kw in kwQ:
            count+=1
    return float(count)/len(kwQ)


if __name__ == '__main__':
    print(search('巴士底狱'))
    print(search('北京海淀明天的天气'))
    print(search('你的名字'))
    print(search('少林寺方丈'))
    print(search('乞力马扎罗山的海拔'))