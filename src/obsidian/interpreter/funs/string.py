from ..types import PrimFun, Panic, String


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


concat = Concat()
