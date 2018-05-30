from ..parser import parse

from .types import (
    Object,
    Module,
    Panic,
    PrimFun,
    String,
    Fun,
    Scope,
    Int,
    Float,
    List,
    Tuple,
    Map,
    Bool,
    Symbol,
    Type,
    Nil,
    true,
    false,
    nil,
)

from .types.scope import to_str

from .types.ast import (
    ast_node_type,
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
    model_to_ast,
)

from .funs import (
    get_attr,
    set_attr,
    has_attr,
    let,
    assign,
    panic,
    is_fn,
    attrs,
    puts,
    cond,
    while_fn,
    type_fn,
    is_instance,
    int,
    float,
    bool,
    # list,
    # map,
    # tuple,
    # ast,
    string,
)


class Import(PrimFun):
    def __init__(self):
        super().__init__('prim.import', ['path', 'name'])

    def fun(self, path, name):
        self.typecheck_arg(path, String)
        self.typecheck_arg(name, String)
        with open(path.str, 'r') as f:
            source = f.read()
        import_ast, source_map = parse(source)
        return load_module(import_ast, source_map, name.str, {'prim': prim})


prim = Module('prim', attrs={
    'Type': Type.T,
    'Object': Object.T,
    'PrimFun': PrimFun.T,
    'Fun': Fun.T,
    'Module': Module.T,
    'Scope': Scope.T,
    'String': String.T,
    'List': List.T,
    'Tuple': Tuple.T,
    'Map': Map.T,
    'Int': Int.T,
    'Float': Float.T,
    'Symbol': Symbol.T,
    'Bool': Bool.T,
    'Nil': Nil.T,

    'import': Import(),
    'let': let,
    'assign': assign,
    'panic': panic,
    'is': is_fn,
    'attrs': attrs,
    'cond': cond,
    'while': while_fn,
    'type': type_fn,
    'is_instance': is_instance,
    'puts': puts,
})

prim.set('ast', Module('ast', parent=prim, attrs={
    'Node': ast_node_type,
    'Ident': ASTIdent.T,
    'String': ASTString.T,
    'Int': ASTInt.T,
    'Float': ASTFloat.T,
    'Symbol': ASTSymbol.T,
    'InterpolatedString': ASTInterpolatedString.T,
    'List': ASTList.T,
    'Tuple': ASTTuple.T,
    'Map': ASTMap.T,
    'Call': ASTCall.T,
    'Unquote': ASTUnquote.T,
    'BinarySlurp': ASTBinarySlurp.T,
    'Block': ASTBlock.T,
}))

prim.set('int', Module('int', parent=prim, attrs={
    'add': int.add,
    'sub': int.sub,
    'mul': int.mul,
    'floor_div': int.floor_div,
    'mod': int.mod,
    'pow': int.pow,
    'eq': int.eq,
    'neq': int.neq,
    'lt': int.lt,
    'lte': int.lte,
    'gt': int.gt,
    'gte': int.gte,
}))


prim.set('float', Module('float', parent=prim, attrs={
    'add': float.add,
    'sub': float.sub,
    'mul': float.mul,
    'div': float.div,
    'floor_div': float.floor_div,
    'mod': float.mod,
    'pow': float.pow,
    'eq': float.eq,
    'neq': float.neq,
    'lt': float.lt,
    'lte': float.lte,
    'gt': float.gt,
    'gte': float.gte,
}))

prim.set('bool', Module('list', parent=prim, attrs={
    'and': bool.and_fn,
    'or': bool.or_fn,
}))


prim.set('list', Module('list', parent=prim, attrs={
    # 'get': list.get,
}))


prim.set('tuple', Module('tuple', parent=prim, attrs={
    # 'get': tuple.get,
}))


prim.set('map', Module('map', parent=prim, attrs={
    # 'get': tuple.get,
}))


prim.set('string', Module('string', parent=prim, attrs={
    'concat': string.concat,
}))


builtin_vars = {
    'get_attr': get_attr,
    'set_attr': set_attr,
    'has_attr': has_attr,
    'nil': nil,
    'true': true,
    'false': false,
}

prelude = None


def load_prelude():
    global prelude
    if prelude is None:
        import os
        dirname = os.path.dirname(os.path.abspath(__file__))
        fnm = os.path.join(dirname, '../prelude/prelude.on')
        with open(fnm, 'r') as f:
            source = f.read()
        prelude_ast, source_map = parse(source)
        prelude = load_module(prelude_ast, source_map,
                              'prelude', {'prim': prim})
        if prelude is None:
            raise Exception('Failed to load prelude')


def load_module(statements, source_map, module_name, preload=None, include_prelude=False):
    if preload is None:
        preload = {}
    module = Module(module_name)
    for name, obj in builtin_vars.items():
        module.set(name, obj)
    for name, obj in preload.items():
        module.set(name, obj)
    if include_prelude:
        load_prelude()
        for name, obj in prelude.attrs.items():
            module.set(name, obj)
    try:
        for statement in statements:
            statement = model_to_ast(statement)
            statement = module.preprocess(statement)
            module.eval(statement)
        return module
    except Panic as p:
        parseinfo = statement.parseinfo
        msg = p.msg
        stack = p.stack
        print('=' * 10 + ' Panic: ' + '=' * 10)
        for (fun, info) in reversed(stack):
            if isinstance(fun, PrimFun):
                print('PrimFun `{}` panicked:'.format(
                    fun.name))
            else:
                print('Fun `{}` panicked at statement {}:'.format(
                    fun.name_string(), info['statement_idx']))
                print('    Statement: {}'.format(
                    to_str(module, info['statement'], panic=False)))
            print('    Args: {}'.format(
                ' '.join(to_str(module, a, panic=False) for a in info['args'])))
        if parseinfo is not None:
            print('Module `{}` panicked at line {}:'.format(
                module_name, parseinfo.line + 1))
        else:
            print('Module `{}` panicked:')
        if isinstance(statement, Object):
            print('    Statement: {}'.format(to_str(module, statement)))
        print('    Panic: {}'.format(msg))
        return None
