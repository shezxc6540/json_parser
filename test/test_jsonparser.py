#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from jsonparser import JsonParser
from deepcopy_and_pre_fun import *
from subdump_fun import *
from subparser_fun import *


class JsonParserTest(unittest.TestCase):
    def test_remove_space(self):
        ori = '{  "a ": 1, "":2 ,"3" : "\u1234" ,"4":["k","k1 "] }'
        tar = '{"a ":1,"":2,"3":"\u1234","4":["k","k1 "]}'
        self.assertEqual(remove_space(ori), tar)

    def test_parser_string(self):
        ori = '"1234","4":["k","k1 '
        a, b = parser_string(ori)
        tar_a = '1234'
        tar_b = ',"4":["k","k1 '
        self.assertEqual(a, tar_a)
        self.assertEqual(b, tar_b)

    def test_parser_value(self):
        ori1 = '[[2,-3],4,7,20e1,3.14],'
        ori2 = '{"a":2},'
        ori3 = 'null,'
        ori4 = 'trueh'
        ori5 = 'falsee'
        tar11 = [[2, -3], 4, 7, 20e1, 3.14]
        tar21 = {"a": 2}
        a1, b1 = parser_value(ori1)
        a2, b2 = parser_value(ori2)
        a3, b3 = parser_value(ori3)
        a4, b4 = parser_value(ori4)
        a5, b5 = parser_value(ori5)
        self.assertEqual(tar11, a1)
        self.assertEqual(tar21, a2)
        self.assertIsNone(a3)
        self.assertTrue(a4)
        self.assertFalse(a5)
        self.assertEqual(',', b1)
        self.assertEqual(',', b2)
        self.assertEqual(',', b3)
        self.assertEqual('h', b4)
        self.assertEqual('e', b5)

    def test_parser_number(self):
        ori = '-123.01E+1'
        res = parser_number(ori)
        self.assertEqual(res, -123.01E1)

    def test_dump_value(self):
        a = dict()
        a['\\\b\f\"abcd'] = [-12, 30, True, False, None]
        res = dump_value(a)
        tar = r'{"\\\b\f\"abcd": [-12, 30, true, false, null]}'
        self.assertEqual(res, tar)

    def test_deep_copy(self):
        a = [1, {"a": True}, None]
        b = deep_copy_list(a)
        self.assertEqual(a, b)
        self.assertIsNot(a, b)

    def test_main_function(self):
        json_ok = [
            ('{}', 1),
            ('{"":""}', 1),
            ('{"a":123}', 1),
            ('{"a":-123}', 1),
            ('{"a":1.23}', 1),
            ('{"a":1e1}', 1),
            ('{"a":true,"b":false}', 1),
            ('{"a":null}', 1),
            ('{"a":[]}', 1),
            ('{"a":{}}', 1),
            (' {"a:": 123}', 1),
            ('{ "a  " : 123}', 1),
            ('{ "a" : 123    	}', 1),
            ('{"true": "null"}', 1),
            ('{"":"\\t\\n"}', 1),
            ('{"\\"":"\\""}', 1),
            ]

        json_ok2 = [
            ('{"a":"abcde,:-+{}[]"}', 2),
            ('{"a": [1,2,"abc"]}', 2),
            ('{"d{": "}dd", "a":123}', 2),
            ('{"a": {"a": {"a": 123}}}', 2),
            ('{"a": {"a": {"a": [1,2,[3]]}}}', 2),
            ('{"a": "\\u7f51\\u6613CC\\"\'"}', 3),

            ('{"a":1e-1, "cc": -123.4}', 2),
            ('{ "{ab" : "}123", "\\\\a[": "]\\\\"}', 3),
            ]

        json_ex = [
            # exceptions
            ('{"a":[}', 2),
            ('{"a":"}', 2),
            ('{"a":True}', 1),
            ('{"a":Null}', 1),
            ('{"a":foobar}', 2),
            ("{'a':1}", 3),
            ('{1:1}', 2),
            ('{true:1}', 2),
            ('{"a":{}', 2),
            ('{"a":-}', 1),
            ('{"a":[,]}', 2),
            ('{"a":.1}', 1),
            ('{"a":+123}', 1),
            ('{"a":1..1}', 1),
            ('{"a":--1}', 1),
            ('{"a":"""}', 1),
            ('{"a":"\\"}', 1),
        ]
        for js in json_ok + json_ok2:
            js_str = js[0]
            jp = JsonParser()
            jp.loads(js_str)  # jp has a new dict
            # new dict transfers to js_str, it equals to the text after handling whitespaces
            js_str = jp.dumps()
            jp_dict1 = jp.dump_dict()

            jp.dump_file('output.txt')
            jp.loads(js_str)   # a new dict from js_str
            jp_dict2 = jp.dump_dict()
            self.assertDictEqual(jp_dict1, jp_dict2)

            jp.load_file('output.txt')
            jp_dict3 = jp.dump_dict()
            self.assertDictEqual(jp_dict2, jp_dict3)
        for js in json_ex:
            js_str = js[0]
            jp = JsonParser()
            jp.loads(js_str)

        jp1 = JsonParser()
        jp1.load_file("test1.txt")
        jp_dict4 = jp1.dump_dict()
        self.assertEqual(jp1['a'], 1)
        jp1.update(jp_dict4)

if __name__ == '__main__':
    unittest.main()
