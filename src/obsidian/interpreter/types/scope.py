from ..bootstrap import (
    Type, Object, PrimFun, Panic,
    String,
    object_type, string_type,
    nil,
)
from .ast import (
    ASTIdent, ASTString, ASTInt, ASTFloat, ASTList, ASTCall, ASTBinarySlurp, ASTSymbol,
)
from .int import int_type, Int
from .float import float_type
from .list import list_type, List
from .symbol import symbol_type, Symbol


class DummyCall:
    def __init__(self, callable_expr, args):
        self.callable_expr = callable_expr  # already evaluated
        self.args = args

    def __repr__(self):
        return 'DummyCall({}, {})'.format(self.callable_expr, self.args)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


class Scope(Object):
    def __init__(self, parent=None):
        super().__init__({}, scope_type)
        self.get('meta').set('eval', Eval(self))
        self.get('meta').set('scope', self)
        self.get('meta').set('parent', parent if parent is not None else nil)

    def parse_binary_subexpr(self, slurp, lhs, min_precedence=-1, pos=0):
        # pos always points to a terminal
        def lookahead():
            if pos >= len(slurp) - 1:
                return None, None, None
            return slurp[pos + 1]
        next_op, next_precedence, next_associativity = lookahead()
        while next_op is not None and next_precedence >= min_precedence:
            op, precedence, associativity = next_op, next_precedence, next_associativity
            pos += 2
            rhs = slurp[pos]
            next_op, next_precedence, next_associativity = lookahead()
            if associativity in ['left', 'right']:
                while next_op and (next_precedence > precedence or
                                   (next_associativity == 'right' and
                                    next_precedence == precedence)):
                    pos, rhs = self.parse_binary_subexpr(
                        slurp, rhs, next_precedence, pos)
                    next_op, next_precedence, next_associativity = lookahead()
                lhs = DummyCall(op, [lhs, rhs])
            elif associativity == 'none':
                args = [lhs]
                pos, rhs = self.parse_binary_subexpr(
                    slurp, rhs, precedence + 1, pos)
                next_op, next_precedence, next_associativity = lookahead()
                args.append(rhs)
                while next_op is op:
                    pos += 2
                    rhs = slurp[pos]
                    pos, rhs = self.parse_binary_subexpr(
                        slurp, rhs, precedence + 1, pos)
                    next_op, next_precedence, next_associativity = lookahead()
                    args.append(rhs)
                lhs = DummyCall(op, args)
            else:
                raise Exception(
                    'Invalid associativity {}'.format(associativity))
        return pos, lhs

    def parse_binary_slurp(self, slurp):
        slurp = list(slurp)  # copy
        for i in range(1, len(slurp), 2):
            op = self.eval(slurp[i])
            precedence = 9
            associativity = 'left'
            if op.has('precedence'):
                precedence = op.get('precedence')
                if not isinstance(precedence, Int):
                    raise Panic('Invalid precedence {}'.format(precedence))
                precedence = precedence.int
                if precedence < 0 or precedence > 9:
                    raise Panic(
                        'Precedence must be between 0 and 9, inclusive')
            if op.has('associativity'):
                associativity = op.get('associativity')
                if not isinstance(associativity, Symbol):
                    raise Panic(
                        'Invalid associativity {}'.format(associativity))
                associativity = associativity.symbol
                if not associativity in ['left', 'none', 'right']:
                    raise Panic(
                        'Associativity must be either @left, @none, or @right')
            slurp[i] = (op, precedence, associativity)
        pos, expr = self.parse_binary_subexpr(slurp, slurp[0])
        return expr

    def eval(self, ast):
        if isinstance(ast, ASTCall):
            return self.eval(ast.get('callable')).call(self, ast.get('args').elems)
        elif isinstance(ast, DummyCall):
            return ast.callable_expr.call(self, ast.args)
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
        elif isinstance(ast, ASTFloat):
            return float_type.call(self, [ast])
        elif isinstance(ast, ASTSymbol):
            return symbol_type.call(self, [ast])
        elif isinstance(ast, ASTList):
            return list_type.call(self, [ast])
        elif isinstance(ast, ASTBinarySlurp):
            slurp = ast.get('slurp')
            if not isinstance(slurp, List):
                raise Panic('Invalid binary slurp {}'.format(slurp))
            return self.eval(self.parse_binary_slurp(slurp.elems))
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
