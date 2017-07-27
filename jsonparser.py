#!/usr/bin/env python
# -*- coding: utf-8 -*-
from deepcopy_and_pre_fun import *
from subdump_fun import *
from subparser_fun import *


class JsonParser(object):
    """Json解析类。

    可用于Json字符串与Python字典的相互转换"""
    def __init__(self):
        self._data = dict()

    def loads(self, s):
        """读取JSON格式数据，输入s为一个JSON字符串，无返回值。

        若遇到JSON格式错误的应该抛出异常。为简便考虑，JSON的最外层假定只为Object"""
        # 预处理字符串中的空格
        s = remove_space(s)
        try:
            self._data, rest_s = parser_object(s)
            if rest_s != '':
                raise ParserError
        except ParserError as pe:
            print("Parser Error! Expecting: " + pe.error_type)

    def dumps(self):
        """将实例中的内容转成JSON格式返回。

        """
        try:
            return dump_object(self._data)
        except DumpError:
            print("Dump Error!")

    def load_file(self, f):
        """从文件中读取JSON格式数据，f为文件路径。

        Json解析时异常处理，文件操作失败抛出异常"""
        with open(f, "r") as read_json:
            json_str = read_json.read()
            self.loads(json_str)

    def dump_file(self, f):
        """将实例中的内容以JSON格式存入文件。

        文件若存在则覆盖，文件操作失败抛出异常"""
        with open(f, "w") as out1:
            out1.write(self.dumps())

    def load_dict(self, d):
        """从dict中读取数据，存入实例中，若遇到不是字符串的key则忽略。

        """
        self._data = dict()
        for k, v in d.iteritems():
            if isinstance(k, str):
                self._data[k] = deep_copy_value(v)

    def dump_dict(self):
        """返回一个字典，包含实例中的内容。

        """
        return deep_copy_dict(self._data)

    def __getitem__(self, key):
        """重写__getitem__方法。

        """
        return self._data[key]

    def __setitem__(self, key, value):
        """重写__setitem__方法。

        """
        try:
            if isinstance(key, str):
                self._data[key] = value
            else:
                raise DumpError
        except DumpError:
            print("Dump Error!")

    def update(self, d):
        """用字典d更新实例中的数据，类似于字典的update。

        """
        for k, v in d.iteritems():
            if isinstance(k, str):
                self._data[k] = deep_copy_value(v)
