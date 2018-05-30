from ..bootstrap import (
    Panic,
    Object,
    Type,
    PrimFun,
    String,
)
from .scope import Scope
from .list import List


class Fun(Object):
    T = Type('Fun', Object.T)

    def __init__(self, defn_scope, name, body):
        if not len(body.elems_list()) > 0:
            raise Panic('Funs must have at least one body statement')
        super().__init__(
            {'name': name, 'body': body, 'definer': defn_scope})
        # print(f'Created fun with body {body}')

    def call(self, caller_scope, args=None):
        if args is None:
            args = []
        scope = Scope(self.get('definer'))
        scope.get('meta').set('args', List(args))
        scope.get('meta').set('caller', caller_scope)
        scope.get('meta').set('fun', self)
        scope.set('return', ret)
        body = self.get('body').get('elems')
        if not isinstance(body, List):
            raise Panic('Function body must be a list')
        try:
            for statement_idx, statement in enumerate(body.elems[:-1]):
                scope.eval(statement)
            statement = body.elems[-1]
            statement_idx = len(body.elems) - 1
            return scope.eval(statement)
        except ReturnException as e:  # hack to use Python's function stack instead of building our own
            return e.obj
        except Panic as p:
            raise Panic(p.msg, stack=p.stack +
                        [(self, {'args': args,
                                 'statement': statement,
                                 'statement_idx': statement_idx})])

    def name_string(self):
        name = self.get('name')
        if not isinstance(name, String):
            return '[Fun name {} not a string]'.format(name)
        return name.str

    def __repr__(self):
        return 'Fun({})'.format(self.body)


class ReturnException(Exception):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj


class Return(PrimFun):
    def __init__(self):
        super().__init__('return', ['obj'])

    def fun(self, obj):
        raise ReturnException(obj)


ret = Return()
