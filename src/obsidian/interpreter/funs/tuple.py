from ..types import (
    PrimFun,
    Panic,
    Tuple,
    Int,
    String,
    Scope,
)
from .get_attr import get_attr
from ..types.scope import to_str, call_method
from ..types.ast import ASTTuple, ASTIdent, ASTList


class TupleConstructor(PrimFun):
    def __init__(self):
        super().__init__('Tuple', ['ast'])

    def macro(self, scope, ast):
        self.typecheck_arg(ast, ASTTuple)
        ast.validate()
        return Tuple([scope.eval(elem) for elem in ast.elems_list()])


class TupleToStr(PrimFun):
    def __init__(self):
        super().__init__('Tuple.to_str', ['tuple'])

    def macro(self, scope, tup):
        tup = scope.eval(tup)
        self.typecheck_arg(tup, Tuple)
        strs = [to_str(scope, elem) for elem in tup.elems]
        return String('(' + ', '.join(strs) + ')')


class TupleHash(PrimFun):
    def __init__(self):
        super().__init__('Tuple.hash', ['tuple'])

    def macro(self, scope, tuple):
        tuple = scope.eval(tuple)
        self.typecheck_arg(tuple, Tuple)
        return Int(hash(tuple(get_attr.fun(elem, 'hash').call(scope) for elem in tuple.elems)))


class TupleGet(PrimFun):
    def __init__(self):
        super().__init__('Tuple.get', ['tuple', 'idx'])

    def fun(self, tup, idx):
        self.typecheck_arg(tup, Tuple)
        self.typecheck_arg(idx, Int)
        if idx.int >= len(tup.elems):
            raise Panic('Index `{}` out of range (len = `{}`)'.format(
                idx.int, len(tup.elems)))
        return tup.elems[idx.int]


class TupleLen(PrimFun):
    def __init__(self):
        super().__init__('Tuple.len', ['tuple'])

    def fun(self, tup):
        self.typecheck_arg(tup, Tuple)
        return Int(len(tup.elems))


class TupleDot(PrimFun):
    def __init__(self):
        super().__init__('Tuple.dot', ['tuple', 'scope', 'attr'])

    def macro(self, scope, tup, eval_scope, attr):
        # print(scope)
        tup = scope.eval(tup)
        attr = scope.eval(attr)
        eval_scope = scope.eval(eval_scope)
        self.typecheck_arg(tup, Tuple)
        self.typecheck_arg(eval_scope, Scope)
        self.typecheck_arg(attr, (ASTIdent, ASTList))
        attr.validate()
        if isinstance(attr, ASTIdent):
            return get_attr.fun(tup, attr.get('ident'))
        else:
            elems = attr.elems_list()
            if not len(elems) == 1:
                raise Panic(
                    'PrimFun `Tuple.dot` needs exactly `1` element in its attribute list, not `{}`'
                    .format(len(elems)))
            return call_method(eval_scope, tup, 'get', [attr.elems_list()[0]])


Tuple.T.set('call', TupleConstructor())
Tuple.T.get('methods').set('get', TupleGet())
Tuple.T.get('methods').set('to_str', TupleToStr())
Tuple.T.get('methods').set('hash', TupleHash())
Tuple.T.get('methods').set('len', TupleLen())
Tuple.T.get('methods').set('dot', TupleDot())
