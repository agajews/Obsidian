from ..types import PrimFun, String, Panic
from .get_attr import get_attr


class Puts(PrimFun):
    def __init__(self):
        super().__init__('puts', variadic=True)

    def macro(self, scope, *strings):
        # if not isinstance(string, String):
        #     raise Panic('Argument must be a string')
        strings = [get_attr.fun(scope.eval(s), String(
            'to_str')).call(scope) for s in strings]
        for string in strings:
            if not isinstance(string, String):
                raise Panic('to_str must return a string')
        string = ' '.join(s.str for s in strings)
        print(string)


puts = Puts()
