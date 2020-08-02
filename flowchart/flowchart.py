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
    def __init__(self,
                 name  = None,
                 left  = None,
                 right = None,
                 down  = None,
                 kw    = False):
        self.name = name
        self.left = left
        self.right = right
        self.down = down
        self.kw = kw


class compile(object):
    def __init__(self, fk):
        self.content = None
        self.del_char = lambda x, c: re.sub(r" *\%s *" % str(c), c, x)
        self.stack = list()
        self.nodelist = list()
        with open(fk, 'r') as fd:
            self.content = fd.read()
        self._process_fk()
        self._parse_fk()

    def _get_kw(self, fstr):
        rest = re.search(r'^(while|if|else if|else)$', fstr, re.IGNORECASE)
        return rest.group() if rest else None

    @catch_error()
    def _process_fk(self):
        self.content = re.sub(r'^#.*', "", self.content)
        self.content = self.content.replace("\r", "").replace("\n", "")
        for c in ['(', ')', '{', '}']:
            self.content = self.del_char(self.content, c)

    @catch_error()
    def _parse_fk(self):
        segs = self.content.split("{") or []
        self.fk_segs = list()
        for fk in segs:
            self.fk_segs.extend(fk.split(";"))
        print(self.fk_segs)
        
    def _parse_fk_sg_node(self, nstr):
        node = fnode(name=nstr)
        if self.is_kw(nstr, "while"):
            node.kw = "while"
            self.stack.append(node)
        elif self.is_kw(nstr, "else if"):
            node.kw = "else if"
        elif self.is_kw(nstr, "if"):
            node.kw = "else"
        elif self.is_kw(nstr, "else"):
            node.kw = "else"

        self.nodelist.append(node)
        return node

        

if '__main__' == __name__:
    compile("./fct.fk")
