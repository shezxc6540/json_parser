#!/usr/bin/env python
# -*- coding: utf-8 -*-


ACCEPTED_SPACE_CHARS = '{[}],:'
ESCAPE_DIR_PARSER = {'t': '\t', 'r': '\r', 'n': '\n', 'f': '\f', 'b': '\b'}
ESCAPE_DIR_DUMP = {'"': '"', '\\': '\\', '/': '/', '\b': 'b', '\f': 'f', '\n': 'n',
                   '\r': 'r', '\t': 't'}
LEGAL_DIGIT = '0123456789eE+-.'
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


class JsonParser(object):
    """Json解析类。

    可用于Json字符串与Python字典的相互转换"""
    def __init__(self):
        self._data = dict()

    def loads(self, s):
        """读取JSON格式数据，输入s为一个JSON字符串，无返回值。

        若遇到JSON格式错误的应该抛出异常。为简便考虑，JSON的最外层假定只为Object"""
        # 预处理字符串中的空格
        s = self.remove_space(s)
        try:
            self._data = self.parser_object(s)
        except ParserError as pe:
            print("Parser Error! Expecting: " + pe.error_type)

    def dumps(self):
        """将实例中的内容转成JSON格式返回。

        """
        try:
            return self.dump_object(self._data)
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
                self._data[k] = self.deep_copy_value(v)

    def dump_dict(self):
        """返回一个字典，包含实例中的内容。

        """
        return self.deep_copy_dict(self._data)

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
                self._data[k] = self.deep_copy_value(v)

    def remove_space(self, s):
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

    def parser_string(self, s):
        """解析Json字符串中的string形式。

        返回为Python中的str类型，出现不是预期的情况时，则抛出异常。"""
        if s[0] != '"':
            raise ParserError('string')
        temp_index = 1
        new_s = ''
        while temp_index < len(s) and s[temp_index] != '"':
            if s[temp_index] == '\\':
                temp_index += 1
                if temp_index == len(s):
                    raise ParserError('string')
                if s[temp_index] in ESCAPE_DIR_PARSER:
                    new_s += ESCAPE_DIR_PARSER[s[temp_index]]
                elif s[temp_index] in ('/', '"', '\\'):
                    new_s += s[temp_index]
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

    def parser_value(self, s):
        """解析Json字符串中的value类型。

        value类型包括string类型，object类型，array类型， number类型， 以及特殊的
        null，true，false，进行分支判断。"""

        # 第一个字符为{，认为是object
        if s[0] == '{':
            temp_index = 1
            count_bracket = 0
            # 找出与左括号相匹配的右括号的位置
            while temp_index < len(s):
                if s[temp_index] == '{':
                    count_bracket += 1
                elif s[temp_index] == '}':
                    if count_bracket == 0:
                        break
                    else:
                        count_bracket -= 1
                temp_index += 1
            if temp_index == len(s):
                raise ParserError('object')
            else:
                return self.parser_object(s[:temp_index + 1]), s[temp_index + 1:]
        # 第一个字符为[，认为是array
        elif s[0] == '[':
            temp_index = 1
            count_bracket = 0
            # 找出与左括号相匹配的右括号的位置
            while temp_index < len(s):
                if s[temp_index] == '[':
                    count_bracket += 1
                elif s[temp_index] == ']':
                    if count_bracket == 0:
                        break
                    else:
                        count_bracket -= 1
                temp_index += 1
            if temp_index == len(s):
                raise ParserError('array')
            else:
                return self.parser_array(s[:temp_index + 1]), s[temp_index + 1:]
        # 第一个字符为"，认为是string
        elif s[0] == '"':
            return self.parser_string(s)
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
                return self.parser_number(s[0:temp_index]), s[temp_index:]
        else:
            raise ParserError('value')

    def parser_number(self, s):
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

    def parser_array(self, s):
        """解析Json字符串中的array类型。

        得到一个list。"""
        if len(s) < 2 or s[0] != '[' or s[-1] != ']':
            raise ParserError('array')
        temp_list = list()
        if s == '[]':
            return temp_list
        while True:
            temp_value, s = self.parser_value(s[1:])
            temp_list.append(temp_value)
            if len(s) > 1 and s[0] == ',':
                continue
            elif s == ']':
                return temp_list
            else:
                raise ParserError('array')

    def parser_object(self, s):
        """解析Json字符串中的object类型。

        得到一个dict。"""
        if len(s) < 2 or s[0] != '{' or s[-1] != '}':
            raise ParserError('object')
        temp_dict = dict()
        temp_key = str()
        if s == '{}':
            return temp_dict
        while True:
            temp_key, s = self.parser_string(s[1:])
            if s[0] == ':' and len(s) > 1:
                temp_dict[temp_key], s = self.parser_value(s[1:])
                if s[0] == ',' and len(s) > 1:
                    continue
                elif s == '}':
                    return temp_dict
                else:
                    raise ParserError('object')
            else:
                raise ParserError('object')

    def dump_string(self, s):
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

    def dump_value(self, v):
        """判断v对应的类型是什么，转换为对应的类型或值

        """
        if v is True:
            return 'true'
        elif v is False:
            return 'false'
        elif isinstance(v, dict):
            return self.dump_object(v)
        elif isinstance(v, list):
            return self.dump_array(v)
        elif isinstance(v, float) or isinstance(v, int):
            return str(v)
        elif isinstance(v, unicode) or isinstance(v, str):
            return self.dump_string(v)
        elif v is None:
            return 'null'
        else:
            raise DumpError

    def dump_array(self, l):
        """将list转换为Json字符串中的array类型。

        注意空list的特殊处理。"""
        return '[%s]' % (', '.join(map(self.dump_value, l)))

    def dump_object(self, d):
        """将dict转换为Json字符串中的object类型。

        注意空dict的特殊处理。"""
        return unicode(
            '{%s}' % (', '.join(map(lambda x, y: self.dump_string(x) + ': ' + self.dump_value(y),
                      d.keys(), d.values())))
        )

    def deep_copy_value(self, v):
        """对于value进行深拷贝。

        dict和list类型需要深拷贝，其余直接返回。"""
        if isinstance(v, dict):
            return self.deep_copy_dict(v)
        elif isinstance(v, list):
            return self.deep_copy_list(v)
        else:
            return v

    def deep_copy_list(self, l):
        """对于list进行深拷贝。

        list中包含很多个value，进行递归。"""
        new_l = list()
        for i in l:
            new_l.append(self.deep_copy_value(i))
        return new_l

    def deep_copy_dict(self, d):
        """对dict进行深拷贝。

        key一定为str，value进行递归"""
        new_d = dict()
        for k, v in d.iteritems():
            new_d[k] = self.deep_copy_value(v)
        return new_d
