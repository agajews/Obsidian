from .bootstrap import (
    type_type, string_type, object_type, prim_fun_type, meta_type, nil_type,
    nil
)
from .types import (
    Module,
    fun_type, scope_type, module_type, int_type, list_type,
)
from .types.ast import (
    model_to_ast,
    ast_node_type, ast_ident_type, ast_string_type, ast_int_type, ast_list_type,
    ast_call_type, ast_binary_slurp_type,
)
from .funs import (
    get_attr, set_attr, let, puts
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
    'Int': int_type,

    'Nil': nil_type,
    'nil': nil,

    'let': let,

    'puts': puts,
})

prim.set('ast', Module('ast', parent=prim, attrs={
    'Node': ast_node_type,
    'Ident': ast_ident_type,
    'String': ast_string_type,
    'Int': ast_int_type,
    # 'Float': ASTFloatType,
    # 'InterpolatedString': ASTInterpolatedStringType,
    # 'Symbol': ASTSymbolType,
    'List': ast_list_type,
    # 'Tuple': ASTTupleType,
    # 'Map': ASTMapType,
    'Call': ast_call_type,

    # 'Unquote': ASTUnquoteType,
    # 'Binary': ASTBinaryType,
    'BinarySlurp': ast_binary_slurp_type,
    # 'Block': ASTBlockType,
}))


builtin_vars = {
    'get_attr': get_attr,
    'set_attr': set_attr,
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
        module.eval(model_to_ast(statement))
