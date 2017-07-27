#!/usr/bin/env python
# -*- coding: utf-8 -*-

ACCEPTED_SPACE_CHARS = '{[}],:'


def deep_copy_value(v):
    """对于value进行深拷贝。

    dict和list类型需要深拷贝，其余直接返回。"""
    if isinstance(v, dict):
        return deep_copy_dict(v)
    elif isinstance(v, list):
        return deep_copy_list(v)
    else:
        return v


def deep_copy_list(l):
    """对于list进行深拷贝。

    list中包含很多个value，进行递归。"""
    new_l = list()
    for i in l:
        new_l.append(deep_copy_value(i))
    return new_l


def deep_copy_dict(d):
    """对dict进行深拷贝。

    key一定为str，value进行递归"""
    new_d = dict()
    for k, v in d.iteritems():
        new_d[k] = deep_copy_value(v)
    return new_d


def remove_space(s):
        """对于输入的一个字符串，将允许去除的空格全部去掉，以便于下一步操作。

        初始化一个新串，遍历旧串， 如果是空格，查看新串末尾是否为允许前后出现空
        格字符，如果是，则不加空格到新串中；如果是允许前后出现空格字符，则把新串
        末尾的空格都去除掉；如果为其他，则直接加入新串中。"""
        new_s = ''   # new string
        for c in s:
            if c in ACCEPTED_SPACE_CHARS:
                new_s = new_s.rstrip()
                new_s += c
            elif c.isspace():
                # The new string is empty or the end of new string is not the accepted space chars
                if len(new_s) == 0 or new_s[-1] not in ACCEPTED_SPACE_CHARS:
                    new_s += c
            else:
                new_s += c
        return new_s
