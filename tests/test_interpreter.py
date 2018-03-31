from obsidian.parser import parse
from obsidian.interpreter import load_module, prim


def get_output(source, capsys):
    load_module(parse(source), 'test', {'prim': prim})
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
    (let 'newputs' (get_attr prim 'puts'))
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


def test_module_name(capsys):
    source = '''
    (get_attr prim 'puts') (get_attr meta 'name')
    '''
    target = ['test']
    assert get_output(source, capsys) == target
