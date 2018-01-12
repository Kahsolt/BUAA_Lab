#!/usr/bin/env python3
import pycurl, io
import urllib.parse
import re
import jieba.posseg
import random
import time

# Features and Control
CURL_DELAY = 1              # time to wait before curl (in seconds)
N_MISC_TRIAL = 150          # set 0 to disable this silly feature :(
ENABLE_STRICT = True        # restrict that results SUPPOSED contain words in the QUEST_AUX_VOC,
                            # and can NOT be too short
MIN_QUEST_SEG_LENGTH = 2    # this is NOT accurate, but just aid this engine to filter
MIN_QUEST_STR_LENGTH = 3

# Content Config
QUEST_FILE = open('Questions.txt', 'a+')
QUEST_AUX_VOC = [
    # General misc
    '么', '吗', '对吗', '可以吗'
    # What
    '什么', '什么东西', '什么是', '什么叫', '什么意思', '什么体验',
    '是什么', '用什么', '有什么', '叫什么'
    '啥是', '是啥', '啥东西',
    # Which/Who
    '哪个', '哪一个', '哪位', '谁', '哪个人',
    # Where
    '哪里', '在哪里'
    # When
    '什么时候', '何时', '几点',
    # How
    '怎么', '怎样', '如何', '有何',
    '怎么可以', '怎样可以', '如何可以',
    '怎么评价', '怎样可以', '如何评价',
    '怎么能', '怎么办', '该怎么', '怎样能', '如何能', '的办法', '咋办',
    # Why
    '为什么', '为什么会', '为何', '为何会', '的理由', '的原因', '原因呢'
]
QUEST_MISC_VOC = [
    '的', '一', '是', '了', '我', '不', '人', '在', '他', '有',
    '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
    '子', '中', '你', '说', '生', '国', '年', '着', '就', '那',
    '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
    '会', '家', '可', '下', '而', '过', '天', '去', '能', '对',
    '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
    '看', '起', '发', '当', '没', '成', '只', '如', '事', '把',
    '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
    '总', '从', '无', '情', '己', '面', '最', '女', '但', '现',
    '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
    '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分',
    '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
    '世', '什', '两', '次', '使', '身', '者', '被', '高', '已',
    '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
    '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定',
    '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
    '将', '月', '十', '实', '向', '声', '车', '全', '信', '重',
    '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
    '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水',
    '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
    '利', '海', '受', '听', '表', '德', '少', '克', '代', '员',
    '许', '棱', '先', '口', '由', '死', '安', '写', '性', '马',
    '光', '白', '或', '住', '难', '望', '教', '命', '花', '结',
    '乐', '色',
]

# Metainfo Databases
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
TAG_JIEBA_AUX = [
    'r'
]

# Runtime Databases
QUERY_HISTORY = []
QUEST_LIST = []
QUEST_QUEUE = []


def curl(url):
    try:
        s = io.BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.REFERER, url)
        c.setopt(pycurl.FOLLOWLOCATION, True)
        c.setopt(pycurl.TIMEOUT, 60)
        c.setopt(pycurl.ENCODING, 'gzip')
        c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0')
        c.setopt(pycurl.NOSIGNAL, True)
        c.setopt(pycurl.WRITEFUNCTION, s.write)
        c.perform()
        c.close()
        return s.getvalue().decode('gbk')
    except Exception as e:
        print(e)
        return None


def search(kw):
    global QUEST_QUEUE, QUEST_LIST, QUERY_HISTORY

    if kw in QUERY_HISTORY:
        print('[WARN] Duplicated searching for keyword "%s", dropping...' % (kw))
        return
    QUERY_HISTORY.append(kw)

    time.sleep(CURL_DELAY)
    print('[INFO] Searching keyword "%s"' % (kw))
    URL = 'http://suggestion.baidu.com/su?wd=%s' % (urllib.parse.quote(kw))
    resp = curl(URL)
    if not resp:
        print('[ERRO] Curl without response...')
        return

    quests = re.findall('window\.baidu\.sug.*s:\[(.*)\].*', resp)[0]
    if not quests:
        print('[INFO] Curl no data found in resp "%s"' % (resp))
        return
    quests = [i.strip('"') for i in quests.split(',')]

    print(quests)
    return quests


def sugSearch(auxKw):           # 构建init问题集的队列
    global QUEST_QUEUE, QUEST_LIST, QUERY_HISTORY

    quests = search(auxKw)        # 纯粹疑问助词搜索
    if not quests:
        print('[WARN] sugSearch-AuxKw has no question.')
        return
    for quest in quests:
        write(quest)
        QUEST_QUEUE.append(quest)

    if N_MISC_TRIAL > 0:          # 人工辅助词搜索
        extVoc = random.sample(QUEST_MISC_VOC, N_MISC_TRIAL)
        for ext in extVoc:
            extAuxKw = auxKw + ext
            quests = search(extAuxKw)
            if not quests:
                print('[WARN] sugSearch-ExtAuxKw has no question.')
                break
            for quest in quests:
                write(quest)
                QUEST_QUEUE.append(quest)


def sugExtend():                # 处理init问题集的任务队列，智障反馈性扩展搜索
    global QUEST_QUEUE, QUEST_LIST, QUERY_HISTORY
    def getSensible(listSegs):
        listNoun = []
        for w in listSegs:
            if w[1] in TAG_JIEBA_SENSIBLE:
                listNoun.append(w[0])
        return listNoun
    def getAux(listSegs):
        listAux = []
        for w in listSegs:
            if w[1] in TAG_JIEBA_AUX:
                listAux.append(w[0])
        return listAux

    while len(QUEST_QUEUE) > 0:
        Q = QUEST_QUEUE[0]
        QUEST_QUEUE = QUEST_QUEUE[1:]

        segs = [list(pair) for pair in jieba.posseg.lcut(Q)]
        segSensible = getSensible(segs)
        segAux = getAux(segs)
        for sensible in segSensible:
            for aux in segAux:
                segKw = aux + sensible
                quests = search(segKw)
                if not quests:
                    print('[WARN] sugExtend has no question.')
                    break
                for quest in quests:
                    write(quest)
                    QUEST_QUEUE.append(quest)


def write(quest):
    if quest not in QUEST_LIST and filter(quest):
        QUEST_LIST.append(quest)
        QUEST_FILE.write(quest)
        QUEST_FILE.write('\n')


def filter(quest):
    def countSeg(quest):
        return len([list(pair) for pair in jieba.posseg.lcut(quest)])
    def judgeRelation(quest):
        for aux in QUEST_AUX_VOC:
            if aux in quest:
                return True
        return False

    if ENABLE_STRICT:
        if not judgeRelation(quest):
            return False
        if countSeg(quest) < MIN_QUEST_SEG_LENGTH:
            return False
        if len(quest) < MIN_QUEST_STR_LENGTH:
            return False
        return True
    else:
        if judgeRelation(quest):
            return countSeg(quest) >= MIN_QUEST_SEG_LENGTH
        else:
            return countSeg(quest) > MIN_QUEST_SEG_LENGTH

def go():
    print('==== [[STAGE 1: sugSearch START]] ====')
    for i in QUEST_AUX_VOC:
        sugSearch(i)
    print('==== [[STAGE 1: sugSearch END]] ====')

    print('==== [[STAGE 2: sugExtend START]] ====')
    sugExtend()
    print('==== [[STAGE 2: sugExtend END]] ====')


########
# Entry
if __name__ == '__main__':
    go()