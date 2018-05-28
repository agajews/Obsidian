from .types import (
    Module,
    fun_type,
    scope_type,
    module_type,
    int_type,
    float_type,
    list_type,
    tuple_type,
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
    ast_call_type,
    ast_binary_slurp_type,
    ast_symbol_type,
    ast_unquote_type,
)
from .funs import (
    get_attr,
    set_attr,
    let,
    puts,
    cond,
    int,
    float,
    list,
    string,
)


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
    'Int': int_type,
    'Float': float_type,
    'Symbol': symbol_type,
    'Bool': bool_type,
    'Nil': nil_type,

    'let': let,
    'cond': cond,
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
    # 'Map': ASTMapType,
    'Call': ast_call_type,
    'Unquote': ast_unquote_type,
    'BinarySlurp': ast_binary_slurp_type,
    # 'Block': ASTBlockType,
    # 'Trailed': ast_trailed_type
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
}))


prim.set('list', Module('list', parent=prim, attrs={
    'get': list.get,
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


def load_module(statements, source_map, name, preload=None):
    if preload is None:
        preload = {}
    module = Module(name)
    for name, obj in builtin_vars.items():
        module.set(name, obj)
    for name, obj in preload.items():
        module.set(name, obj)
    for statement in statements:
        statement = model_to_ast(statement)
        statement = module.preprocess(statement)
        module.eval(statement)
