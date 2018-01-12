#!/usr/bin/env python

import random
import time

while True:
    a = random.randint(1, 64)
    b = random.randint(1, 64)
    print '%d * %d = %d' % (a, b, a * b)
    d = random.random() * 3.0
    time.sleep(d)
