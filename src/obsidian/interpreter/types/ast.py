from ... import semantics as sem
from ..bootstrap import (
    String,
    Object,
    Type,
)
from .int import Int
from .float import Float
from .list import List
from .tuple import Tuple
from .symbol import Symbol


ast_node_type = Type('ast.Node', Object.T)


class ASTString(Object):
    T = Type('ast.String', ast_node_type)

    def __init__(self, string, sigil=None, parseinfo=None):
        if sigil is None:
            sigil = String('')
        self.parseinfo = parseinfo
        super().__init__({'str': string, 'sigil': sigil})
        self.validate()

    def validate(self):
        self.typecheck_attr('str', String)
        self.typecheck_attr('sigil', String)

    def __repr__(self):
        return 'ASTString({}, {})'.format(self.get('str'), self.get('sigil'))


class ASTInterpolatedString(Object):
    T = Type('ast.InterpolatedString', ast_node_type)

    def __init__(self, body, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'body': body})
        self.validate()

    def validate(self):
        self.typecheck_attr('body', List)

    def body_list(self):
        self.validate()
        return self.get('body').elems

    def __repr__(self):
        return 'ASTInterpolatedString({})'.format(self.get('body'))


class ASTIdent(Object):
    T = Type('ast.Ident', ast_node_type)

    def __init__(self, ident, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'ident': ident})
        self.validate()

    def validate(self):
        self.typecheck_attr('ident', String)

    def __repr__(self):
        return 'ASTIdent({})'.format(self.get('ident'))


class ASTInt(Object):
    T = Type('ast.Int', ast_node_type)

    def __init__(self, val, sigil=None, parseinfo=None):
        if sigil is None:
            sigil = String('')
        self.parseinfo = parseinfo
        super().__init__({'int': val, 'sigil': sigil})
        self.validate()

    def validate(self):
        self.typecheck_attr('int', Int)
        self.typecheck_attr('sigil', String)

    def __repr__(self):
        return 'ASTInt({}, {})'.format(self.get('int'), self.get('sigil'))


class ASTFloat(Object):
    T = Type('ast.Float', ast_node_type)

    def __init__(self, val, sigil=None, parseinfo=None):
        if sigil is None:
            sigil = String('')
        self.parseinfo = parseinfo
        super().__init__({'float': val, 'sigil': sigil})
        self.validate()

    def validate(self):
        self.typecheck_attr('float', Float)
        self.typecheck_attr('sigil', String)

    def __repr__(self):
        return 'ASTFloat({}, {})'.format(self.get('float'), self.get('sigil'))


class ASTSymbol(Object):
    T = Type('ast.Symbol', ast_node_type)

    def __init__(self, symbol, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'symbol': symbol})
        self.validate()

    def validate(self):
        self.typecheck_attr('symbol', Symbol)

    def __repr__(self):
        return 'ASTSymbol({})'.format(self.get('symbol'))


class ASTList(Object):
    T = Type('ast.List', ast_node_type)

    def __init__(self, elems, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'elems': elems})
        self.validate()

    def validate(self):
        self.typecheck_attr('elems', List)

    def elems_list(self):
        self.validate()
        return self.get('elems').elems

    def __repr__(self):
        return 'ASTList({})'.format(self.get('elems'))


class ASTBlock(Object):
    T = Type('ast.Block', ast_node_type)

    def __init__(self, statements, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'statements': statements})
        self.validate()

    def validate(self):
        self.typecheck_attr('statements', List)

    def statements_list(self):
        self.validate()
        return self.get('statements').elems

    def __repr__(self):
        return 'ASTBlock({})'.format(self.get('statements'))


class ASTTuple(Object):
    T = Type('ast.Tuple', ast_node_type)

    def __init__(self, elems, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'elems': elems})
        self.validate()

    def validate(self):
        self.typecheck_attr('elems', Tuple)

    def elems_list(self):
        self.validate()
        return self.get('elems').elems

    def __repr__(self):
        return 'ASTTuple({})'.format(self.get('elems'))


class ASTMap(Object):
    T = Type('ast.Map', ast_node_type)

    def __init__(self, elems, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'elems': elems})
        self.validate()

    def validate(self):
        self.typecheck_attr('elems', List)

    def elems_list(self):
        self.validate()
        return self.get('elems').elems

    def __repr__(self):
        return 'ASTMap({})'.format(self.get('elems'))


class ASTCall(Object):
    T = Type('ast.Call', ast_node_type)

    def __init__(self, callable_expr, args, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'callable': callable_expr, 'args': args})
        self.validate()

    def validate(self):
        self.typecheck_attr('args', List)

    def args_list(self):
        self.validate()
        return self.get('args').elems

    def __eq__(self, other):
        def clean_dict(dictionary):
            {k: v for k, v in dictionary.items() if k != 'parseinfo'}
        if type(other) is type(self):
            return clean_dict(self.__dict__) == clean_dict(other.__dict__)
        return False

    def __repr__(self):
        return 'ASTCall({}, {})'.format(self.get('callable'), self.get('args'))


class ASTBinarySlurp(Object):
    T = Type('ast.BinarySlurp', ast_node_type)

    def __init__(self, slurp, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'slurp': slurp})
        self.validate()

    def validate(self):
        self.typecheck_attr('slurp', List)

    def __repr__(self):
        return 'ASTBinarySlurp({})'.format(' '.join(str(e) for e in self.get('slurp').elems))


class ASTUnquote(Object):
    T = Type('ast.Unquote', ast_node_type)

    def __init__(self, expr, parseinfo=None):
        self.parseinfo = parseinfo
        super().__init__({'expr': expr})

    def __repr__(self):
        return 'Unquote({})'.format(self.get('expr'))


def model_to_ast(model):
    if isinstance(model, sem.Ident):
        return ASTIdent(String(model.identifier), parseinfo=model.parseinfo)
    elif isinstance(model, sem.Call):
        return ASTCall(model_to_ast(model.callable_expr), List([model_to_ast(arg) for arg in model.args]),
                       parseinfo=model.parseinfo)
    elif isinstance(model, sem.String):
        return ASTString(String(model.string), String(model.sigil), parseinfo=model.parseinfo)
    elif isinstance(model, sem.InterpolatedString):
        return ASTInterpolatedString(List([model_to_ast(elem) for elem in model.body]),
                                     parseinfo=model.parseinfo)
    elif isinstance(model, sem.Int):
        return ASTInt(Int(model.val), String(model.sigil),
                      parseinfo=model.parseinfo)
    elif isinstance(model, sem.Float):
        return ASTFloat(Float(model.val), String(model.sigil), parseinfo=model.parseinfo)
    elif isinstance(model, sem.List):
        return ASTList(List([model_to_ast(elem) for elem in model.elements]),
                       parseinfo=model.parseinfo)
    elif isinstance(model, sem.Tuple):
        return ASTTuple(Tuple([model_to_ast(elem) for elem in model.elements]),
                        parseinfo=model.parseinfo)
    elif isinstance(model, sem.Map):
        return ASTMap(List([model_to_ast(elem) for elem in model.elements]),
                      parseinfo=model.parseinfo)
    elif isinstance(model, sem.Symbol):
        return ASTSymbol(Symbol(model.symbol),
                         parseinfo=model.parseinfo)
    elif isinstance(model, sem.BinarySlurp):
        return ASTBinarySlurp(List([model_to_ast(elem) for elem in model.slurp]),
                              parseinfo=model.parseinfo)
    elif isinstance(model, sem.Unquote):
        return ASTUnquote(model_to_ast(model.expr),
                          parseinfo=model.parseinfo)
    elif isinstance(model, sem.Block):
        return ASTBlock(List([model_to_ast(statement) for statement in model.statements]),
                        parseinfo=model.parseinfo)
    else:
        raise NotImplementedError(
            'Translation of model node {} to AST not implemented'.format(model))


# ASTString.T = Type('ast.String', ast_node_type)
# ASTInterpolatedString.T = Type('ast.InterpolatedString', ast_node_type)
# ASTIdent.T = Type('ast.Ident', ast_node_type)
# ASTInt.T = Type('ast.Int', ast_node_type)
# ASTFloat.T = Type('ast.Float', ast_node_type)
# ASTSymbol.T = Type('ast.Symbol', ast_node_type)
# ASTList.T = Type('ast.List', ast_node_type)
# ASTTuple.T = Type('ast.Tuple', ast_node_type)
# ASTMap.T = Type('ast.Map', ast_node_type)
# ASTCall.T = Type('ast.Call', ast_node_type)
# ASTBlock.T = Type('ast.Block', ast_node_type)
# ASTUnquote.T = Type('ast.Unquote', ast_node_type)
# ASTBinarySlurp.T = Type('ast.BinarySlurp', ast_node_type)
