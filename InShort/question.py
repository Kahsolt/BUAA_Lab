#!/usr/bin/env python3

import jieba.posseg
import thulac
# import genius
# import mmseg
# import scseg


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
TAG_JIEBA_NOUN = [
    'an', 'Ng', 'j', 'l', 'n', 'nr', 'ns', 'nt', 'nz', 'vn'
]
TAG_THULAC = {
    'n': '名词', 'np': '人名', 'ns': '地名', 'ni': '机构名', 'nz': '其它专名',
    'm': '数词', 'q': '量词', 'mq': '数量词', 't': '时间词', 'f': '方位词', 's': '处所词',
    'v': '动词', 'a': '形容词', 'd': '副词', 'h': '前接成分', 'k': '后接成分', 'i': '习语',
    'j': '简称', 'r': '代词', 'c': '连词', 'p': '介词', 'u': '助词', 'y': '语气助词',
    'e': '叹词', 'o': '拟声词', 'g': '语素', 'w': '标点', 'x': '其它',
}
TAG_THULAC_NOUN = [
    'n', 'np', 'ns', 'ni', 'nz', 'j', 'i'
]

def getKeyWords(quest):
    def getNouns(listWords, egine):
        listNoun = []
        if egine == 'thulac':
            for w in listWords:
                if w[1] in TAG_THULAC_NOUN:
                    listNoun.append(w[0])
        elif egine == 'jieba':
            for w in listWords:
                if w[1] in TAG_JIEBA_NOUN:
                    listNoun.append(w[0])
        return listNoun

    segThulac = thulac.thulac().cut(quest)
    segJieba = [list(pair) for pair in jieba.posseg.lcut(quest)]
    nounThulac = getNouns(segThulac, 'thulac')
    nounJieba = getNouns(segJieba, 'jieba')
    nounCommon = list(set(nounThulac).union(set(nounJieba)))
    return nounCommon


def test(words):
    print('==== jieba ====')
    print([list(pair) for pair in jieba.posseg.lcut(words)])

    print('==== thulac ====')
    print(thulac.thulac().cut(words))


if __name__ == '__main__':
    test("大运村的邮编是多少")
    test("北京海淀明天的天气怎么样")