#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import ast
import copy

class PythonNodeDecorator(ast.NodeVisitor):
    def generic_visit(self,node):
        try:
            max_line=node.lineno
        except:
            max_line=0
        super(PythonNodeDecorator,self).generic_visit(node)
        try:
            for fieldname, value in ast.iter_fields(node):
                try:
                    if type(value)!=list:
                        max_line=max(max_line,value.line_end)
                    else:
                        for x in value:
                            max_line=max(max_line,x.line_end)
                except:
                    pass
        except:
            pass
        node.line_end=max_line
        
        

class PythonNodeVisitor(ast.NodeVisitor):
    def __init__(self,pattern,result_dict):
        self.pattern=pattern
        self.result_dict=result_dict
        self.results=[]
        super(PythonNodeVisitor,self).__init__()

    def process(self,node):
        PythonNodeDecorator().visit(node)
        self.visit(node)
    
    def feed_pattern(self,node,pattern_type):
        for x in self.pattern.node_enter(pattern_type,self.result_dict,name=node.name,
                                         line_start=node.lineno,line_end=node.line_end,
                                         num_lines=node.line_end-node.lineno+1):
            self.results.append(x)
        self.generic_visit(node)
        self.pattern.node_exit(pattern_type,self.result_dict,name=node.name)        
        
    def visit_ClassDef(self, node):
        self.feed_pattern(node,'python_class')

    def visit_FunctionDef(self, node):
        self.feed_pattern(node,'python_function')

class BaseConstructorMixin(object):
    def setUp(self):
        pass

class KwConstructorMixin(BaseConstructorMixin):
    def __init__(self,**kwargs):
        for k in kwargs:
            setattr(self,k,kwargs[k])
        self.setUp()
class ArgsConstructorMixin(BaseConstructorMixin):
    def __init__(self,*args):
        self.args=[]
        for a in args:
            self.args.append(a)
        self.setUp()

class Query(KwConstructorMixin):
    def get_results(self):
        self.result_dict={}
        for root,dirs,files in os.walk(self.start):
            for f in files:
                if f.endswith('.py'):
                    for result in self.process_python_file(root,f):
                        yield result
        return
        yield
    
    def process_python_file(self,relative_dir,file_name):
        file_content=open(os.path.join(relative_dir,file_name),'r').read()
        for result in self.pattern.node_enter('python_file',self.result_dict,
                                              file_content=file_content,
                                              name=file_name,
                                              relative_dir=relative_dir):
            yield result
        tree=ast.parse(file_content)
        visitor=PythonNodeVisitor(self.pattern,self.result_dict)
        visitor.process(tree)
        for r in visitor.results: 
            yield r
        self.pattern.node_exit('python_file',self.result_dict,file_content=file_content)
        return
        yield
        

class PyFile(KwConstructorMixin):
    def node_enter(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_file':
            result_dict[self.var]={'name':kwargs['name'],
                                   'relative_dir':kwargs['relative_dir'],
                                   'num_lines':len(kwargs['file_content'].split('\n'))
                                  }
            yield copy.copy(result_dict)
        return
        yield
    def node_exit(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_file':
            del result_dict[self.var]

class PyClass(KwConstructorMixin):
    def node_enter(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_class':
            result_dict[self.var]={'name':kwargs['name'],
                                   'line_start':kwargs['line_start'],
                                   'line_end':kwargs['line_end'],
                                   'num_lines':kwargs['num_lines']
                                  }
            yield copy.copy(result_dict)
        return
        yield
    def node_exit(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_class':
            del result_dict[self.var]

class PyFunction(KwConstructorMixin):
    def node_enter(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_function':
            result_dict[self.var]={'name':kwargs['name'],
                                   'line_start':kwargs['line_start'],
                                   'line_end':kwargs['line_end'],
                                   'num_lines':kwargs['num_lines']
                                  }
            yield copy.copy(result_dict)
        return
        yield
    def node_exit(self,pattern_type,result_dict,*args,**kwargs):
        if pattern_type=='python_function':
            del result_dict[self.var]

class And(ArgsConstructorMixin):
    pass

class PyString(KwConstructorMixin):
    pass

class Stack(ArgsConstructorMixin):
    def setUp(self):
        self.level=0
    def node_enter(self,pattern_type,result_dict,*args,**kwargs):
        yielded=False
        if self.level<len(self.args):
            for result in self.args[self.level].node_enter(pattern_type,result_dict,*args,**kwargs):
                yielded=True
                yield result
            if yielded:
                self.level+=1
        return 
        yield
    def node_exit(self,pattern_type,result_dict,*args,**kwargs):
        pass