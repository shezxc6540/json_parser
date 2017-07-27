#!/usr/bin/env python
# -*- coding: utf-8 -*-


class JsonError(Exception):
    """自定义异常的基类"""
    def __init__(self):
        pass


class ParserError(JsonError):
    """自定义异常类。

    在解析Json字符串遇到错误时抛出该异常"""
    def __init__(self, error_type):
        self.error_type = error_type


class DumpError(JsonError):
    def __init__(self):
        pass
