from obsidian.parser import parse
from obsidian.interpreter import load_module
from textwrap import dedent


def get_output(source, capsys):
    ast, source_map = parse(dedent(source))
    load_module(ast, source_map, 'test', include_prelude=True)
    out, err = capsys.readouterr()
    return out.splitlines()


def test_dot(capsys):
    source = '''
    prim.puts 'Hello, World!'
    '''
    target = ['Hello, World!']
    assert get_output(source, capsys) == target
