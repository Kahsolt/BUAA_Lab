from question import getKeyWords
from query import goWeb

Q = '大运村的邮编是多少'

kw = getKeyWords(Q)
print(kw)

goWeb(kw)
