from ..types import PrimFun, String, Panic


class Puts(PrimFun):
    def __init__(self):
        super().__init__('puts', ['str'])

    def fun(self, string):
        if not isinstance(string, String):
            raise Panic('Argument must be a string')
        print(string.str)


puts = Puts()
