#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import ast

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
        for root,dirs,files in os.walk(self.start):
            for f in files:
                if f.endswith('.py'):
                    self.process_python_file(root,f)
        return []
    
    def process_python_file(self,root,file_name):
        file_content=open(os.path.join(root,file_name),'r').read()
        self.pattern.feed('python_file',file_content=file_content)
        tree=ast.parse(file_content)
        
        
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