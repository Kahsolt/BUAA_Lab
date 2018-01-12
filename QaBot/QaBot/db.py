#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3

from QaBot.settings import *


# [本地数据库]
#   缓存的用户信息和问答数据


def update_users(users):
    try:
        for u in users:
            sql = 'INSERT OR REPLACE INTO User(id, username, nickname, time) VALUES("%s", "%s", "%s", "%s");' % (u.id, u.name, u.nick, u.joined_at)
            query(sql)
        db.commit()
        print('[DB] User info updated! :)')
    except:
        print('[DB] Failed to update user info!! :(')


def add_question(user, quest, kws):
    qid = None
    try:
        sql = 'INSERT INTO Question(uid, content) VALUES("%s", "%s");' % (user, quest)
        query(sql)
        sql = 'SELECT id FROM Question WHERE uid="%s" AND content="%s";' % (user, quest)
        qid=query(sql)[0][0]  # [(1,)] tuple => row0(column0,)
        for kw in kws:
            sql = 'SELECT id FROM KeyWord WHERE name="%s";' % (kw)
            data = query(sql)
            if len(data) == 0:
                sql = 'INSERT INTO KeyWord(name) VALUES("%s");' % (kw)
                query(sql)
            sql = 'SELECT id FROM KeyWord WHERE name="%s";' % (kw)
            kwid = query(sql)[0][0]
            sql = 'INSERT OR REPLACE INTO Question_KeyWord(qid, kwid) VALUES("%s", "%s");' % (qid, kwid)
            query(sql)
        db.commit()
        print('[DB] New question record added, keywords updated! :)')
    except:
        print('[DB] Failed to add a question record or keyword!! :(')

    return qid


def add_answer(user, quest, ans):
    try:
        sql = 'INSERT INTO Answer(uid, qid, content) VALUES("%s", "%s", "%s");' % (user, quest, ans)
        query(sql)
        sql = 'SELECT id FROM Answer WHERE uid="%s" AND qid="%s" AND content="%s";' % (user, quest, ans)
        query(sql)
        db.commit()
        print('[DB] New answer record added! :)')
    except:
        print('[DB] Failed to add a answer record!! :(')


def find_answers(kws):
    if len(kws)==0:
        return None

    anss = None
    try:
        sql_where = 'WHERE'
        for i in range(len(kws)):
            sql_where += ' KeyWord.name LIKE "%%%s%%" ' % kws[i]
            if i != len(kws)-1:
                sql_where += 'OR'

        sql = 'SELECT DISTINCT Answer.content FROM KeyWord JOIN Question_KeyWord ON KeyWord.id=Question_KeyWord.kwid JOIN Question ON Question_KeyWord.qid=Question.id JOIN Answer ON Question.id=Answer.qid %s;' % sql_where
        anss = query(sql)
        db.commit()
        print('[DB] Nice re-discovery! :)')
    except:
        print('[DB] Failed to retrieve answers from db!! :(')

    return [t[0] for t in anss]


# Auxiliary Function
def init():
    if os.path.isfile(DB_DATA_FILE):
        db = sqlite3.connect(DB_DATA_FILE)
    else:
        print('[DB] Fresh setup, creating our local db first! :D')
        db = sqlite3.connect(DB_DATA_FILE)
        sql_bulk = open(DB_SCHEMA_FILE, 'r').read()
        db.executescript(sql_bulk)
        db.commit()
    if not db:
        print('[DB] Error init DB... X(')
        sys.exit(-1)
    return db


def query(sql):
    cur = db.cursor()
    print('/DB/ Execute "%s"' % sql)
    data = cur.execute(sql).fetchall()
    cur.close()
    print('\\DB\\ DataSet "%s"...' % data[:10])
    return data


db=init()

if __name__ == '__main__':
    print('List Users')
    sql = 'SELECT * FROM User;'
    for i in db.execute(sql).fetchall():
        print(i)
    print('=======')

    print('Add Question')
    qid = add_question(None, '喜马拉雅山的海拔是多少', ['喜马拉雅', '海拔'])
    sql = 'SELECT * FROM Question;'
    for i in db.execute(sql).fetchall():
        print(i)
    print('List Questions')
    sql = 'SELECT * FROM KeyWord;'
    for i in db.execute(sql).fetchall():
        print(i)
    print('=======')

    print('Add Answer')
    add_answer(None, qid, '8848.44米')
    add_answer(None, qid, '-2333米')
    print('List Answers')
    sql = 'SELECT * FROM Answer;'
    for i in db.execute(sql).fetchall():
        print(i)
    print('=======')

    print('Find Answers')
    anss = find_answers(['阿尔卑斯', '海拔'])
    print(anss)
    print('=======')