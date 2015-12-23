#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import MagicMock as mm
from astql import Query,PyFile,PyClass,PyFunction,And,PyString,Stack

class TestQueryBasic(TestCase):
    def testPyFile(self):
        pattern=PyFile(var='pyfile')
        query=Query(start='tests/examples/example1',
                    pattern=pattern)
        self.assertEqual(query.start,'tests/examples/example1')
        self.assertEqual(query.pattern,pattern)
        results=[x for x in query.get_results()]
        r=results[0]
        self.assertEqual(r['pyfile']['name'],'example1.py')
        self.assertEqual(r['pyfile']['relative_dir'],'tests/examples/example1')
        self.assertEqual(r['pyfile']['num_lines'],5)

    def testPyClass(self):
        pattern=PyClass(var='c1')
        query=Query(start='tests/examples/example1',
                    pattern=pattern)
        self.assertEqual(query.start,'tests/examples/example1')
        self.assertEqual(query.pattern,pattern)
        results=[x for x in query.get_results()]
        r=results[0]
        self.assertEqual(r['c1']['name'],'Class1')
        self.assertEqual(r['c1']['line_start'],1)
        self.assertEqual(r['c1']['line_end'],4)
        self.assertEqual(r['c1']['num_lines'],4)
        
    def testPyFunction(self):
        pattern=PyFunction(var='f')
        query=Query(start='tests/examples/example1',
                    pattern=pattern)
        self.assertEqual(query.start,'tests/examples/example1')
        self.assertEqual(query.pattern,pattern)
        results=[x for x in query.get_results()]
        r=results[0]
        self.assertEqual(r['f']['name'],'m1')
        self.assertEqual(r['f']['line_start'],2)
        self.assertEqual(r['f']['line_end'],4)
        self.assertEqual(r['f']['num_lines'],3)
    def testPyString(self):
        pattern=PyString(var='s')
        query=Query(start='tests/examples/example1',
                    pattern=pattern)
        self.assertEqual(query.start,'tests/examples/example1')
        self.assertEqual(query.pattern,pattern)
        results=[x for x in query.get_results()]
        r=results[0]
        self.assertEqual(r['s']['content'],'inv.agreement')
        self.assertEqual(r['s']['line_start'],3)
        self.assertEqual(r['s']['line_end'],3)
        self.assertEqual(r['s']['num_lines'],1)
        r=results[1]
        self.assertEqual(r['s']['content'],'invoice_date')
        self.assertEqual(r['s']['line_start'],4)
        self.assertEqual(r['s']['line_end'],4)
        self.assertEqual(r['s']['num_lines'],1) 
        
    def testStack(self):
        pattern=Stack(PyFile(var='pyfile'),
                      PyClass(var='cl'),
                      PyFunction(var='m'),
                      And(PyString(var='str1',content='inv.agreement'),
                          PyString(var='str2',content='invoice_date')))
        query=Query(start='tests/examples/example1',
                    pattern=pattern)
        self.assertEqual(query.start,'tests/examples/example1')
        self.assertEqual(query.pattern,pattern)
        results=[x for x in query.get_results()]
        r=results[0]
        self.assertEqual(r.pyfile.name,'example1.py')
        self.assertEqual(r.pyfile.relative_dir,'tests/examples/example1')
        self.assertEqual(r.pyfile.num_lines,5)
        self.assertEqual(r.cl.name,'Class1')
        self.assertEqual(r.cl.line_start,1)
        self.assertEqual(r.cl.line_end,4)
        self.assertEqual(r.cl.num_lines,4)
        self.assertEqual(r.m.name,'m1')
        self.assertEqual(r.m.line_start,2)
        self.assertEqual(r.m.line_end,4)
        self.assertEqual(r.m.num_lines,3)
        self.assertEqual(r.str1.content,'inv.agreement') 
        self.assertEqual(r.str2.content,'invoice_date')               