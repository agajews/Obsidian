from ..bootstrap import (
    Panic, Object, Type, PrimFun,
    object_type
)
from .scope import Scope
from .list import List


class Fun(Object):
    def __init__(self, defn_scope, body):
        super().__init__(
            {'body': body, 'defn_scope': defn_scope}, fun_type)
        # print(f'Created fun with body {body}')

    def call(self, caller_scope, args):
        scope = Scope(self.get('defn_scope'))
        scope.get('meta').set('args', List(args))
        scope.get('meta').set('fun', self)
        scope.set('return', ret)
        body = self.get('body')
        if not isinstance(body, List):
            raise Panic('Function body must be a list')
        try:
            for statement in body.elems[:-1]:
                scope.eval(statement)
            return scope.eval(body.elems[-1])
        except ReturnException as e:  # hack to use Python's function stack instead of building our own
            return e.obj

    def __repr__(self):
        return 'Fun({})'.format(self.body)


class FunType(Type):
    def __init__(self):
        super().__init__('Fun', object_type, ['body'])

    def macro(self, scope, body):
        return Fun(scope, scope.eval(body))


class ReturnException(Exception):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj


class Return(PrimFun):
    def __init__(self):
        super().__init__('return', ['obj'])

    def fun(obj):
        raise ReturnException(obj)


fun_type = FunType()
ret = Return()
