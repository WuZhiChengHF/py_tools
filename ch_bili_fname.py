#!/usr/bin/env python
#coding: utf-8
import os,sys,re

import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])


def ch_name():
    rest = os.popen("ls .").read()
    rest = rest.replace("\r", "").replace("\n\n", "\n")
    olist = rest.split("\n")
    name = re.sub("(【|】)", "", rest.replace(" ", ""))
    name = re.sub(".*?\(P", "P", name)
    nlist = name.split("\n")
    for i, v in enumerate(nlist):
        if re.match(r"P[0-9]{1}\.", v):
            nname = "P0" + v[1:]
            nlist[i] = nname.replace(")", "")
    for o, n in zip(olist, nlist):
        o = o.replace("\n", "")
        n = n.replace("\n", "")
        if o != n:
            cmd = "move \"{}\" \"{}\"".format(str(o), str(n))
            print("cmd: " + cmd)
            os.popen(cmd)
    #print("\n".join(nlist))

if __name__ == "__main__":
    ch_name()
