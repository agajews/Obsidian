from ..bootstrap import (
    Type, Object, PrimFun, Panic,
    String,
    object_type, string_type,
    nil,
)
from .ast import (
    ASTIdent, ASTString, ASTInt, ASTList, ASTCall, ASTBinarySlurp,
)
from .int import int_type
from .list import list_type


class Scope(Object):
    def __init__(self, parent=None):
        super().__init__({}, scope_type)
        self.get('meta').set('eval', Eval(self))
        self.get('meta').set('scope', self)
        self.get('meta').set('parent', parent if parent is not None else nil)

    def eval(self, ast):
        if isinstance(ast, ASTCall):
            # print(f'Calling {ast}')
            return self.eval(ast.get('callable')).call(self, ast.get('args').elems)
        elif isinstance(ast, ASTIdent):
            ident = ast.get('ident')
            if not isinstance(ident, String):
                raise Panic('Invalid ident')
            ident = ident.str
            if ident in self.attrs:
                return self.get(ident)
            if self.get('meta').get('parent') is not nil:
                return self.get('meta').get('parent').eval(ast)
            raise Panic('No such object `{}`'.format(ident))
        elif isinstance(ast, ASTString):
            return string_type.call(self, [ast])
        elif isinstance(ast, ASTInt):
            return int_type.call(self, [ast])
        elif isinstance(ast, ASTList):
            return list_type.call(self, [ast])
        elif isinstance(ast, ASTBinarySlurp):
            raise Panic('Got binary slurp {}'.format(ast))
        else:
            raise NotImplementedError(
                'Evaluation of node {} not implemented'.format(ast))


class Eval(PrimFun):
    def __init__(self, scope):
        super().__init__('eval', ['ast'])
        self.scope = scope

    def fun(self, ast):
        return self.scope.eval(ast)


class ScopeType(Type):
    def __init__(self):
        super().__init__('Scope', object_type, ['parent'])

    def fun(self, parent):
        if parent is nil:
            return Scope()
        return Scope(parent)


scope_type = ScopeType()
