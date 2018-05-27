from obsidian.interpreter.types.scope import Scope, DummyCall


def test_simple():
    scope = Scope()
    slurp = ['x', ('+', 6, 'left'), 'y']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall('+', ['x', 'y'])


def test_multi():
    scope = Scope()
    slurp = ['w', ('+', 6, 'left'), 'x', ('+', 6, 'left'),
             'y', ('+', 6, 'left'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall(
        '+', [DummyCall('+', [DummyCall('+', ['w', 'x']), 'y']), 'z'])


def test_noop():
    scope = Scope()
    slurp = ['x']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == 'x'


def test_right():
    scope = Scope()
    slurp = ['w', ('^', 6, 'right'), 'x', ('^', 6, 'right'),
             'y', ('^', 6, 'right'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall(
        '^', ['w', DummyCall('^', ['x', DummyCall('^', ['y', 'z'])])])


def test_precedence():
    scope = Scope()
    slurp = ['w', ('+', 6, 'left'), 'x', ('*', 7, 'left'),
             'y', ('+', 6, 'left'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall(
        '+', [DummyCall('+', ['w', DummyCall('*', ['x', 'y'])]), 'z'])


def test_no_assoc():
    scope = Scope()
    op = '=='
    slurp = ['w', (op, 4, 'none'), 'x', (op, 4, 'none'),
             'y', (op, 4, 'none'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall('==', ['w', 'x', 'y', 'z'])


def test_no_assoc_single():
    scope = Scope()
    op = '=='
    slurp = ['w', (op, 4, 'none'), 'x']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall('==', ['w', 'x'])


def test_no_assoc_precedence():
    scope = Scope()
    op = '=='
    slurp = ['w', (op, 4, 'none'), 'x', ('*', 7, 'left'),
             'y', (op, 4, 'none'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall('==', ['w', DummyCall('*', ['x', 'y']), 'z'])


def test_multi_no_assoc():
    scope = Scope()
    op = '=='
    slurp = ['w', (op, 4, 'none'), 'x', ('!=', 4, 'none'),
             'y', (op, 4, 'none'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall(
        '==', [DummyCall('!=', [DummyCall('==', ['w', 'x']), 'y']), 'z'])


def test_multi_no_assoc_precedence():
    scope = Scope()
    op = '=='
    slurp = ['w', (op, 4, 'none'), 'x', ('!=', 7, 'none'),
             'y', (op, 4, 'none'), 'z']
    pos, ast = scope.parse_binary_subexpr(slurp, slurp[0])
    assert ast == DummyCall('==', ['w', DummyCall('!=', ['x', 'y']), 'z'])
