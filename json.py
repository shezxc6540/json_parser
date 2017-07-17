

def has_six_chars(c):
    return c == '[' or c == '{' or c == ']' or c == '}' or c == ':' or c == ','

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
                if len(new_s) == 0 or has_six_chars(new_s[len(new_s) - 1]) is not True:
                    new_s += c
            else:
                new_s += c
        return new_s

    def is_string(s):
        return len(s) >= 2 and s[0] == '\"' and s[len(s) - 1] == '\"' and s[len(s) - 2] != '\\'

    def is_number(s):
        test = 0
        try:
            test = float(s)
            return True
        except:
            return False

    def is_object(s):
    def is_array(s):

    def is_value(s):
        return is_object(s) or is_array(s) or is_number(s) or is_string(s) or s == 'null' or s == 'true' or s == 'false'

    def parser_number(s):
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

    def parser_array(s):

    def parser_value(s):
        if s == 'null':
            return None
        elif s == 'true':
            return True
        elif s == 'false':
            return False
        elif is_string(s):
            return s
        elif is_number(s):
            return parser_number(s)
        elif is_object(s):
            return parser_object(s)
        elif is_array(s):
            return parser_array(s)
        elif
            raise my_error

    def parser_object(s):
        length = len(s)
        i = 0
        can_space = True
        while i < length:
            if can_space and s[i] == ' ':
                continue

    def main_parser(self, s):
        s = handle_whitespace(s)
        try:
            return parser_object(s)
        except:
            raise my_error

    def loads(self, s):
        pass

    def dumps(self):
        pass

    def load_file(self, f):
        pass

    def dump_file(self, f):
        pass

    def load_dict(self, d):
        _data = d
