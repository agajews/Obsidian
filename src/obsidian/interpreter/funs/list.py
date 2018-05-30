from ..types import (
    PrimFun,
    Panic,
    List,
    Int,
    String,
    Scope,
)
from ..types.scope import to_str, call_method
from ..types.ast import ASTList, ASTIdent
from .get_attr import get_attr


class ListConstructor(PrimFun):
    def __init__(self):
        super().__init__('List', ['ast'])

    def macro(self, scope, ast):
        elems = ast.get('elems')
        if not isinstance(elems, List):
            raise Panic('Invalid list')
        return List([scope.eval(elem) for elem in elems.elems])


class ListToStr(PrimFun):
    def __init__(self):
        super().__init__('List.to_str', ['list'])

    def macro(self, scope, lst):
        lst = scope.eval(lst)
        self.typecheck_arg(lst, List)
        strs = [to_str(scope, elem) for elem in lst.elems]
        return String('[' + ', '.join(strs) + ']')


class ListGet(PrimFun):
    def __init__(self):
        super().__init__('List.get', ['list', 'idx'])

    def fun(self, lst, idx):
        self.typecheck_arg(lst, List)
        self.typecheck_arg(idx, Int)
        if idx.int >= len(lst.elems):
            raise Panic('Index `{}` out of range (len = `{}`)'.format(
                idx.int, len(lst.elems)))
        return lst.elems[idx.int]


class ListSet(PrimFun):
    def __init__(self):
        super().__init__('List.set', ['list', 'idx', 'val'])

    def fun(self, lst, idx, val):
        self.typecheck_arg(lst, List)
        self.typecheck_arg(idx, Int)
        if idx.int >= len(lst.elems):
            raise Panic('Index `{}` out of range (len = `{}`)'.format(
                idx.int, len(lst.elems)))
        lst.elems[idx.int] = val


class ListLen(PrimFun):
    def __init__(self):
        super().__init__('List.len', ['list'])

    def fun(self, lst):
        self.typecheck_arg(lst, List)
        return Int(len(lst.elems))


class ListDot(PrimFun):
    def __init__(self):
        super().__init__('List.dot', ['list', 'scope', 'attr'])

    def macro(self, scope, lst, eval_scope, attr):
        # print(scope)
        lst = scope.eval(lst)
        attr = scope.eval(attr)
        eval_scope = scope.eval(eval_scope)
        self.typecheck_arg(lst, List)
        self.typecheck_arg(eval_scope, Scope)
        self.typecheck_arg(attr, (ASTIdent, ASTList))
        attr.validate()
        if isinstance(attr, ASTIdent):
            return get_attr.fun(lst, attr.get('ident'))
        else:
            elems = attr.elems_list()
            if not len(elems) == 1:
                raise Panic(
                    'PrimFun `List.dot` needs exactly `1` element in its attribute list, not `{}`'
                    .format(len(elems)))
            return call_method(eval_scope, lst, 'get', [attr.elems_list()[0]])


List.T.set('call', ListConstructor())
List.T.get('methods').set('len', ListLen())
List.T.get('methods').set('get', ListGet())
List.T.get('methods').set('set', ListSet())
List.T.get('methods').set('to_str', ListToStr())
List.T.get('methods').set('dot', ListDot())
