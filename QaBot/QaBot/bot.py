#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
import asyncio

from QaBot.settings import *
from QaBot import AI, db

HELP = 'QaBot的正确用法：\n' \
       '  提问请前缀问号?，例如：？南京市长是谁\n' \
       '  回答请前缀感叹号!，例如：！江大桥\n' \
       '  反馈请给出yes/no\n'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as [%s]: <%s>' % (client.user.name, client.user.id))
    print('=======')
    db.update_users(client.get_all_members())


@client.event
async def on_message(message):
    if message.content in ['?', '？']:
        await client.send_message(message.channel, HELP)

    elif message.content.startswith('?') or message.content.startswith('？'):
        # Alias
        ask = message
        quest = ask.content[1:].strip()
        print('[Quest] %s<%s> asking about "%s"' % (ask.author.name, ask.author.id, quest))
        tmp = await client.send_message(message.channel, '好问题，(⊙v⊙)容我三思...')

        # [1] Dispatch AI-DB
        ansDB = AI.query(quest) or ''
        print('[Ans] Answer by AI-DB "%s..."' % ansDB[:20])
        if len(ansDB) > 0:
            await client.edit_message(tmp, ansDB)
        else:
            # <Q> Add question to local db
            qid = db.add_question(ask.author.id, quest, AI.get_keywords(quest))

            # [2] Dispatch AI-SE
            ansSE = AI.search(quest) or ''
            print('[Ans] Answer by AI-SE "%s..."' % ansSE[:20])
            if AI.get_QA_likeness(quest ,ansSE) >= ANSWER_ALIKENESS:
                reans = '%s\n（这个答案不知客官是否满意 yes/no :D）' % ansSE
                await client.edit_message(tmp, reans)

                feedback = await client.wait_for_message(author=ask.author, timeout=30)
                if feedback:
                    # <A> Cache SE-answer to local db
                    if feedback.content.upper() != 'NO':
                        db.add_answer(feedback.author.id, qid, ansSE)
                    await client.send_message(ask.channel, '感谢您的反馈 :)')

            else:
                # [3] Dispatch CI
                request = '[%s] 遇到了一个问题："%s"，大家能帮忙解答一下吗？ :)' % (ask.author.name, quest)
                await client.send_message(ask.channel, request)

                # TODO: for i in range(1):  # Collect N answers?
                reply = await client.wait_for_message(author=ask.author, check=lambda msg:(msg.content.startswith('!') or msg.content.startswith('！')))
                ansCI = reply.content[1:].strip()
                print('[Ans] Answer by CI "%s..."' % ansCI[:20])
                reans = '来自[%s]的回答 "%s"\n（不知客官是否满意 yes/no :D)' % (reply.author.name, ansCI)
                await client.send_message(reply.channel, reans)

                feedback = await client.wait_for_message(author=reply.author, timeout=30)
                if feedback and feedback.content.upper() == 'YES':
                    # <A> Cache CI-answer to local db
                    db.add_answer(feedback.author.id, qid, ansCI)
                    await client.send_message(reply.channel, '感谢您的反馈 :)')

    elif message.content == '$':
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have sent {} messages.'.format(counter))

    elif message.content == '~':
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping :)')


client.run(DISCORD_TOKEN)
