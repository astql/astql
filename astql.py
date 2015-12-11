#!/usr/bin/env python
# -*- coding: utf-8 -*-

class KwConstructorMixin(object):
    def __init__(self,**kwargs):
        for k in kwargs:
            setattr(self,k,kwargs[k])
class ArgsConstructorMixin(object):
    def __init__(self,*args):
        self.args=[]
        for a in args:
            self.args.append(a)

class Query(KwConstructorMixin):
    def get_results(self):
        return []

class PyFile(KwConstructorMixin):
    pass

class PyClass(KwConstructorMixin):
    pass

class PyMethod(KwConstructorMixin):
    pass

class And(ArgsConstructorMixin):
    pass

class PyString(KwConstructorMixin):
    pass

class Stack(ArgsConstructorMixin):
    pass