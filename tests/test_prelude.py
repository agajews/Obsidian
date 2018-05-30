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


def test_dot_multiple(capsys):
    source = '''
    prim.puts (prim.int.add 1 2)
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_dot_list(capsys):
    source = '''
    prim.puts [1, 2, 3].[1]
    '''
    target = ['2']
    assert get_output(source, capsys) == target


def test_dot_list_panic(capsys):
    source = '''
    prim.puts [1, 2, 3].[1, 2]
    '''
    target = ['========== Panic: ==========',
              'PrimFun `prim.puts` panicked:',
              '    Args: (. [1, 2, 3] [1, 2])',
              'Fun `prelude.{.}` panicked at statement 5:',
              "    Statement: ((get_attr (eval lhs) 'dot') rhs)",
              '    Args: {[1, 2, 3]} {[1, 2]}',
              'PrimFun `method_fun` panicked:',
              '    Args: {rhs}',
              'PrimFun `List.dot` panicked:',
              '    Args: {__self__} {rhs}',
              'Module `test` panicked at line 1:',
              '    Statement: ((. prim puts) (. [1, 2, 3] [1, 2]))',
              '    Panic: PrimFun `List.dot` needs exactly `1` element in its attribute list, not `2`']
    output = get_output(source, capsys)
    assert output == target


def test_dot_list_panic_invalid_type(capsys):
    source = '''
    prim.puts [1, 2, 3].['fish']
    '''
    target = ['========== Panic: ==========',
              'PrimFun `prim.puts` panicked:',
              "    Args: (. [1, 2, 3] ['fish'])",
              'Fun `prelude.{.}` panicked at statement 5:',
              "    Statement: ((get_attr (eval lhs) 'dot') rhs)",
              "    Args: {[1, 2, 3]} {['fish']}",
              'PrimFun `method_fun` panicked:',
              '    Args: {rhs}',
              'PrimFun `List.dot` panicked:',
              '    Args: {__self__} {rhs}',
              'PrimFun `method_fun` panicked:',
              "    Args: {'fish'}",
              'PrimFun `List.get` panicked:',
              "    Args: {__self__} {'fish'}",
              'Module `test` panicked at line 1:',
              "    Statement: ((. prim puts) (. [1, 2, 3] ['fish']))",
              '    Panic: Arg `"fish"` of `List.get` must be a `Int`, not a `String`']
    output = get_output(source, capsys)
    assert output == target


def test_let(capsys):
    source = '''
    let x = 3
    prim.puts x
    '''
    target = ['3']
    assert get_output(source, capsys) == target
