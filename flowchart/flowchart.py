#!/usr/bin/env python
import re
import requests as req
import graphviz as g


def catch_error(value=None):
    def _catch_error(func):
        def wrapper(*a, **k):
            try:
                return func(*a, **k)
            except Exception as e:
                print("=========%s error:%s========" % (func.__name__, str(e)))
                return None

        return wrapper

    return _catch_error


class fnode(object):
    def __init__(self, name=None, left=None, right=None, down=None):
        self.name = name
        self.left = left
        self.right = right
        self.down = down


class compile(object):
    def __init__(self, fk):
        self.content = None
        self.del_char = lambda x, c: re.sub(r" *\%s *" % str(c), c, x)
        with open(fk, 'r') as fd:
            self.content = fd.read()
        self._process_fk()

    @catch_error()
    def _process_fk(self):
        self.content = re.sub(r'^#.*', "", self.content)
        self.content = self.content.replace("\r", "").replace("\n", "")
        for c in ['(', ')', '{', '}']:
            self.content = self.del_char(self.content, c)


if '__main__' == __name__:
    compile("./fct.fk")
