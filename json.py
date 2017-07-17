
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

    def parser_string(self, s):
        if s[0] != '"':
            raise MyError
        temp_index = 1
        while temp_index < len(s) and s[temp_index] != '"':
            temp_index = temp_index + 1
        if temp_index == len(s):
            raise MyError
        else:
            return s[1:temp_index], s[temp_index + 1 :]

    def is_digit(self, s):
        if s[0] >= '0' and s[0] <= '9':
            return True
        elif s[0] == 'e' or s[0] == 'E':
            return True
        elif s[0] == '+' or s[0] == '-' or s[0] == '.':
            return True
        else:
            return False

    def parser_value(self, s):
        if s[0] == '{':
            temp_index = 1
            count_bracket = 0
            while temp_index < len(s):
                if s[temp_index] == '{':
                    count_bracket = count_bracket + 1
                elif s[temp_index] == '}':
                    if count_bracket == 0:
                        break
                    else:
                        count_bracket = count_bracket - 1
                temp_index = temp_index + 1
            if temp_index == len(s):
                raise MyError
            else:
                return self.parser_object(s[:temp_index + 1]), s[temp_index + 1 :]
        elif s[0] == '[':
            temp_index = 1
            count_bracket = 0
            while temp_index < len(s):
                if s[temp_index] == '[':
                    count_bracket = count_bracket + 1
                elif s[temp_index] == ']':
                    if count_bracket == 0:
                        break
                    else:
                        count_bracket = count_bracket - 1
                temp_index = temp_index + 1
            if temp_index == len(s):
                raise MyError
            else:
                return self.parser_array(s[:temp_index + 1]), s[temp_index + 1 :]
        elif s[0] == '"':
            return self.parser_string(s)
        elif s[0] == 't':
            if len(s) >= 4 and s[1:4] == 'rue':
                return True, s[4:]
        elif s[0] == 'f':
            if len(s) >= 5 and s[1:5] == 'alse':
                return False, s[5:]
        elif s[0] == 'n':
            if len(s) >= 4 and s[1:4] = 'ull':
                return None, s[4:]
        elif (s[0] >= '0' and s[0] <= '9') or s[0] =='-':
            if(s[0] == '0' and len(s) > 1):
                raise  MyError
            temp_index = 1
            while temp_index < len(s) and self.is_digit(s[temp_index]):
                temp_index = temp_index + 1
            if temp_index == len(s):
                raise MyError
            else:
                return self.parser_number(s[0:temp_index]), s[temp_index:]
        else:
            raise MyError

    def parser_number(self, s):
        res = 0
        try:
            res = int(s)
            return res
        except:
            try:
                res = float(s)
                return res
            except:
                raise MyError

    def parser_array(self, s):
        try:
            if len(s) < 2 or s[0] != '[' or s[-1] != ']':
                raise  MyError
            index = 1
            temp_list = list()
            while True:
                temp_value, s = self.parser_value(s[1:])
                temp_list.append(temp_value)
                if len(s) > 1 and s[0] == ',':
                    s = s[1:]
                elif s == '}':
                    return temp_list
                else:
                    raise MyError
            return temp_list
        except:
            raise MyError

    def parser_object(self, s):
        try:
            if len(s) < 2 or s[0] != '{' or s[-1] != '}':
                raise MyError
            temp_dict = dict()
            temp_key = str()
            while True:
                temp_key, s = self.parser_string(s[1:])
                if s[0] == ':' and len(s) > 1:
                    temp_dict[temp_key], s = self.dump_value(s[1:])
                    if s[0] == ',' and len(s) > 1:
                        s = s[1:]
                    elif s == '}':
                        return temp_dict
                    else:
                        raise MyError
                else:
                    raise MyError
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

    def loads(self, s):
        s = self.handle_whitespace(s)
        try:
            _data = self.parser_object(s)
        except:
            raise MyError

    def dumps(self):
        return self.dump_object(self._data)

    def load_file(self, f):
        try:
            with open(f, "r") as read_json:
                json_str = ''.join(read_json.readlines())
                self.loads(json_str)
        except IOError:
            print("File read error!")


    def dump_file(self, f):
        try:
            out1 = open(f, "w")
            out1.write(self.dumps())
        except IOError:
            print("File write error!")
        finally:
            out1.close()

    def load_dict(self, d):
        _data = d
