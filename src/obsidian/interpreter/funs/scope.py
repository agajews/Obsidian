from ..types import (
    PrimFun,
    Scope,
    String,
    nil,
)


class ScopeConstructor(PrimFun):
    def __init__(self):
        super().__init__('Module', ['parent'])

    def fun(self, parent):
        if parent is nil:
            return Scope()
        return Scope(parent)


class ScopeToStr(PrimFun):
    def __init__(self):
        super().__init__('Scope.to_str', ['scope'])

    def fun(self, scope):
        self.typecheck_arg(scope, Scope)
        return String('<scope `{}`>'.format(scope.name_string()))


Scope.T.set('call', ScopeConstructor())
Scope.T.get('methods').set('to_str', ScopeToStr())
