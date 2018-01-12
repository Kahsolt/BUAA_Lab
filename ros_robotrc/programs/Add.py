#!/usr/bin/env python

import random
import time

while True:
    a = random.randint(1, 1024)
    b = random.randint(1, 1024)
    print '%d + %d = %d' % (a, b, a + b)
    d = random.random() * 3.0
    time.sleep(d)
