from obsidian.parser import parse
from obsidian.interpreter import load_module, prim
from obsidian.interpreter.types import Panic
from textwrap import dedent
import pytest


def get_output(source, capsys):
    ast, source_map = parse(dedent(source))
    load_module(ast, source_map, 'test', {'prim': prim})
    out, err = capsys.readouterr()
    return out.splitlines()


def test_hello(capsys):
    source = '''
    (get_attr prim 'puts') "Hello, World!"
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_let(capsys):
    source = '''
    ((get_attr prim 'let') 'newputs' (get_attr prim 'puts'))
    newputs "Hello, World!"
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_set_attr(capsys):
    source = '''
    (set_attr prim 'newputs' (get_attr prim 'puts'))
    (get_attr prim 'newputs') "Hello, World!"
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_call_string(capsys):
    source = '''
    (get_attr prim 'puts') ((get_attr prim 'String') "Hello, World!")
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_type_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'Type') 'name')
    '''
    target = ['Type']
    assert get_output(source, capsys) == target


def test_object_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'Object') 'name')
    '''
    target = ['Object']
    assert get_output(source, capsys) == target


def test_fun_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'Fun') 'name')
    '''
    target = ['Fun']
    assert get_output(source, capsys) == target


def test_module_type_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'Module') 'name')
    '''
    target = ['Module']
    assert get_output(source, capsys) == target


def test_primfun_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'PrimFun') 'name')
    '''
    target = ['PrimFun']
    assert get_output(source, capsys) == target


def test_string_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'String') 'name')
    '''
    target = ['String']
    assert get_output(source, capsys) == target


def test_meta_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr prim 'Meta') 'name')
    '''
    target = ['Meta']
    assert get_output(source, capsys) == target


def test_meta_type(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr (get_attr (get_attr meta 'meta') 'type') 'name')
    '''
    target = ['Meta']
    assert get_output(source, capsys) == target


def test_module_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr meta 'name')
    '''
    target = ['test']
    assert get_output(source, capsys) == target


def test_fun(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    (let 'Fun' (get_attr prim 'Fun'))
    (let 'ast' (get_attr prim 'ast'))
    (let 'puts' (get_attr prim 'puts'))
    let 'hello' (Fun 'hello' [(puts 'Hello, World!')])
    (hello)
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_eval(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    (let 'ast' (get_attr prim 'ast'))
    (let 'ASTCall' (get_attr ast 'Call'))
    (let 'ASTIdent' (get_attr ast 'Ident'))
    (let 'ASTString' (get_attr ast 'String'))
    (let 'puts' (get_attr prim 'puts'))
    (get_attr meta 'eval') (ASTCall (ASTIdent 'puts') [(ASTString 'Hello, World!' nil)])
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_scope(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 's' 'test_str'
    puts (get_attr (get_attr meta 'scope') 's')
    '''
    target = ['test_str']
    assert get_output(source, capsys) == target


def test_list(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'l' [1, 2, 3]
    let 'list' (get_attr prim 'list')
    let 'list_get' (get_attr list 'get')
    puts ((get_attr (list_get l 1) 'to_str'))
    '''
    target = ['2']
    assert get_output(source, capsys) == target


def test_int(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr 3 'to_str'))
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_float(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr 3.0 'to_str'))
    '''
    target = ['3.0']
    assert get_output(source, capsys) == target


def test_symbol(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr @hello 'to_str'))
    '''
    target = ['@hello']
    assert get_output(source, capsys) == target


def test_string_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr 'Hello, World!' 'to_str'))
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_bool_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr true 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_bool_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr false 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_int_add(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_add' (get_attr int 'add')
    puts ((get_attr (int_add 1 2) 'to_str'))
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_int_sub(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_sub' (get_attr int 'sub')
    puts ((get_attr (int_sub 10 2) 'to_str'))
    '''
    target = ['8']
    assert get_output(source, capsys) == target


def test_int_mul(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_mul' (get_attr int 'mul')
    puts ((get_attr (int_mul 2 2) 'to_str'))
    '''
    target = ['4']
    assert get_output(source, capsys) == target


def test_int_floor_div(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_floor_div' (get_attr int 'floor_div')
    puts ((get_attr (int_floor_div 10 4) 'to_str'))
    '''
    target = ['2']
    assert get_output(source, capsys) == target


def test_int_mod(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_mod' (get_attr int 'mod')
    puts ((get_attr (int_mod 11 4) 'to_str'))
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_int_pow(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_pow' (get_attr int 'pow')
    puts ((get_attr (int_pow 2 5) 'to_str'))
    '''
    target = ['32']
    assert get_output(source, capsys) == target


def test_int_eq_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_eq' (get_attr int 'eq')
    puts ((get_attr (int_eq 2 2 2) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_int_eq_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_eq' (get_attr int 'eq')
    puts ((get_attr (int_eq 2 2 4) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_int_neq_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_neq' (get_attr int 'neq')
    puts ((get_attr (int_neq 2 4 2) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_int_neq_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_neq' (get_attr int 'neq')
    puts ((get_attr (int_neq 2 2 2) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_float_add(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_add' (get_attr float 'add')
    puts ((get_attr (float_add 1.0 2.0) 'to_str'))
    '''
    target = ['3.0']
    assert get_output(source, capsys) == target


def test_float_sub(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_sub' (get_attr float 'sub')
    puts ((get_attr (float_sub 10.0 2.0) 'to_str'))
    '''
    target = ['8.0']
    assert get_output(source, capsys) == target


def test_float_mul(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_mul' (get_attr float 'mul')
    puts ((get_attr (float_mul 2.0 2.0) 'to_str'))
    '''
    target = ['4.0']
    assert get_output(source, capsys) == target


def test_float_div(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_div' (get_attr float 'div')
    puts ((get_attr (float_div 4.0 2.0) 'to_str'))
    '''
    target = ['2.0']
    assert get_output(source, capsys) == target


def test_float_floor_div(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_floor_div' (get_attr float 'floor_div')
    puts ((get_attr (float_floor_div 10.0 4.0) 'to_str'))
    '''
    target = ['2.0']
    assert get_output(source, capsys) == target


def test_float_mod(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_mod' (get_attr float 'mod')
    puts ((get_attr (float_mod 11.0 4.0) 'to_str'))
    '''
    target = ['3.0']
    assert get_output(source, capsys) == target


def test_float_pow(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_pow' (get_attr float 'pow')
    puts ((get_attr (float_pow 2.0 5.0) 'to_str'))
    '''
    target = ['32.0']
    assert get_output(source, capsys) == target


def test_float_eq_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_eq' (get_attr float 'eq')
    puts ((get_attr (float_eq 2.0 2.0 2.0) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_float_eq_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_eq' (get_attr float 'eq')
    puts ((get_attr (float_eq 2.0 2.0 4.0) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_float_neq_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_neq' (get_attr float 'neq')
    puts ((get_attr (float_neq 2.0 4.0 2.0) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_float_neq_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_neq' (get_attr float 'neq')
    puts ((get_attr (float_neq 2.0 2.0 2.0) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_binary_int_add(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_add' (get_attr int 'add')
    puts ((get_attr 1 ~int_add 2 'to_str'))
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_binary_int_precedence(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_add' (get_attr int 'add')
    let 'int_mul' (get_attr int 'mul')
    puts ((get_attr 1 ~int_add 2 ~int_mul 2 ~int_add 5 'to_str'))
    '''
    target = ['10']
    assert get_output(source, capsys) == target


def test_binary_int_associativity(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_add' (get_attr int 'add')
    let 'int_pow' (get_attr int 'pow')
    puts ((get_attr 1 ~int_add 4 ~int_pow 2 ~int_pow 3 'to_str'))
    '''
    target = ['65537']
    assert get_output(source, capsys) == target


def test_binary_int_no_associativity(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'plus' (get_attr int 'add')
    let 'pow' (get_attr int 'pow')
    let 'eq' (get_attr int 'eq')
    puts ((get_attr 2 ~plus 6 ~eq 2 ~pow 3 ~eq 8 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_binary_ops(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let '+' (get_attr int 'add')
    let '^' (get_attr int 'pow')
    let '==' (get_attr int 'eq')
    puts ((get_attr 2 + 6 == 2^3 == 8 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_binary_op_neq(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let '+' (get_attr int 'add')
    let '^' (get_attr int 'pow')
    let '!=' (get_attr int 'neq')
    puts ((get_attr 2 + 5 != 2^3 != 7 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_cond(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'cond' (get_attr prim 'cond')
    let 'int' (get_attr prim 'int')
    let '+' (get_attr int 'add')
    let '==' (get_attr int 'eq')
    puts (cond (1 + 1 == 2, 'Math works'))
    '''
    target = ['Math works']
    assert get_output(source, capsys) == target


def test_cond_multi(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'cond' (get_attr prim 'cond')
    let 'int' (get_attr prim 'int')
    let '+' (get_attr int 'add')
    let '==' (get_attr int 'eq')
    let '!=' (get_attr int 'neq')
    puts (cond (1 + 1 != 2, 'Math is broken') (2 + 2 == 4,
          'Math works') (1 + 1 == 2, 'Math still works'))
    '''
    target = ['Math works']
    assert get_output(source, capsys) == target


def test_cond_lazy(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'cond' (get_attr prim 'cond')
    let 'int' (get_attr prim 'int')
    let '+' (get_attr int 'add')
    let '==' (get_attr int 'eq')
    let '!=' (get_attr int 'neq')
    cond (1 + 1 != 2, (puts 'Math is broken')) (2 + 2 == 4, (puts 'Math works')) (1 + 1 == 2, (puts 'Math still works'))
    '''
    target = ['Math works']
    assert get_output(source, capsys) == target


def test_types(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    set_attr (get_attr Dog 'methods') 'bark' (Fun 'bark' [(puts 'Woof!')])
    let 'butch' (Object Dog)
    ((get_attr butch 'bark'))
    '''
    target = ['Woof!']
    assert get_output(source, capsys) == target


def test_inheritance(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    set_attr (get_attr Dog 'methods') 'bark' (Fun 'bark' [(puts 'Woof!')])
    let 'Beagle' (Type 'Beagle' Dog)
    let 'butch' (Object Beagle)
    ((get_attr butch 'bark'))
    '''
    target = ['Woof!']
    assert get_output(source, capsys) == target


def test_statics(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    set_attr (get_attr Dog 'statics') 'species' 'C. lupus'
    let 'butch' (Object Dog)
    puts (get_attr butch 'species')
    '''
    target = ['C. lupus']
    assert get_output(source, capsys) == target


def test_statics_inheritance(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    set_attr (get_attr Dog 'statics') 'species' 'C. lupus'
    let 'Beagle' (Type 'Beagle' Dog)
    let 'butch' (Object Beagle)
    puts (get_attr butch 'species')
    '''
    target = ['C. lupus']
    assert get_output(source, capsys) == target


def test_statics_inheritance_missing(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    let 'Beagle' (Type 'Beagle' Dog)
    let 'butch' (Object Beagle)
    puts (get_attr butch 'species')
    '''
    with pytest.raises(Panic):
        get_output(source, capsys)


def test_methods(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    let 'list' (get_attr prim 'list')
    let 'list_get' (get_attr list 'get')
    let 'string' (get_attr prim 'string')
    let 'strcat' (get_attr string 'concat')
    set_attr (get_attr Dog 'methods') 'greet' (Fun 'greet' [
        (let 'raw_name' (list_get (get_attr meta 'args') 1)),
        (let 'name' ((get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval') raw_name)),
        (puts (strcat 'Woof ' name '!')),
    ])
    let 'butch' (Object Dog)
    ((get_attr butch 'greet') 'Jim')
    '''
    target = ['Woof Jim!']
    assert get_output(source, capsys) == target
