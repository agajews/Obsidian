from ..types import PrimFun, Panic, String, string_type, Int


class StringHash(PrimFun):
    def __init__(self):
        super().__init__('hash', ['string'])

    def fun(self, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        return Int(hash(string.str))


class Concat(PrimFun):
    def __init__(self):
        super().__init__('get', variadic=True)

    def fun(self, *strings):
        catted_string = ''
        for string in strings:
            if not isinstance(string, String):
                raise Panic('Strings must be strings')
            catted_string += string.str
        return String(catted_string)


string_type.get('methods').set('hash', StringHash())
concat = Concat()
