from obsidian.semantics import *
from obsidian import parser
from textwrap import dedent
from beeprint import pp


def parse(source):
    ast, source_map = parser.parse(dedent(source), trace=False)
    print('ast:')
    pp(ast, max_depth=20)
    return ast


def test_simple_statement():
    source = '''
    puts "Hello, World!"
    '''
    assert parse(source) == [Call(Ident('puts'), [String('Hello, World!')])]


def test_simple_multiple_statements():
    source = '''
    puts "Hello!"
    puts "World!"
    '''
    assert parse(source) == [
        Call(Ident('puts'), [String('Hello!')]),
        Call(Ident('puts'), [String('World!')]),
    ]


def test_simple_multiple_singleline_statements():
    source = '''
    puts "Hello!"; puts "World!"
    '''
    assert parse(source) == [
        Call(Ident('puts'), [String('Hello!')]),
        Call(Ident('puts'), [String('World!')]),
    ]


def test_simple_call_statement():
    source = '''
    puts.("Hello, World!",)
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('puts'), Ident('.'), Tuple([String("Hello, World!")])])]


def test_simple_binary_slurp():
    source = '''
    puts 1+2
    '''
    assert parse(source) == [Call(Ident('puts'), [
        BinarySlurp([Int(1), Ident('+'), Int(2)])])]


def test_compound_binary_slurp():
    source = '''
    puts 1+2 * 3
    '''
    assert parse(source) == [Call(Ident('puts'), [BinarySlurp(
        [Int(1), Ident('+'), Int(2), Ident('*'), Int(3)])])]


def test_op_identifier():
    source = '''
    plus = {+}
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('plus'), Ident('='), Ident('+')])]


def test_binary_identifier():
    source = '''
    fn = {~and}
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('fn'), Ident('='), Ident('and')])]


def test_whitespace_slurp():
    source = '''
    x
    =
    1
    +
    2
    puts x
    .
    y
    '''
    assert parse(source) == [
        BinarySlurp([Ident('x'), Ident('='), Int(1), Ident('+'), Int(2)]),
        Call(Ident('puts'), [BinarySlurp(
            [Ident('x'), Ident('.'), Ident('y')])])
    ]


def test_whitespace_call():
    source = '''
    (
    fn
    arg1
    arg2
    )
    '''
    assert parse(source) == [Call(Ident('fn'), [Ident('arg1'), Ident('arg2')])]


def test_whitespace_tuple():
    source = '''
    (
    fn,
    arg1,
    arg2,
    )
    '''
    assert parse(source) == [Tuple(
        [Ident('fn'), Ident('arg1'), Ident('arg2')])]


def test_whitespace_single_tuple():
    source = '''
    (
    fn,
    )
    '''
    assert parse(source) == [Tuple(
        [Ident('fn')])]


def test_whitespace_list():
    source = '''
    [
    fn,
    arg1,
    arg2,
    ]
    '''
    assert parse(source) == [List(
        [Ident('fn'), Ident('arg1'), Ident('arg2')])]


def test_whitespace_map():
    source = '''
    {
    fn,
    arg1,
    arg2,
    }
    '''
    assert parse(source) == [Map(
        [Ident('fn'), Ident('arg1'), Ident('arg2')])]


def test_simple_if():
    source = '''
    if name ~is "John"
        puts "Hello, John!"
    '''
    assert parse(source) == [
        Call(Ident('if'), [BinarySlurp([Ident('name'), Ident('is'), String('John')]),
                           Block([Call(Ident('puts'), [String('Hello, John!')])])])
    ]


def test_single_quote():
    source = '''
    puts 'Hello, World!'
    '''
    assert parse(source) == [Call(Ident('puts'), [String('Hello, World!')])]


def test_single_nested_quote():
    source = '''
    puts 'Hello, "World!"'
    '''
    assert parse(source) == [Call(Ident('puts'), [String('Hello, "World!"')])]


def test_double_nested_quote():
    source = '''
    puts "Hello, 'World!'"
    '''
    assert parse(source) == [Call(Ident('puts'), [String("Hello, 'World!'")])]


def test_double_quote_escape():
    source = r'''
    puts "Hello, \"World!\""
    '''
    assert parse(source) == [Call(Ident('puts'), [String('Hello, "World!"')])]


def test_single_quote_escape():
    source = r'''
    puts 'Hello, \'World!\''
    '''
    assert parse(source) == [Call(Ident('puts'), [String("Hello, 'World!'")])]


def test_double_multiline_quote():
    source = r'''
    puts "Hello,
    World!"
    '''
    assert parse(source) == [
        Call(Ident('puts'), [String("Hello,\nWorld!")])]


def test_single_multiline_quote():
    source = r'''
    puts 'Hello,
    World!'
    '''
    assert parse(source) == [
        Call(Ident('puts'), [String("Hello,\nWorld!")])]


def test_triple_double_quote():
    source = r'''
    puts """Hello,
    "World"!"""
    '''
    assert parse(source) == [Call(Ident('puts'), [
        String('Hello,\n"World"!')])]


def test_triple_double_quote_escape():
    source = r'''
    puts """Hello,
    "World"!"""
    '''
    assert parse(source) == [Call(Ident('puts'), [
        String('Hello,\n"World"!')])]


def test_triple_single_quote_escape():
    source = r"""
    puts '''Hello,
    ''\'World'\'!'''
    """
    assert parse(source) == [Call(Ident('puts'), [
        String("Hello,\n'''World''!")])]


def test_triple_single_quote():
    source = r"""
    puts '''Hello,
    ''\'World'\'!'''
    """
    assert parse(source) == [Call(Ident('puts'), [
        String("Hello,\n'''World''!")])]


def test_string_interpolation():
    source = r'''
    puts "Hello, {"John"}!"
    '''
    assert parse(source) == [Call(Ident('puts'), [
        InterpolatedString([String('Hello, '), String('John'), String('!')])])]


def test_string_interpolation_nested():
    source = r'''
    puts "Hello, {1 + {2}}"
    '''
    assert parse(source) == [Call(Ident('puts'), [
        InterpolatedString([
            String('Hello, '),
            BinarySlurp([Int(1), Ident('+'), Int(2)])])
    ])]


def test_string_interpolation_empty():
    source = r'''
    puts "Hello{""}!"
    '''
    assert parse(source) == [
        Call(Ident('puts'), [InterpolatedString([String('Hello'), String(''), String('!')])])]


def test_string_interpolation_leading_space():
    source = r'''
    puts "  Hello, {"John"}"
    '''
    assert parse(source) == [Call(Ident('puts'), [
        InterpolatedString([String('  Hello, '), String('John')])])]


def test_string_interpolation_trailing_space():
    source = r'''
    puts "  Hello, {"John"}  "
    '''
    assert parse(source) == [Call(Ident('puts'), [
        InterpolatedString([String('  Hello, '), String('John'), String('  ')])])]


def test_string_interpolation_compound():
    source = r'''
    puts "  Hello, { name  }  {  "!" }  "
    '''
    assert parse(source) == [Call(Ident('puts'), [InterpolatedString([
        String('  Hello, '),
        Ident('name'),
        String('  '),
        String('!'),
        String('  ')
    ])])]


def test_string_interpolation_call():
    source = r'''
    puts "  Hello, { (last name)  }  {  "!" }  "
    '''
    assert parse(source) == [Call(Ident('puts'), [InterpolatedString([
        String('  Hello, '),
        Call(Ident('last'), [Ident('name')]),
        String('  '),
        String('!'),
        String('  ')
    ])])]


def test_unary_in_call():
    source = '''
    puts (-x)
    '''
    assert parse(source) == [Call(Ident('puts'), [
        Call(Ident('-'), [Ident('x')])])]


def test_int():
    source = '''
    x = 3
    '''
    assert parse(source) == [BinarySlurp([Ident('x'), Ident('='), Int(3)])]


def test_int_underscore():
    source = '''
    x = 3_000_000
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(3000000)])]


def test_int_trailing_underscore():
    source = '''
    x = 3_000_000_
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(3000000)])]


def test_bigint():
    source = '''
    x = 3e10
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(int(3e10))])]


def test_bigint_small():
    source = '''
    x = 3e-10
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(int(3e-10))])]


def test_bigint_small_negative():
    source = '''
    x = -3e-10
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(int(-3e-10))])]


def test_bigint_underscore():
    source = '''
    x = 3_00e1_0
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(int(300e10))])]


def test_bigint_trailing_underscore():
    source = '''
    x = 3_00_e1_0_
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(int(300e10))])]


def test_bigfloat():
    source = '''
    x = 3.0e10
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(3e10)])]


def test_bigfloat_small():
    source = '''
    x = 3.0e-10
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(3e-10)])]


def test_bigfloat_small_negative():
    source = '''
    x = -3.0e-10
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(-3e-10)])]


def test_bigfloat_underscore():
    source = '''
    x = 3_00.0e1_0
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(300e10)])]


def test_bigfloat_trailing_underscore():
    source = '''
    x = 3_00.0_e1_0_
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(300e10)])]


def test_float():
    source = '''
    x = 3.0
    '''
    assert parse(source) == [BinarySlurp([Ident('x'), Ident('='), Float(3.0)])]


def test_float_underscore():
    source = '''
    x = 3_000_000.000_000
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(3000000.0)])]


def test_float_trailing_underscore():
    source = '''
    x = 3_000_000.000_000_
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Float(3000000.0)])]


def test_symbol():
    source = '''
    x = @thingy
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Symbol('thingy')])]


def test_ident_question():
    source = '''
    works? = true
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('works?'), Ident('='), Ident('true')])]


def test_ident_question_nospace():
    source = '''
    works?=true
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('works?'), Ident('='), Ident('true')])]


def test_question_op():
    source = '''
    works ?= true
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('works'), Ident('?='), Ident('true')])]


def test_ident_exclamation():
    source = '''
    works! = true
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('works!'), Ident('='), Ident('true')])]


def test_ident_question_nospace():
    source = '''
    works!=true
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('works!'), Ident('='), Ident('true')])]


def test_question_op():
    source = '''
    works != true
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('works'), Ident('!='), Ident('true')])]


def test_op_identifier():
    source = '''
    def (+ x: int y: int)
        x.add_int y
    '''
    assert parse(source) == [
        Call(Ident('def'), [
            Call(Ident('+'), [
                BinarySlurp([Ident('x'), Ident(':'), Ident('int')]),
                BinarySlurp([Ident('y'), Ident(':'), Ident('int')]),
            ]), Block([
                Call(BinarySlurp([Ident('x'), Ident('.'),
                                  Ident('add_int')]), [Ident('y')])
            ])
        ])
    ]


def test_if_not():
    source = '''
    if (not thing.())
        puts "badness"
    '''
    assert parse(source) == [
        Call(Ident('if'), [
            Call(Ident('not'), [BinarySlurp(
                [Ident('thing'), Ident('.'), Tuple()])]),
            Block([Call(Ident('puts'), [String('badness')])])
        ])
    ]


def test_curly_expression():
    source = '''
    puts 3 * {4 + 1}
    '''
    assert parse(source) == [Call(Ident('puts'), [BinarySlurp([
        Int(3),
        Ident('*'),
        BinarySlurp([Int(4), Ident('+'), Int(1)])
    ])])]


def test_curly_expression_compound():
    source = '''
    puts 3 * {x = 4; x + 1}
    '''
    assert parse(source) == [Call(Ident('puts'), [BinarySlurp([
        Int(3),
        Ident('*'),
        Block([
            BinarySlurp([Ident('x'), Ident('='), Int(4)]),
            BinarySlurp([Ident('x'), Ident('+'), Int(1)])
        ])
    ])])]


def test_curly_expression_compound_multiline():
    source = '''
    puts 3
    *
    {
    x
    =
    4
    ;
    x
    +
    1
    }
    '''
    assert parse(source) == [Call(Ident('puts'), [BinarySlurp([
        Int(3),
        Ident('*'),
        Block([
            BinarySlurp([Ident('x'), Ident('='), Int(4)]),
            BinarySlurp([Ident('x'), Ident('+'), Int(1)])
        ])
    ])])]


def test_curly_expression_compound_multiline_nosemi():
    source = '''
    puts 3
    *
    {
    x
    =
    4
    x
    +
    1
    }
    '''
    assert parse(source) == [Call(Ident('puts'), [BinarySlurp([
        Int(3),
        Ident('*'),
        Block([
            BinarySlurp([Ident('x'), Ident('='), Int(4)]),
            BinarySlurp([Ident('x'), Ident('+'), Int(1)])
        ])
    ])])]


def test_list_dot_slice():
    source = '''
    puts list.{3..5}
    '''
    assert parse(source) == [Call(Ident('puts'), [BinarySlurp([
        Ident('list'),
        Ident('.'),
        BinarySlurp([Int(3), Ident('..'), Int(5)])
    ])])]


def test_toplevel_expression():
    source = '''
    3 + 4
    '''
    assert parse(source) == [BinarySlurp([Int(3), Ident('+'), Int(4)])]


def test_comment():
    source = r'''
    puts "Hello!"  # inline
    # prints "Hello\nWorld!"
    puts "World!"
    '''
    assert parse(source) == [
        Call(Ident('puts'), [String('Hello!')]),
        Call(Ident('puts'), [String('World!')]),
    ]


def test_list():
    source = '''
    list = [1, 2, (compute "number")]
    '''
    assert parse(source) == [BinarySlurp([
        Ident('list'),
        Ident('='),
        List([Int(1), Int(2), Call(Ident('compute'), [String('number')])])
    ])]


def test_empty_list():
    source = '''
    list = []
    '''
    assert parse(source) == [BinarySlurp([
        Ident('list'),
        Ident('='),
        List()
    ])]


def test_single_list():
    source = '''
    list = [1, ]
    '''
    assert parse(source) == [BinarySlurp([
        Ident('list'),
        Ident('='),
        List([Int(1)])
    ])]


def test_map():
    source = '''
    map = {"thing" -> "place",
           2 -> 3,
           5 -> (compute "number")}
    '''
    assert parse(source) == [BinarySlurp([
        Ident('map'),
        Ident('='),
        Map([
            BinarySlurp([String('thing'), Ident('->'), String('place')]),
            BinarySlurp([Int(2), Ident('->'), Int(3)]),
            BinarySlurp(
                [Int(5), Ident('->'), Call(Ident('compute'), [String('number')])])
        ])
    ])]


def test_map_trailing():
    source = '''
    map = {"thing" -> "place",
           2 -> 3,
           5 -> (compute "number"), }
    '''
    assert parse(source) == [BinarySlurp([
        Ident('map'),
        Ident('='),
        Map([
            BinarySlurp([String('thing'), Ident('->'), String('place')]),
            BinarySlurp([Int(2), Ident('->'), Int(3)]),
            BinarySlurp(
                [Int(5), Ident('->'), Call(Ident('compute'), [String('number')])])
        ])
    ])]


def test_single_map():
    source = '''
    map = {"thing" -> "place", }
    '''
    assert parse(source) == [BinarySlurp([
        Ident('map'),
        Ident('='),
        Map([
            BinarySlurp([String('thing'), Ident('->'), String('place')]),
        ])
    ])]


def test_empty_map():
    source = '''
    map = {}
    '''
    assert parse(source) == [BinarySlurp([
        Ident('map'),
        Ident('='),
        Map()
    ])]


def test_tuple():
    source = '''
    tuple = ("thing" -> "place",
             2 -> 3,
             5 -> (compute "number"))
    '''
    assert parse(source) == [BinarySlurp([
        Ident('tuple'),
        Ident('='),
        Tuple([
            BinarySlurp([String('thing'), Ident('->'), String('place')]),
            BinarySlurp([Int(2), Ident('->'), Int(3)]),
            BinarySlurp(
                [Int(5), Ident('->'), Call(Ident('compute'), [String('number')])])
        ])
    ])]


def test_tuple_trailing():
    source = '''
    tuple = ("thing" -> "place",
             2 -> 3,
             5 -> (compute "number"),)
    '''
    assert parse(source) == [BinarySlurp([
        Ident('tuple'),
        Ident('='),
        Tuple([
            BinarySlurp([String('thing'), Ident('->'), String('place')]),
            BinarySlurp([Int(2), Ident('->'), Int(3)]),
            BinarySlurp(
                [Int(5), Ident('->'), Call(Ident('compute'), [String('number')])])
        ])
    ])]


def test_single_tuple():
    source = '''
    tuple = ("thing" -> "place",)
    '''
    assert parse(source) == [BinarySlurp([
        Ident('tuple'),
        Ident('='),
        Tuple([
            BinarySlurp([String('thing'), Ident('->'), String('place')]),
        ])
    ])]


def test_empty_tuple():
    source = '''
    tuple = ()
    '''
    assert parse(source) == [BinarySlurp([
        Ident('tuple'),
        Ident('='),
        Tuple()
    ])]


def test_call_expression():
    source = '''
    (puts "Hello, World!")
    '''
    assert parse(source) == [Call(Ident('puts'), [String('Hello, World!')])]


def test_partial_call_expression():
    source = '''
    [replace "Hello, World!"]
    '''
    assert parse(source) == [PartialCall(
        Ident('replace'), [String('Hello, World!')])]


def test_unquote():
    source = '''
    $var (do_stuff)
    '''
    assert parse(source) == [
        Call(Unquote(Ident('var')), [Call(Ident('do_stuff'))])]


def test_unquote_call():
    source = '''
    $(fn arg) (do_stuff)
    '''
    assert parse(source) == [
        Call(Unquote(Call(Ident('fn'), [Ident('arg')])), [Call(Ident('do_stuff'))])]


def test_unquote_compound():
    source = '''
    ${(fn arg).attr} (do_stuff)
    '''
    assert parse(source) == [
        Call(Unquote(BinarySlurp([Call(Ident('fn'), [Ident('arg')]), Ident('.'), Ident('attr')])), [Call(Ident('do_stuff'))])]


def test_unquote_nested():
    source = '''
    $$var (do_stuff)
    '''
    assert parse(source) == [
        Call(Unquote(Unquote(Ident('var'))), [Call(Ident('do_stuff'))])]


def test_lambda():
    source = '''
    for list x =>
        puts x
    '''
    assert parse(source) == [Call(Ident('for'), [Ident('list'), BinarySlurp([
        Ident('x'),
        Ident('=>'),
        Block([Call(Ident('puts'), [Ident('x')])])
    ])])]


def test_class():
    source = '''
    class Dog
        def (new breed)
            self.breed = breed

        def (bark)
            puts "Woof!"
    '''
    assert parse(source) == [Call(Ident('class'), [Ident('Dog'), Block([
        Call(Ident('def'), [Call(Ident('new'), [Ident('breed')]), Block([
            BinarySlurp([Ident('self'), Ident('.'), Ident(
                'breed'), Ident('='), Ident('breed')])
        ])]),
        Call(Ident('def'), [Call(Ident('bark')), Block([
            Call(Ident('puts'), [String('Woof!')])
        ])])
    ])])]


def test_match():
    source = '''
    match x
        Dog -> (puts "I'm a dog")
        Cat -> (puts "I'm a cat")
    '''
    assert parse(source) == [Call(Ident('match'), [Ident('x'), Block([
        BinarySlurp([Ident('Dog'), Ident('->'),
                     Call(Ident('puts'), [String("I'm a dog")])]),
        BinarySlurp([Ident('Cat'), Ident('->'),
                     Call(Ident('puts'), [String("I'm a cat")])]),
    ])])]


def test_record():
    source = '''
    record Dog
        breed: [@golden_retriever, @beagle]
        name: String
    '''
    truth = [Call(Ident('record'), [Ident('Dog'), Block([
        BinarySlurp([Ident('breed'), Ident(':'), List(
            [Symbol('golden_retriever'), Symbol('beagle')])]),
        BinarySlurp([Ident('name'), Ident(':'), Ident('String')])
    ])])]
    print('Truth: ', truth)
    assert parse(source) == truth


def test_kwargs():
    source = '''
    train model l2: 0.5 alpha: 0.01
    '''
    assert parse(source) == [Call(Ident('train'), [
        Ident('model'),
        BinarySlurp([Ident('l2'), Ident(':'), Float(0.5)]),
        BinarySlurp([Ident('alpha'), Ident(':'), Float(0.01)]),
    ])]


def test_varargs():
    source = '''
    def (variadic first(...rest))
        (stuff)
    (variadic arg1)
    variadic arg1 arg2 (...args)
    '''
    assert parse(source) == [
        Call(Ident('def'), [
            Call(Ident('variadic'), [Ident('first'),
                                     Call(Ident('...'), [Ident('rest')])]),
            Block([Call(Ident('stuff'))])
        ]),
        Call(Ident('variadic'), [Ident('arg1')]),
        Call(Ident('variadic'), [Ident('arg1'), Ident(
            'arg2'), Call(Ident('...'), [Ident('args')])]),
    ]


def test_tuple_deconstruction():
    source = '''
    (name, occupation) = ("John Smith", @farmer)
    '''
    assert parse(source) == [BinarySlurp([
        Tuple([Ident('name'), Ident('occupation')]),
        Ident('='),
        Tuple([String('John Smith'), Symbol('farmer')])
    ])]


def test_defop():
    source = '''
    defop {+} assoc: @left priority: 5
    '''
    assert parse(source) == [Call(Ident('defop'), [
        Ident('+'),
        BinarySlurp([Ident('assoc'), Ident(':'), Symbol('left')]),
        BinarySlurp([Ident('priority'), Ident(':'), Int(5)])
    ])]


def test_dots():
    source = '''
    x = 1...3
    '''
    assert parse(source) == [BinarySlurp(
        [Ident('x'), Ident('='), Int(1), Ident('...'), Int(3)])]


def test_inline_def():
    source = '''
    (Dog name) =
        self.name = name
    '''
    assert parse(source) == [BinarySlurp([
        Call(Ident('Dog'), [Ident('name')]),
        Ident('='),
        Block([BinarySlurp([Ident('self'), Ident('.'),
                            Ident('name'), Ident('='), Ident('name')])])
    ])]
