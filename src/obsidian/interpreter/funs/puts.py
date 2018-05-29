from ..types import PrimFun
from ..types.scope import to_str


class Puts(PrimFun):
    def __init__(self):
        super().__init__('prim.puts', variadic=True)

    def macro(self, scope, *strings):
        print(' '.join(to_str(scope, scope.eval(s)) for s in strings))


puts = Puts()
