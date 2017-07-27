#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonerror import DumpError
ESCAPE_DIR_DUMP = {'"': '"', '\\': '\\', '/': '/', '\b': 'b', '\f': 'f', '\n': 'n',
                   '\r': 'r', '\t': 't'}


def dump_string(s):
    """将str类型转换为Json字符串中带双引号的string

    """
    s = s.encode('unicode-escape').decode('string_escape')
    new_s = '"'
    for i in range(0, len(s)):
        if (i + 1) < len(s) and s[i:i + 2] == '\u':
            new_s += s[i]
        elif s[i] in ESCAPE_DIR_DUMP:
            new_s += '\\'
            new_s += ESCAPE_DIR_DUMP[s[i]]
        else:
            new_s += s[i]
    new_s += '"'
    return new_s


def dump_value(v):
    """判断v对应的类型是什么，转换为对应的类型或值

    """
    if v is True:
        return 'true'
    elif v is False:
        return 'false'
    elif isinstance(v, dict):
        return dump_object(v)
    elif isinstance(v, list):
        return dump_array(v)
    elif isinstance(v, float) or isinstance(v, int):
        return str(v)
    elif isinstance(v, unicode) or isinstance(v, str):
        return dump_string(v)
    elif v is None:
        return 'null'
    else:
        raise DumpError


def dump_array(l):
    """将list转换为Json字符串中的array类型。

    注意空list的特殊处理。"""
    return unicode('[%s]' % (', '.join(map(dump_value, l))))


def dump_object(d):
    """将dict转换为Json字符串中的object类型。

    注意空dict的特殊处理。"""
    return unicode(
        '{%s}' % (', '.join(map(lambda x, y: dump_string(x) + ': ' + dump_value(y),
                  d.keys(), d.values())))
    )
