#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import os
import json

FIN='person.ttl'
FOUT_FORMAT='LIST'         # 'LIST','JSON'

def parseResource(str):
    id=re.findall('<http://ics.swjtu.edu.cn/resource/(.*)>', str)[0]
    return id
def parseAttribute(str):
    attr=re.findall('<http://ics.swjtu.edu.cn/rdfs/people/person/(.*)>', str)[0]
    return attr
def parseValue(str):
    val=re.findall('<http://ics.swjtu.edu.cn/datatype/.*@(.*)>', str)[0]
    return val

def read(fin):
    ferr=open(os.path.splitext(FIN)[0]+'.err', 'w+')
    dic={}
    for line in fin.readlines():
        l=line.strip('\r\n\t\0 .').split('\t')
        try:
            id=parseResource(l[0])
            k,v=parseAttribute(l[1]),parseValue(l[2])
            if id in dic.keys():
                dic[id][k]=v
            else:
                dic[id]={k:v}
        except:
            ferr.write("%s\n"%(line))
            print('Bad Line: %s'%(line))
    return dic

def write(dic, FORMAT='READ'):
    if FORMAT=='LIST':
        fout=open(os.path.splitext(FIN)[0]+'.list', 'w+')
        for id in dic.keys():
            attrval=dic[id]
            fout.write("%s\n" %(id))
            for a in attrval.keys():
                fout.write("\t%s\t%s\n" %(a, attrval[a]))
            fout.write('\n')

    elif FORMAT=='JSON':
        fout=open(os.path.splitext(FIN)[0]+'.json', 'w+')
        fout.write(json.dumps(dic, ensure_ascii=False))

########
# Entry
write(read(open(FIN, 'r')), FOUT_FORMAT)
