from obsidian.parser import parse
from obsidian.interpreter import load_module, prim
from textwrap import dedent


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
    (let 'puts' (get_attr prim 'puts'))
    let 'hello' (Fun 'hello' [(puts 'Hello, World!')])
    (hello)
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_panic(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    (let 'Fun' (get_attr prim 'Fun'))
    (let 'puts' (get_attr prim 'puts'))
    (let 'panic' (get_attr prim 'panic'))
    let 'danger' (Fun 'danger' [(panic 'Panicking')])
    (danger)
    '''
    target = ['Module `test` panicked at line 7:', 'Panic: Panicking']
    assert get_output(source, capsys) == target


def test_return(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    (let 'Fun' (get_attr prim 'Fun'))
    (let 'puts' (get_attr prim 'puts'))
    let 'fn' (Fun 'fn' [(puts 'Hello'), (return 'People'), (puts 'Yay!')])
    puts (fn)
    '''
    target = ['Hello', 'People']
    assert get_output(source, capsys) == target


def test_return_nested(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    (let 'Fun' (get_attr prim 'Fun'))
    (let 'puts' (get_attr prim 'puts'))
    let 'fn1' (Fun 'fn1' [(puts 'You'), (return 'All'), (puts 'Yay!')])
    let 'fn2' (Fun 'fn2' [(puts 'Hello'), (return (fn1)), (puts 'Yay!')])
    puts (fn2)
    '''
    target = ['Hello', 'You', 'All']
    assert get_output(source, capsys) == target


def test_is(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    (let 'puts' (get_attr prim 'puts'))
    (let 'is' (get_attr prim 'is'))
    let 'x' 3
    puts x ~is x
    let 'y' 3
    puts x ~is y
    '''
    target = ['true', 'false']
    assert get_output(source, capsys) == target


def test_attrs(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    (let 'puts' (get_attr prim 'puts'))
    (let 'attrs' (get_attr prim 'attrs'))
    puts (attrs 'str')
    let 'x' 3
    (set_attr x 'a' 'b')
    puts (attrs x)
    '''
    target = ['[meta]', '[meta, a]']
    assert get_output(source, capsys) == target


def test_eval(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    (let 'ast' (get_attr prim 'ast'))
    (let 'ASTCall' (get_attr ast 'Call'))
    (let 'ASTIdent' (get_attr ast 'Ident'))
    (let 'ASTString' (get_attr ast 'String'))
    (let 'puts' (get_attr prim 'puts'))
    (get_attr meta 'eval') (ASTCall (ASTIdent 'puts') [(ASTString 'Hello, World!' '')])
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_assign(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'assign' (get_attr prim 'assign')
    let 'x' 'hi'
    puts x
    assign 'x' 'bye'
    puts x
    '''
    target = ['hi', 'bye']
    assert get_output(source, capsys) == target


def test_block(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'Fun' (get_attr prim 'Fun')
    let 'puts' (get_attr prim 'puts')
    let 'while' (get_attr prim 'while')
    let 'assign' (get_attr prim 'assign')
    let '-' (get_attr (get_attr prim 'int') 'sub')
    let '>=' (get_attr (get_attr prim 'int') 'gte')
    let 'run' (Fun 'run' [
        (let 'statements' (get_attr ((get_attr (get_attr meta 'args') 'get') 0) 'statements')),
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'n_args' ((get_attr statements 'len'))),
        (let 'i' n_args - 1),
        (while i >= 0 [
            (eval ((get_attr statements 'get') i)),
            (assign 'i' i - 1)
        ]),
    ])
    run
        puts 'Hello, World!'
        puts 'Hi again'
    '''
    target = ['Hi again', 'Hello, World!']
    assert get_output(source, capsys) == target


def test_block_global_i(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'Fun' (get_attr prim 'Fun')
    let 'puts' (get_attr prim 'puts')
    let 'while' (get_attr prim 'while')
    let 'assign' (get_attr prim 'assign')
    let '+' (get_attr (get_attr prim 'int') 'add')
    let '<' (get_attr (get_attr prim 'int') 'lt')
    let 'i' 0
    let 'run' (Fun 'run' [
        (let 'statements' (get_attr ((get_attr (get_attr meta 'args') 'get') 0) 'statements')),
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'n_args' ((get_attr statements 'len'))),
        (while i < n_args [
            (eval ((get_attr statements 'get') i)),
            (assign 'i' i + 1)
        ]),
    ])
    run
        puts 'Hello, World!'
        puts 'Hi again'
    puts ((get_attr i 'to_str'))
    '''
    target = ['Hello, World!', 'Hi again', '2']
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


def test_list_get(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'list' [1, 2, 3]
    puts ((get_attr ((get_attr list 'get') 1) 'to_str'))
    '''
    target = ['2']
    assert get_output(source, capsys) == target


def test_tuple_get(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'tuple' (1, 2, 3)
    puts ((get_attr ((get_attr tuple 'get') 1) 'to_str'))
    '''
    target = ['2']
    assert get_output(source, capsys) == target


def test_map_get(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {(1, 'dogs'), (2, 'fish'), (3, 'horses')}
    puts ((get_attr map 'get') 3)
    '''
    target = ['horses']
    assert get_output(source, capsys) == target


def test_list_trailed_get(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'list' [1, 2, 3]
    puts ((get_attr list[2] 'to_str'))
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_tuple_trailed_get(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'tuple' (1, 2, 3)
    puts ((get_attr tuple[0] 'to_str'))
    '''
    target = ['1']
    assert get_output(source, capsys) == target


def test_map_trailed_get_string_key(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {('dogs', 1), ('fish', 2), ('horses', 3)}
    puts ((get_attr map['fish'] 'to_str'))
    '''
    target = ['2']
    assert get_output(source, capsys) == target


def test_map_trailed_get_int_key(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {(1, 'dogs'), (2, 'fish'), (3, 'horses')}
    puts map[1]
    '''
    target = ['dogs']
    assert get_output(source, capsys) == target


def test_map_trailed_get_float_key(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {(1.0, 'dogs'), (2.0, 'fish'), (3.0, 'horses')}
    puts map[1.0]
    '''
    target = ['dogs']
    assert get_output(source, capsys) == target


def test_map_trailed_get_symbol_key(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {(@fuzzy, 'dogs'), (@scaly, 'fish'), (@runny, 'horses')}
    puts map[@fuzzy]
    '''
    target = ['dogs']
    assert get_output(source, capsys) == target


def test_list_set(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'list' [1, 2, 3]
    puts list
    ((get_attr list 'set') 2 4)
    puts list
    '''
    target = ['[1, 2, 3]', '[1, 2, 4]']
    assert get_output(source, capsys) == target


def test_map_set(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {('dogs', 1), ('fish', 2), ('horses', 3)}
    puts map
    ((get_attr map 'set') 'horses' 4)
    puts map['horses']
    puts map
    '''
    target = ['{dogs -> 1, fish -> 2, horses -> 3}',
              '4',
              '{dogs -> 1, fish -> 2, horses -> 4}']
    assert get_output(source, capsys) == target


def test_map_set_add(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'map' {('dogs', 1), ('fish', 2), ('horses', 3)}
    puts map
    ((get_attr map 'set') 'whales' 8)
    puts map['whales']
    puts map
    '''
    target = ['{dogs -> 1, fish -> 2, horses -> 3}',
              '8',
              '{dogs -> 1, fish -> 2, horses -> 3, whales -> 8}']
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


def test_float_implicit_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts 3.0
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


def test_symbol_implicit_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts @hello
    '''
    target = ['@hello']
    assert get_output(source, capsys) == target


def test_list_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr [1, 2, 3] 'to_str'))
    '''
    target = ['[1, 2, 3]']
    assert get_output(source, capsys) == target


def test_list_to_str_implicit(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts [1, 2, 3]
    '''
    target = ['[1, 2, 3]']
    assert get_output(source, capsys) == target


def test_tuple_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr (1, 2, 3) 'to_str'))
    '''
    target = ['(1, 2, 3)']
    assert get_output(source, capsys) == target


def test_tuple_to_str_implicit(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts (1, 2, 3)
    '''
    target = ['(1, 2, 3)']
    assert get_output(source, capsys) == target


def test_map_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr {(1, 'dogs'), (2, 'fish'), (3, 'horses')} 'to_str'))
    '''
    target = ['{1 -> dogs, 2 -> fish, 3 -> horses}']
    assert get_output(source, capsys) == target


def test_map_to_str_implicit(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts {(1, 'dogs'), (2, 'fish'), (3, 'horses')}
    '''
    target = ['{1 -> dogs, 2 -> fish, 3 -> horses}']
    assert get_output(source, capsys) == target


def test_unquote(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    (let 'ast' (get_attr prim 'ast'))
    (let 'ASTIdent' (get_attr ast 'Ident'))
    $(ASTIdent 'puts') 'Hello, World!'
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_unquote_double(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    (let 'ast' (get_attr prim 'ast'))
    (let 'ASTIdent' (get_attr ast 'Ident'))
    let 'puts_node' (ASTIdent 'puts')
    $$(ASTIdent 'puts_node') 'Hello, World!'
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_unquote_nested(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    (let 'ast' (get_attr prim 'ast'))
    (let 'ASTIdent' (get_attr ast 'Ident'))
    (let 'ASTString' (get_attr ast 'String'))
    let 'puts_str' (ASTString 'puts' '')
    $(ASTIdent $puts_str) 'Hello, World!'
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_string_to_str(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts ((get_attr 'Hello, World!' 'to_str'))
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target


def test_string_decoding(capsys):
    source = r'''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts 'hello\nworld'
    '''
    target = ['hello', 'world']
    assert get_output(source, capsys) == target


def test_string_r_sigil(capsys):
    source = r'''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    puts r'hello\nworld'
    '''
    target = [r'hello\nworld']
    assert get_output(source, capsys) == target


def test_interpolated_string(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'name' 'Alex'
    puts "Hello, ${name}!"
    '''
    target = ['Hello, Alex!']
    assert get_output(source, capsys) == target


def test_triple_interpolated_string(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'name' 'Alex'
    puts """Hello, ${name}!"""
    '''
    target = ['Hello, Alex!']
    assert get_output(source, capsys) == target


def test_interpolated_string_int(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'name' 'Alex'
    let 'n_dogs' 3
    puts "Hello $name, I have $n_dogs dogs!"
    '''
    target = ['Hello Alex, I have 3 dogs!']
    assert get_output(source, capsys) == target


def test_triple_interpolated_string_int(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'name' 'Alex'
    let 'n_dogs' 3
    puts """Hello $name, I have $n_dogs dogs!"""
    '''
    target = ['Hello Alex, I have 3 dogs!']
    assert get_output(source, capsys) == target


def test_interpolated_string_symbol(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'name' 'Alex'
    let 'associativity' @left
    puts "Hello $name, my associativity is ${associativity}!"
    '''
    target = ['Hello Alex, my associativity is @left!']
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


def test_int_lt_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_lt' (get_attr int 'lt')
    puts ((get_attr (int_lt 2 3 4) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_int_lt_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_lt' (get_attr int 'lt')
    puts ((get_attr (int_lt 2 3 3) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_int_lte_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_lte' (get_attr int 'lte')
    puts ((get_attr (int_lte 2 3 3) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_int_lte_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_lte' (get_attr int 'lte')
    puts ((get_attr (int_lte 2 3 2) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_int_gt_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_gt' (get_attr int 'gt')
    puts ((get_attr (int_gt 4 3 2) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_int_gt_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_gt' (get_attr int 'gt')
    puts ((get_attr (int_gt 4 4 3) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_int_gte_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_gte' (get_attr int 'gte')
    puts ((get_attr (int_gte 4 4 3) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_int_gte_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'int' (get_attr prim 'int')
    let 'int_gte' (get_attr int 'gte')
    puts ((get_attr (int_gte 4 4 5) 'to_str'))
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


def test_float_lt_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_lt' (get_attr float 'lt')
    puts ((get_attr (float_lt 2.0 3.0 4.0) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_float_lt_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_lt' (get_attr float 'lt')
    puts ((get_attr (float_lt 2.0 3.0 3.0) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_float_lte_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_lte' (get_attr float 'lte')
    puts ((get_attr (float_lte 2.0 3.0 3.0) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_float_lte_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_lte' (get_attr float 'lte')
    puts ((get_attr (float_lte 2.0 3.0 2.0) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_float_gt_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_gt' (get_attr float 'gt')
    puts ((get_attr (float_gt 4.0 3.0 2.0) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_float_gt_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_gt' (get_attr float 'gt')
    puts ((get_attr (float_gt 4.0 4.0 3.0) 'to_str'))
    '''
    target = ['false']
    assert get_output(source, capsys) == target


def test_float_gte_true(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_gte' (get_attr float 'gte')
    puts ((get_attr (float_gte 4.0 4.0 3.0) 'to_str'))
    '''
    target = ['true']
    assert get_output(source, capsys) == target


def test_float_gte_false(capsys):
    source = '''
    ((get_attr prim 'let') 'let' (get_attr prim 'let'))  # import let
    let 'puts' (get_attr prim 'puts')
    let 'float' (get_attr prim 'float')
    let 'float_gte' (get_attr float 'gte')
    puts ((get_attr (float_gte 4.0 4.0 5.0) 'to_str'))
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
    puts butch
    '''
    target = ['Woof!', '<Dog>']
    assert get_output(source, capsys) == target


def test_int_sigil(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Object' (get_attr prim 'Object')
    let 'Int' (get_attr prim 'Int')
    let 'Type' (get_attr prim 'Type')
    let 'Fun' (get_attr prim 'Fun')
    let 'Im' (Type 'Im' Object)
    let 'concat' (get_attr (get_attr prim 'string') 'concat')
    set_attr Im 'call' (Fun 'Im' [
        (let 'self' (Object Im)),
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'val' (eval (get_attr meta 'args')[0])),
        (set_attr self 'val' val),
        self,
    ])
    set_attr (get_attr Im 'methods') 'to_str' (Fun 'Im.to_str' [
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'self' (eval (get_attr meta 'args')[0])),
        (let 'val_str' ((get_attr (get_attr self 'val') 'to_str'))),
        (concat val_str 'i'),
    ])
    let 'num' (Im 3)
    puts num
    ((get_attr (get_attr Int 'sigils') 'set') 'i' Im)
    let 'num2' 4i
    puts num2
    '''
    target = ['3i', '4i']
    assert get_output(source, capsys) == target


def test_float_sigil(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Object' (get_attr prim 'Object')
    let 'Float' (get_attr prim 'Float')
    let 'Type' (get_attr prim 'Type')
    let 'Fun' (get_attr prim 'Fun')
    let 'Im' (Type 'Im' Object)
    let 'concat' (get_attr (get_attr prim 'string') 'concat')
    set_attr Im 'call' (Fun 'Im' [
        (let 'self' (Object Im)),
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'val' (eval (get_attr meta 'args')[0])),
        (set_attr self 'val' val),
        self,
    ])
    set_attr (get_attr Im 'methods') 'to_str' (Fun 'Im.to_str' [
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'self' (eval (get_attr meta 'args')[0])),
        (let 'val_str' ((get_attr (get_attr self 'val') 'to_str'))),
        (concat val_str 'i'),
    ])
    let 'num' (Im 3.0)
    puts num
    ((get_attr (get_attr Float 'sigils') 'set') 'i' Im)
    let 'num2' 4.0i
    puts num2
    '''
    target = ['3.0i', '4.0i']
    assert get_output(source, capsys) == target


def test_string_sigil(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Object' (get_attr prim 'Object')
    let 'String' (get_attr prim 'String')
    let 'Type' (get_attr prim 'Type')
    let 'Fun' (get_attr prim 'Fun')
    let 'FunnyString' (Type 'FunnyString' Object)
    set_attr FunnyString 'call' (Fun 'FunnyString' [
        (let 'self' (Object FunnyString)),
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'string' (eval (get_attr meta 'args')[0])),
        (set_attr self 'string' string),
        self,
    ])
    set_attr (get_attr FunnyString 'methods') 'to_str' (Fun 'FunnyString.to_str' [
        (let 'eval' (get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval')),
        (let 'self' (eval (get_attr meta 'args')[0])),
        "haha $(get_attr self 'string')"
    ])
    let 's' (FunnyString 'I like cheese')
    puts s
    ((get_attr (get_attr String 'sigils') 'set') 'f' FunnyString)
    let 's2' f'I also like cheese'
    puts s2
    '''
    target = ['haha I like cheese', 'haha I also like cheese']
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
    output = get_output(source, capsys)
    assert output == ['Module `test` panicked at line 10:',
                      'Panic: Object has no attribute species']


def test_methods(capsys):
    source = '''
    (get_attr prim 'let') 'let' (get_attr prim 'let')  # import let
    let 'puts' (get_attr prim 'puts')
    let 'Fun' (get_attr prim 'Fun')
    let 'Object' (get_attr prim 'Object')
    let 'Type' (get_attr prim 'Type')
    let 'Dog' (Type 'Dog' Object)
    let 'string' (get_attr prim 'string')
    let 'strcat' (get_attr string 'concat')
    set_attr (get_attr Dog 'methods') 'greet' (Fun 'greet' [
        (let 'raw_name' ((get_attr (get_attr meta 'args') 'get') 1)),
        (let 'name' ((get_attr (get_attr (get_attr meta 'caller') 'meta') 'eval') raw_name)),
        (puts (strcat 'Woof ' name '!')),
    ])
    let 'butch' (Object Dog)
    ((get_attr butch 'greet') 'Jim')
    '''
    target = ['Woof Jim!']
    assert get_output(source, capsys) == target
