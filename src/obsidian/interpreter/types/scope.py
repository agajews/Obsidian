from ..bootstrap import (
    Type,
    Object,
    PrimFun,
    Panic,
    String,
    nil,
    type_name,
)
from .ast import (
    ASTIdent,
    ASTString,
    ASTInterpolatedString,
    ASTInt,
    ASTFloat,
    ASTList,
    ASTTuple,
    ASTMap,
    ASTCall,
    ASTBinarySlurp,
    ASTSymbol,
    ASTUnquote,
    ASTBlock,
)
from .int import Int
from .float import Float
from .list import List
from .tuple import Tuple
from .map import Map
from .symbol import Symbol
from .bool import Bool


class Scope(Object):
    T = Type('Scope', Object.T)

    def __init__(self, parent=None):
        super().__init__({})
        self.get('meta').set('eval', Eval(self))
        self.get('meta').set('scope', self)
        self.get('meta').set('parent', parent if parent is not None else nil)

    def parse_binary_subexpr(self, slurp, lhs, min_precedence=-1, pos=0):
        # pos always points to a terminal
        def lookahead():
            if pos >= len(slurp) - 1:
                return None, None, None, None
            return slurp[pos + 1]
        next_op, next_raw_op, next_precedence, next_associativity = lookahead()
        while next_op is not None and next_precedence >= min_precedence:
            op, raw_op, precedence, associativity = next_op, next_raw_op, next_precedence, next_associativity
            pos += 2
            rhs = slurp[pos]
            next_op, next_raw_op, next_precedence, next_associativity = lookahead()
            if associativity in ['left', 'right']:
                while next_op and (next_precedence > precedence or
                                   (next_associativity == 'right' and
                                    next_precedence == precedence)):
                    pos, rhs = self.parse_binary_subexpr(
                        slurp, rhs, next_precedence, pos)
                    next_op, next_raw_op, next_precedence, next_associativity = lookahead()
                parseinfo = None
                if hasattr(raw_op, 'parseinfo'):
                    parseinfo = raw_op.parseinfo
                lhs = ASTCall(raw_op, List(
                    [lhs, rhs]), parseinfo=parseinfo)
            elif associativity == 'none':
                args = [lhs]
                pos, rhs = self.parse_binary_subexpr(
                    slurp, rhs, precedence + 1, pos)
                next_op, next_raw_op, next_precedence, next_associativity = lookahead()
                args.append(rhs)
                while next_op is op:
                    pos += 2
                    rhs = slurp[pos]
                    pos, rhs = self.parse_binary_subexpr(
                        slurp, rhs, precedence + 1, pos)
                    next_op, next_raw_op, next_precedence, next_associativity = lookahead()
                    args.append(rhs)
                parseinfo = None
                if hasattr(raw_op, 'parseinfo'):
                    parseinfo = raw_op.parseinfo
                lhs = ASTCall(raw_op, List(args), parseinfo=parseinfo)
            else:
                raise Exception(
                    'Invalid associativity {}'.format(associativity))
        return pos, lhs

    def parse_binary_slurp(self, slurp):
        slurp = list(slurp)  # copy
        for i in range(1, len(slurp), 2):
            raw_op = slurp[i]
            # make sure there are no side effects
            assert isinstance(raw_op, ASTIdent)
            op = self.eval(slurp[i])
            precedence = 9
            associativity = 'left'
            if op.has('precedence'):
                precedence = op.get('precedence')
                if not isinstance(precedence, Int):
                    raise Panic('Invalid precedence {}'.format(precedence))
                precedence = precedence.int
                if precedence < 0 or precedence > 11:
                    raise Panic(
                        'Precedence must be between 0 and 11, inclusive')
            if op.has('associativity'):
                associativity = op.get('associativity')
                if not isinstance(associativity, Symbol):
                    raise Panic(
                        'Invalid associativity {}'.format(associativity))
                associativity = associativity.symbol
                if not associativity in ['left', 'none', 'right']:
                    raise Panic(
                        'Associativity must be either @left, @none, or @right')
            slurp[i] = (op, raw_op, precedence, associativity)
        pos, expr = self.parse_binary_subexpr(slurp, slurp[0])
        # print('Binary slurp:')
        # print(expr)
        return expr

    def preprocess(self, ast):
        if isinstance(ast, ASTCall):
            return ASTCall(self.preprocess(ast.get('callable')),
                           List([self.preprocess(arg)
                                 for arg in ast.args_list()]),
                           parseinfo=ast.parseinfo)
        elif isinstance(ast, ASTList):
            return ASTList(List([self.preprocess(elem) for elem in ast.elems_list()]),
                           parseinfo=ast.parseinfo)
        elif isinstance(ast, ASTTuple):
            return ASTTuple(Tuple([self.preprocess(elem) for elem in ast.elems_list()]),
                            parseinfo=ast.parseinfo)
        elif isinstance(ast, ASTMap):
            return ASTMap(List([self.preprocess(elem) for elem in ast.elems_list()]),
                          parseinfo=ast.parseinfo)
        elif isinstance(ast, ASTBlock):
            return ASTBlock(List([self.preprocess(elem) for elem in ast.statements_list()]),
                            parseinfo=ast.parseinfo)
        elif isinstance(ast, ASTInterpolatedString):
            return ASTInterpolatedString(List([self.preprocess(body) for body in ast.body_list()]))
        elif isinstance(ast, (ASTIdent,
                              ASTString,
                              ASTInt,
                              ASTFloat,
                              ASTSymbol)):
            # leaf nodes
            return ast
        elif isinstance(ast, ASTBinarySlurp):
            slurp = ast.get('slurp')
            if not isinstance(slurp, List):
                raise Panic('Invalid binary slurp {}'.format(slurp))
            return self.parse_binary_slurp(slurp.elems)
        elif isinstance(ast, ASTUnquote):
            return self.eval(self.preprocess(ast.get('expr')))
        else:
            raise NotImplementedError(
                'Evaluation of node {} not implemented'.format(ast))

    def get_recursive(self, name):
        if name in self.attrs:
            return self.get(name)
        if self.get('meta').get('parent') is not nil:
            return self.get('meta').get('parent').get_recursive(name)
        raise Panic('No such object `{}`'.format(name))

    def assign_recursive(self, name, val):
        if name in self.attrs:
            return self.set(name, val)
        if self.get('meta').get('parent') is not nil:
            return self.get('meta').get('parent').assign_recursive(name, val)
        raise Panic('No such object `{}`'.format(name))

    def eval(self, ast):
        ast = self.preprocess(ast)
        return self._eval(ast)

    def name_string(self):
        name = self.get('meta').get('name')
        if not isinstance(name, String):
            return '[Fun name {} not a string]'.format(name)
        return name.str

    def _eval(self, ast):
        if isinstance(ast, ASTCall):
            return self._eval(ast.get('callable')).call(self, ast.get('args').elems)
        elif isinstance(ast, ASTIdent):
            ast.validate()
            return self.get_recursive(ast.get('ident').str)
        elif isinstance(ast, ASTString):
            return String.T.call(self, [ast])
        elif isinstance(ast, ASTInterpolatedString):
            ast.validate()
            strings = [get_attr.fun(self._eval(elem), String('to_str')).call(self)
                       for elem in ast.body_list()]
            return String(''.join(s.str for s in strings))
        elif isinstance(ast, ASTInt):
            return Int.T.call(self, [ast])
        elif isinstance(ast, ASTFloat):
            return Float.T.call(self, [ast])
        elif isinstance(ast, ASTSymbol):
            return Symbol.T.call(self, [ast])
        elif isinstance(ast, ASTList):
            return List.T.call(self, [ast])
        elif isinstance(ast, ASTBlock):
            ast.validate()
            return List([self._eval(statement) for statement in ast.statements_list()])
        elif isinstance(ast, ASTTuple):
            return Tuple.T.call(self, [ast])
        elif isinstance(ast, ASTMap):
            return Map.T.call(self, [ast])
        else:
            raise NotImplementedError(
                'Evaluation of node {} not implemented'.format(ast))

    def __repr__(self):
        return 'Scope({})'.format({k: v for k, v in self.attrs.items() if k != 'meta'})


class MethodFun(PrimFun):
    def __init__(self, obj, method):
        super().__init__('method_fun', variadic=True)
        self.obj = obj
        self.method = method

    def macro(self, scope, *args):
        scope.set('__self__', self.obj)
        res = self.method.call(
            scope, [ASTIdent(String('__self__'))] + list(args))
        if '__self__' in scope.attrs:
            del scope.attrs['__self__']
        return res


class GetAttr(PrimFun):
    def __init__(self):
        super().__init__('get_attr', ['obj', 'attr'])

    def fun(self, obj, attr):
        self.typecheck_arg(attr, String)
        if not obj.has(attr.str):
            obj_type = obj.get('meta').get('type')
            if obj_type.get('methods').has(attr.str):
                return MethodFun(obj, obj_type.get('methods').get(attr.str))
            if obj_type.get('statics').has(attr.str):
                return obj_type.get('statics').get(attr.str)
            seen_types = set()
            while id(obj_type.get('parent')) not in seen_types:  # while not looping
                obj_type = obj_type.get('parent')
                seen_types.add(id(obj_type))
                if obj_type.get('methods').has(attr.str):
                    return MethodFun(obj, obj_type.get('methods').get(attr.str))
                if obj_type.get('statics').has(attr.str):
                    return obj_type.get('statics').get(attr.str)
            raise Panic('{} `{}` has no attribute `{}`'.format(
                type_name(obj), to_str(Scope(), obj), attr.str))
        return obj.get(attr.str)


def call_method(scope, obj, name, args):
    return get_attr.fun(obj, String(name)).call(scope, args)


def to_str(scope, obj, panic=True):
    if panic:
        string = get_attr.fun(obj, String('to_str')).call(scope)
    else:
        try:
            string = get_attr.fun(obj, String('to_str')).call(scope)
        except Panic as p:
            return "[`{}`'s `to_str` failed with message '{}']".format(type_name(obj), p.msg)
    if not isinstance(string, String):
        if panic:
            raise Panic(
                '`to_str` for `{}` must return a `String`'.format(type_name(obj)))
        else:
            try:
                return "[`{}`'s `to_str` returned a `{}`, not a `String`]".format(type_name(obj), type_name(string))
            except Panic:
                return "[Calling `to_str` failed]"
    return string.str


def hash_obj(scope, obj):
    code = get_attr.fun(obj, String('hash')).call(scope)
    if not isinstance(code, Int):
        raise Panic(
            '`hash` for `{}` must return an `Int`'.format(type_name(obj)))
    return code.int


def obj_eq(parent_scope, obj, other):
    scope = Scope(parent_scope)
    scope.set('__other__', other.key)
    code = get_attr.fun(obj, String('eq')).call(
        scope, [ASTIdent(String('__other__'))])
    if not isinstance(code, Bool):
        raise Panic(
            '`eq` for `{}` must return a `Bool`'.format(type_name(obj)))
    return code.bool


class Eval(PrimFun):
    def __init__(self, scope):
        super().__init__('eval', ['ast'])
        self.scope = scope

    def fun(self, ast):
        # ast = self.scope.preprocess(ast)
        return self.scope.eval(ast)


get_attr = GetAttr()
