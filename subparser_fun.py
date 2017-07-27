#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonerror import ParserError
LEGAL_DIGIT = '0123456789eE+-.'
ESCAPE_DIR_PARSER = {'t': '\t', 'r': '\r', 'n': '\n', 'f': '\f', 'b': '\b',
                     '/': '/', '"': '"', '\\': '\\'}


def parser_string(s):
    """解析Json字符串中的string形式。

    返回为Python中的str类型，出现不是预期的情况时，则抛出异常。"""
    if s[0] != '"':
        raise ParserError('string')
    temp_index = 1
    new_s = ''
    while temp_index < len(s) and s[temp_index] != '"':
        # 出现反斜杠，说明有转义符或unicode
        if s[temp_index] == '\\':
            # 看下一个字符是什么
            temp_index += 1
            if temp_index == len(s):
                raise ParserError('string')
            if s[temp_index] in ESCAPE_DIR_PARSER:
                new_s += ESCAPE_DIR_PARSER[s[temp_index]]
            elif s[temp_index] == 'u':
                if (temp_index + 4) < len(s):
                    try:
                        new_s += s[temp_index - 1:temp_index + 5].decode('raw_unicode_escape')
                        temp_index += 4
                    except ValueError:
                        raise ParserError('string')
                else:
                    raise ParserError('string')
            else:
                raise ParserError('string')
        else:
            new_s += s[temp_index]
        temp_index += 1
    if temp_index == len(s):
        raise ParserError('string')
    else:
        return unicode(new_s), s[temp_index + 1:]


def parser_value(s):
    """解析Json字符串中的value类型。

    value类型包括string类型，object类型，array类型， number类型， 以及特殊的
    null，true，false，进行分支判断。"""

    # 第一个字符为{，认为是object
    if s[0] == '{':
        return parser_object(s)
    # 第一个字符为[，认为是array
    elif s[0] == '[':
        return parser_array(s)
    # 第一个字符为"，认为是string
    elif s[0] == '"':
        return parser_string(s)
    # 第一个字符为t，认为是true
    elif s.startswith('true'):
        return True, s[4:]
    # 第一个字符为f，认为是false
    elif s.startswith('false'):
        return False, s[5:]
    elif s.startswith('null'):
        return None, s[4:]
    # 第一个字符为数字或者是负号时，认为是number
    elif ('0' <= s[0] <= '9') or s[0] == '-':
        temp_index = 1
        while temp_index < len(s) and s[temp_index] in LEGAL_DIGIT:
            temp_index += 1
        if temp_index == len(s):
            raise ParserError('number')
        else:
            return parser_number(s[0:temp_index]), s[temp_index:]
    else:
        raise ParserError('value')


def parser_number(s):
    """解析Json字符串中的number类型

    利用int()和float()函数和try/except语法来判断是否出错和解析字符串。"""
    if s[0] == '0' and len(s) > 1 and s[1] != '.':
        raise ParserError('number')
    try:
        # 此处如果出现ValueError，则可能是float或者解析错误
        return int(s)
    except ValueError:
        try:
            # 此处如果出现ValueError， 则可以判断是解析错误，不合法。
            return float(s)
        except ValueError:
            raise ParserError('number')


def parser_array(s):
    """解析Json字符串中的array类型。

    得到一个list。"""
    if len(s) < 2 or s[0] != '[':
        raise ParserError('array')
    temp_list = list()
    if s.startswith('[]'):
        return temp_list, s[2:]
    while True:
        temp_value, s = parser_value(s[1:])
        temp_list.append(temp_value)
        if len(s) > 1 and s[0] == ',':
            continue
        elif s.startswith(']'):
            return temp_list, s[1:]
        else:
            raise ParserError('array')


def parser_object(s):
    """解析Json字符串中的object类型。

    得到一个dict。"""
    if len(s) < 2 or s[0] != '{':
        raise ParserError('object')
    temp_dict = dict()
    if s.startswith('{}'):
        return temp_dict, s[2:]
    while True:
        temp_key, s = parser_string(s[1:])
        if len(s) > 1 and s[0] == ':':
            temp_dict[temp_key], s = parser_value(s[1:])
            if len(s) > 1 and s[0] == ',':
                continue
            elif s.startswith('}'):
                return temp_dict, s[1:]
            else:
                raise ParserError('object')
        else:
            raise ParserError('object')
