# -*- coding: UTF-8 -*-

# Filename : test.py
# author by : www.runoob.com


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
if __name__ == "__main__":
    print(is_number('foo'))   # False
    print(is_number('1'))     # True
    print(is_number('1.3'))   # True
    print(is_number('-1.37')) # True
    print(is_number('-1'))
    print(is_number('1e3'))   # True
    print(is_number('四')) # False
