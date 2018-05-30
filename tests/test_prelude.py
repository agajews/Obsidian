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
              'Module `test` panicked at line 2:',
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
              'Module `test` panicked at line 2:',
              "    Statement: ((. prim puts) (. [1, 2, 3] ['fish']))",
              '    Panic: Arg `"fish"` of `List.get` must be a `Int`, not a `String`']
    output = get_output(source, capsys)
    assert output == target


def test_dot_missing_attr(capsys):
    source = '''
    prim.missing 'missing'
    '''
    target = ['========== Panic: ==========',
              'Fun `prelude.{.}` panicked at statement 5:',
              "    Statement: ((get_attr (eval lhs) 'dot') rhs)",
              '    Args: {prim} {missing}',
              'PrimFun `method_fun` panicked:',
              '    Args: {rhs}',
              'PrimFun `Object.dot` panicked:',
              '    Args: {__self__} {rhs}',
              'Module `test` panicked at line 2:',
              "    Statement: ((. prim missing) 'missing')",
              '    Panic: Module `<Module `prim`>` has no attribute `missing`']
    output = get_output(source, capsys)
    assert output == target


def test_dot_map(capsys):
    source = '''
    prim.puts {('fish', 1), ('dogs', 2), ('whales', 3)}.['whales']
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_let(capsys):
    source = '''
    let x = 3
    prim.puts x
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_scope(capsys):
    source = '''
    let x = 3
    prim.puts meta.scope.x
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_eval(capsys):
    source = '''
    let x = 3
    prim.puts (meta.eval (ast.Ident 'x'))
    '''
    target = ['3']
    assert get_output(source, capsys) == target


def test_let_dot(capsys):
    source = '''
    let x = 3
    prim.puts x
    let x.pretty_name = 'three'
    prim.puts x.pretty_name
    '''
    target = ['3', 'three']
    assert get_output(source, capsys) == target


def test_let_invalid(capsys):
    source = '''
    let @x = 3
    prim.puts x
    '''
    target = ['========== Panic: ==========',
              'Fun `prelude.let` panicked at statement 5:',
              '    Statement: (let_recursive lval rval)',
              '    Args: (= @x 3)',
              'Fun `let_recursive` panicked at statement 3:',
              '    Statement: ((. prim cond) ((is_instance lval (. ast Ident)), (set_attr caller (. lval ident) rval)) ((is_instance lval (. ast Call)), [((. prim cond) ((and (is (eval (. lval callable)) .) (and ((. (. prim int) eq) ((. (. lval args) len)) 2) (is_instance (. (. lval args) [1]) (. ast Ident)))), (set_attr (ceval (. (. lval args) [0])) (. (. (. lval args) [1]) ident) rval)) (true, ((. prim panic) "\'Fun `prelude.let` received invalid lval `\'lval\'`\'")))]) (true, ((. prim panic) "\'Fun `prelude.let` received invalid lval `\'lval\'`\'")))',
              '    Args: {lval} {rval}',
              'PrimFun `prim.cond` panicked:',
              '    Args: {((is_instance lval (. ast Ident)), (set_attr caller (. lval ident) rval))} {((is_instance lval (. ast Call)), [((. prim cond) ((and (is (eval (. lval callable)) .) (and ((. (. prim int) eq) ((. (. lval args) len)) 2) (is_instance (. (. lval args) [1]) (. ast Ident)))), (set_attr (ceval (. (. lval args) [0])) (. (. (. lval args) [1]) ident) rval)) (true, ((. prim panic) "\'Fun `prelude.let` received invalid lval `\'lval\'`\'")))])} {(true, ((. prim panic) "\'Fun `prelude.let` received invalid lval `\'lval\'`\'"))}',
              'PrimFun `prim.panic` panicked:',
              '    Args: "\'Fun `prelude.let` received invalid lval `\'lval\'`\'"',
              'Module `test` panicked at line 2:',
              '    Statement: (let (= @x 3))',
              '    Panic: Fun `prelude.let` received invalid lval `{@x}`']
    output = get_output(source, capsys)
    assert output == target
