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
    (let 'ast' (get_attr prim 'ast'))
    (let 'ASTCall' (get_attr ast 'Call'))
    (let 'ASTIdent' (get_attr ast 'Ident'))
    (let 'ASTString' (get_attr ast 'String'))
    (let 'puts' (get_attr prim 'puts'))
    (let 'hello' (Fun [(ASTCall (ASTIdent 'puts') [(ASTString 'Hello, World!')])]))
    (hello)
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target
