

def has_six_chars(c):
    return c == '[' or c == '{' or c == ']' or c == '}' or c == ':' or c == ','

class MyError(Exception):
    def __init__(self):
        pass

class JsonParser:
    _data = dict()

    def __init__(self):
        pass

    def handle_whitespace(self, s):
        new_s = ''
        for c in s:
            if has_six_chars(c):
                new_s = new_s.rstrip()
                new_s += c
            elif c.isspace():
                if len(new_s) == 0 or has_six_chars(new_s[-1]) is not True:
                    new_s += c
            else:
                new_s += c
        return new_s

    def parser_number(self, s):
        res = 0
        try:
            res = float(s)
            try:
                temp = int(s)
                res = temp
            except:
                print('It is a integer')
        except:
            print('number error')

    def parser_array(self, s):
        try:
            sum_length = len(s)
            if sum_length < 2 or s[0] != '[' or s[-1] != ']':
                raise  MyError
            index = 1
            temp_list = list()
            while index < sum_length - 1:
                if s[index] == '{':
                    if pre_char != ':':
                        raise  MyError
                    temp_index = index + 1
                    count_bracket = 0
                    while temp_index < (sum_length - 1):
                        if s[temp_index] == '{':
                            count_bracket = count_bracket + 1
                        elif s[temp_index] == '}':
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket = count_bracket - 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_list.append(self.parser_object(s[index:temp_index + 1]))
                        index = temp_index + 1
                        single_finished = True
                elif s[index] == '[':
                    if pre_char != ':':
                        raise  MyError
                    temp_index = index + 1
                    count_bracket = 0
                    while temp_index < (sum_length - 1):
                        if s[temp_index] == '[':
                            count_bracket = count_bracket + 1
                        elif s[temp_index] == ']':
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket = count_bracket - 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_list.append(self.parser_object(s[index:temp_index + 1]))
                        index = temp_index + 1
                        single_finished = True
                elif s[index] == '"':
                    if pre_char != ',' or index != 1 or pre_char != ':':
                        raise MyError
                    temp_index = index + 1
                    while temp_index < (sum_length - 1) and s[temp_index] != '"':
                        temp_index = temp_index + 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_list.append(s[index:temp_index + 1])
                        index = temp_index + 1
                elif s[index] == ',':
                    if not single_finished:
                        raise MyError
                    handle_key = True
                    pre_char = ','
                elif s[index] == 't':
                    pass
                elif s[index] == 'f':
                    pass
                elif s[index] == 'n':
                    pass
                elif (s[index] >= '0' and s[index] <= '9') or s[index] =='-':
                    if pre_char != ',' or index != 1:
                        raise MyError
                    temp_index = index + 1
                    while temp_index < (sum_length - 1) and (s[temp_index] != ',' and s[temp_index] != '}'):
                        temp_index = temp_index + 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_list.append(self.parser_number(s[index]))
                        index = temp_index + 1
            return temp_list
        except:

    def parser_object(self, s):
        try:
            sum_length = len(s)
            if sum_length < 2 or s[0] != '{' or s[-1] != '}':
                raise MyError
            temp_dict = dict()
            temp_key = str()
            handle_key = True
            single_finished = False
            half_finished = False
            index = 1
            pre_char = None
            while index < sum_length - 1:
                if s[index] == '{':
                    if pre_char != ':':
                        raise  MyError
                    temp_index = index + 1
                    count_bracket = 0
                    while temp_index < (sum_length - 1):
                        if s[temp_index] == '{':
                            count_bracket = count_bracket + 1
                        elif s[temp_index] == '}':
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket = count_bracket - 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_dict[temp_key] = self.parser_object(s[index:temp_index + 1])
                        index = temp_index + 1
                        single_finished = True
                elif s[index] == '[':
                    if pre_char != ':':
                        raise  MyError
                    temp_index = index + 1
                    count_bracket = 0
                    while temp_index < (sum_length - 1):
                        if s[temp_index] == '[':
                            count_bracket = count_bracket + 1
                        elif s[temp_index] == ']':
                            if count_bracket == 0:
                                break
                            else:
                                count_bracket = count_bracket - 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_dict[temp_key] = self.parser_object(s[index:temp_index + 1])
                        index = temp_index + 1
                        single_finished = True
                elif s[index] == '"':
                    if pre_char != ',' or index != 1 or pre_char != ':':
                        raise MyError
                    temp_index = index + 1
                    while temp_index < (sum_length - 1) and s[temp_index] != '"':
                        temp_index = temp_index + 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        if handle_key:
                            temp_key = s[index:temp_index + 1]
                            half_finished = True
                        else:
                            temp_dict[temp_key] = s[index:temp_index + 1]
                            single_finished = True
                        index = temp_index + 1
                elif s[index] == ',':
                    if not single_finished:
                        raise MyError
                    handle_key = True
                elif s[index] == ':':
                    if not half_finished:
                        raise MyError
                    handle_key = False
                elif s[index] == 't':
                    pass
                elif s[index] == 'f':
                    pass
                elif s[index] == 'n':
                    pass
                elif (s[index] >= '0' and s[index] <= '9') or s[index] =='-':
                    if pre_char != ',' or index != 1:
                        raise MyError
                    temp_index = index + 1
                    while temp_index < (sum_length - 1) and (s[temp_index] != ',' and s[temp_index] != '}'):
                        temp_index = temp_index + 1
                    if temp_index == (sum_length - 1):
                        raise MyError
                    else:
                        temp_dict[temp_key] = self.parser_number(s[index])
                        index = temp_index + 1
                else:
                    raise MyError
                pre_char = s[index]
                index = index + 1
            return temp_dict
        except:
            raise MyError

    def dump_string(self, s):
        return '"' + s + '"'

    def dump_value(self, v):
        if isinstance(v, dict):
            return self.dump_object(v)
        elif isinstance(v, list):
            return self.dump_array(v)
        elif isinstance(v, float) or isinstance(v, int):
            return str(v)
        elif isinstance(v, str):
            return self.dump_string(v)
        elif isinstance(v, None):
            return 'null'
        elif v is False:
            return 'false'
        elif v is True:
            return 'true'

    def dump_array(self, l):
        temp_str = '['
        for it in l:
            temp_str += self.dump_value(it)
            temp_str += ','
        return temp_str[:-1] + ']'

    def dump_object(self, d):
        temp_str = '{'
        for k,v in d.iteritems():
            temp_str += self.dump_string(k)
            temp_str += ':'
            temp_str += self.dump_value(v)
            temp_str += ','
        return temp_str[:-1] + '}'

    def main_parser(self, s):
        s = self.handle_whitespace(s)
        try:
            return self.parser_object(s)
        except:
            raise MyError


    def loads(self, s):
        pass

    def dumps(self):
        return self.dump_object(self._data)

    def load_file(self, f):
        pass

    def dump_file(self, f):
        pass

    def load_dict(self, d):
        _data = d
