from ..parser import parse

from .types import (
    Module,
    Panic,
    PrimFun,
    String,
    fun_type,
    scope_type,
    module_type,
    int_type,
    float_type,
    list_type,
    tuple_type,
    map_type,
    bool_type,
    true,
    false,
    symbol_type,
    type_type,
    string_type,
    object_type,
    prim_fun_type,
    meta_type,
    nil_type,
    nil,
)

from .types.ast import (
    model_to_ast,
    ast_node_type,
    ast_ident_type,
    ast_string_type,
    ast_interpolated_string_type,
    ast_int_type,
    ast_float_type,
    ast_list_type,
    ast_tuple_type,
    ast_map_type,
    ast_call_type,
    ast_binary_slurp_type,
    ast_symbol_type,
    ast_unquote_type,
    ast_block_type,
    ast_trailed_type,
)

from .funs import (
    get_attr,
    set_attr,
    let,
    assign,
    panic,
    is_fn,
    attrs,
    puts,
    cond,
    while_fn,
    object,
    int,
    float,
    list,
    map,
    tuple,
    string,
)


class Import(PrimFun):
    def __init__(self):
        super().__init__('prim.import', ['path', 'name'])

    def fun(self, path, name):
        if not isinstance(path, String):
            raise Panic('Path must be a string')
        if not isinstance(name, String):
            raise Panic('Name must be a string')
        with open(path.str, 'r') as f:
            source = f.read()
        ast, source_map = parse(source)
        return load_module(ast, source_map, name.str, {'prim': prim})


prim = Module('prim', attrs={
    'Type': type_type,
    'Object': object_type,
    'Meta': meta_type,
    'PrimFun': prim_fun_type,
    'Fun': fun_type,
    'Module': module_type,
    'Scope': scope_type,
    'String': string_type,
    'List': list_type,
    'Tuple': tuple_type,
    'Map': map_type,
    'Int': int_type,
    'Float': float_type,
    'Symbol': symbol_type,
    'Bool': bool_type,
    'Nil': nil_type,

    'import': Import(),
    'let': let,
    'assign': assign,
    'panic': panic,
    'is': is_fn,
    'attrs': attrs,
    'cond': cond,
    'while': while_fn,
    'puts': puts,
})

prim.set('ast', Module('ast', parent=prim, attrs={
    'Node': ast_node_type,
    'Ident': ast_ident_type,
    'String': ast_string_type,
    'Int': ast_int_type,
    'Float': ast_float_type,
    'Symbol': ast_symbol_type,
    'InterpolatedString': ast_interpolated_string_type,
    'List': ast_list_type,
    'Tuple': ast_tuple_type,
    'Map': ast_map_type,
    'Call': ast_call_type,
    'Unquote': ast_unquote_type,
    'BinarySlurp': ast_binary_slurp_type,
    'Block': ast_block_type,
    'Trailed': ast_trailed_type,
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
    'nil': nil,
    'true': true,
    'false': false,
}


def load_module(statements, source_map, module_name, preload=None):
    if preload is None:
        preload = {}
    module = Module(module_name)
    for name, obj in builtin_vars.items():
        module.set(name, obj)
    for name, obj in preload.items():
        module.set(name, obj)
    try:
        for statement in statements:
            statement = model_to_ast(statement)
            statement = module.preprocess(statement)
            module.eval(statement)
        return module
    except Panic as p:
        if p.parseinfo is not None:
            print('Module `{}` panicked at line {}:'.format(
                module_name, p.parseinfo.line + 1))
            print('Panic: {}'.format(p.msg))
        else:
            print('Panic: {}'.format(p.msg))
