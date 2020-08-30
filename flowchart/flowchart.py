#!/usr/bin/env python
import re
import requests as req
import graphviz as g
import random as rd


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
    def __init__(self, name=None, 
            left=None, right=None, 
            down=None, up=None, kw=False):
        self.name = name
        self.left = left
        self.right = right
        self.down = down
        self.up = up
        self._kw = kw

    @property
    def kw(self):
        return self._kw

    @kw.setter
    def kw(self, value):
        self._kw = value

    def __str__(self):
        return " --> ".join([
            str(i)
            for i in [self.name, self.left, self.right, 
                self.up, self.down, self._kw]
        ])


class block(object):
    def __init__(self, inn, nodes=None, sblock=None):
        self.inn = inn
        self.out = None
        self.nodes = nodes
        self.sub_block = None
        self.rdint = lambda x=10000: rd.randint(1, x)

    def _connect_single_block_nodes(self, aw_in, node):
        node.up = aw_in
        node.down = self.rdint()
        return node.down + 1

    def _connect_block_nodes(self, aw_in, nodes=None):
        start, end, aw_in = 0, 0, 0
        if nodes is None: nodes = self.nodes

        # process while
        # process if else

        for i, node in enumerate(nodes):

            if node.kw:
                end = self._calc_blk_pair(self, start)
                aw_in = self._connect_block_nodes(aw_in, nodes[i, end])
            else:
                aw_in = self._connect_single_block_nodes(aw_in, nodes[i])

            if start > 0: start = end + 1

        return aw_in


class compile(object):
    def __init__(self, fk):
        self.content = None
        self.del_char = lambda x, c: re.sub(r" *\%s *" % str(c), c, x)
        self.stack = list()
        self.nodelist = list()
        with open(fk, 'r') as fd:
            self.content = fd.read()
        self._process_fk()

    def _calc_blk_pair(self, start):
        left_brackets = 0
        right_brackets = 0
        for i, node in enumerate(self.nodelist):
            if i < start: continue
            if node.name.find("{") >=0: left_brackets += 1
            elif node.name.find("}") >=0: right_brackets += 1
            if left_brackets == right_brackets and left_brackets >0:
                return i
        raise Exception("node: %s can not get pair node" % str(self.nodelist[start]))

    def _connect_node(self):
        start_node = fnode("start")
        end_node = fnode("end")
        start_node.down = 0
        b = block(0, *self.nodelist)
        out = b.connect_block_nodes()
        end_node.up = out

        #start, end, aw_in = 0, 0, 0
        #for i, node in enumerate(self.nodelist):

        #    if node.kw:
        #        end = self._calc_blk_pair(self, start)
        #        b = block(aw_in, self.nodelist[i, end])
        #    else:
        #        b = block(aw_in, [self.nodelist[i]])

        #    aw_in = b.connect_block_nodes()
        #    if start > 0: start = end + 1

        print("*"*20)
        for i, node in enumerate(self.stack):
            print(i, str(node))

    def _get_kw(self, fstr):
        rest = re.search(r'(while|if|else if|else)', fstr, re.IGNORECASE)
        return rest and rest.group() or None

    @catch_error()
    def _process_fk(self):
        self.content = re.sub(r'^#.*', "", self.content)
        self.content = self.content.replace("\r", "").replace("\n", "")
        for c in ['(', ')', '{', '}']:
            self.content = self.del_char(self.content, c)
        self._parse_fk()
        self._connect_node()

    @catch_error()
    def _parse_fk(self):
        segs = self.content.split("{") or []
        self.fk_segs = list()

        for fk in segs:
            self.fk_segs.extend(fk.split(";"))

        for i in self.fk_segs:
            self._parse_fk_sg_node(i)

    def _parse_fk_sg_node(self, nstr):

        tstr = ""
        for i, s in enumerate(nstr):
            tstr += (("" if i==0 else ",") + s + \
                ("" if (i==len(nstr)-1) else ",")) if s=="}" else s

        for i in tstr.split(","):

            if not i:continue

            node = fnode(name=i)
            node.kw = self._get_kw(i)

            if node.kw: 
                node.name += "{"
                self.stack.append(node)

            self.nodelist.append(node)


if '__main__' == __name__:
    compile("./fct.fk")
