#!/usr/bin/env python3

import sys, os
QABOT_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(QABOT_BASE)


# Discord
DISCORD_TOKEN = 'MzQ5Mzc0NTY5Mjg4Njk1ODI4.DIqAlw.r4MqVqjp3iMMDoNInaCKSbA4QHc'

# QA-Snake
QASNAKE_HOST = '127.0.0.1'
QASNAKE_PORT = 50000

# Local DB
DB_DATA_FILE = os.path.join(QABOT_BASE, 'sqlite3.db')
DB_SCHEMA_FILE = os.path.join(QABOT_BASE, 'init.sql')

QUESTION_ALIKENESS = 0.8
ANSWER_ALIKENESS = 0.5

# NLP Metainfo Databases
TAG_JIEBA = {
    'a': '形容词', 'Ag': '形语素', 'ad': '副形词', 'an': '名形词', 'b': '区别词',
    'c': '连词', 'dg': '副语素', 'd': '副词', 'e': '叹词', 'f': '方位词',
    'g': '语素', 'h': '前接成分', 'i': '成语', 'j': '简称略语', 'k': '后接成分',
    'l': '习用语', 'm': '数词', 'Ng': '名语素', 'n': '名词', 'nr': '人名',
    'ns': '地名', 'nt': '机构团体', 'nz': '其他专名', 'o': '拟声词', 'p': '介词',
    'q': '量词', 'r': '代词', 's': '处所词', 'tg': '时语素', 't': '时间词',
    'u': '助词', 'vg': '动语素', 'v': '动词', 'vd': '副动词', 'vn': '名动词',
    'w': '标点符号', 'x': '非语素字', 'y': '语气词', 'z': '状态词', 'un': '未知词',
}
TAG_JIEBA_SENSIBLE = [
    'j', 'l',
    'an', 'Ng', 'n', 'nr', 'ns', 'nt', 'nz',
    'vn', 'v',
]