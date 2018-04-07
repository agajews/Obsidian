from obsidian.semantics import *
from obsidian import parser
from textwrap import dedent


def preprocess(source):
    text, source_map = parser.preprocess(dedent(source))
    print(text)
    return text, source_map


def test_flat():
    source = '''
    puts "Hello, world!"
    puts "Goodbye"
    '''
    text, source_map = preprocess(source)
    assert text == dedent(source)
    assert source_map == {}


def test_map():
    source = '''
    x = {
        1 -> 2,
        3 -> 4
    }
    '''
    text, source_map = preprocess(source)
    assert text == dedent(source)
    assert source_map == {}


def test_map_empty_indent():
    source = '''
    x = {
        1 -> 2,
        3 -> 4
    }
        '''
    text, source_map = preprocess(source)
    assert text == dedent(source)
    assert source_map == {}


def test_single_indent():
    source = '''
    let x =
        3 + 4
    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        let x =
        {-INDENT-}    3 + 4
        {-DEDENT-}''')
    assert source_map == {2: {0: 10}, 3: {0: 10}}


def test_single_indent_empty_indent():
    source = '''
    let x =
        3 + 4

    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        let x =
        {-INDENT-}    3 + 4

        {-DEDENT-}''')
    assert source_map == {2: {0: 10}, 4: {0: 10}}


def test_single_indent_no_trailing_line():
    source = '''
    let x =
        3 + 4'''
    text, source_map = preprocess(source)
    assert text == dedent('''
        let x =
        {-INDENT-}    3 + 4{-DEDENT-}''')
    assert source_map == {2: {0: 10, 19: 10}}


def test_whitespace():
    source = '''
    fun (f) =
        let x = 3

        let y = 3
    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f) =
        {-INDENT-}    let x = 3

            let y = 3
        {-DEDENT-}''')
    assert source_map == {2: {0: 10}, 5: {0: 10}}


def test_nested_indent():
    source = '''
    fun (f) =
        if cond
            puts "Hi"
    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f) =
        {-INDENT-}    if cond
        {-INDENT-}        puts "Hi"
        {-DEDENT-}{-DEDENT-}''')
    assert source_map == {2: {0: 10}, 3: {0: 10}, 4: {0: 20}}


def test_nested_indent_no_trailing_line():
    source = '''
    fun (f) =
        if cond
            puts "Hi"'''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f) =
        {-INDENT-}    if cond
        {-INDENT-}        puts "Hi"{-DEDENT-}{-DEDENT-}''')
    assert source_map == {2: {0: 10}, 3: {0: 10, 27: 20}}


def test_empty():
    source = ''
    text, source_map = preprocess(source)
    assert text == ''
    assert source_map == {}


def test_nested_indent_parens():
    source = '''
    fun (f
       ) =
        if cond
            puts "Hi"
    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f
           ) =
        {-INDENT-}    if cond
        {-INDENT-}        puts "Hi"
        {-DEDENT-}{-DEDENT-}''')
    assert source_map == {3: {0: 10}, 4: {0: 10}, 5: {0: 20}}


def test_nested_indent_nested_parens():
    source = '''
    fun (f (
        thing {3[

    ]})
       ) =
        if cond
            puts "Hi"
    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f (
            thing {3[

        ]})
           ) =
        {-INDENT-}    if cond
        {-INDENT-}        puts "Hi"
        {-DEDENT-}{-DEDENT-}''')
    assert source_map == {6: {0: 10}, 7: {0: 10}, 8: {0: 20}}


def test_nested_indent_nested_parens_no_trailing_line():
    source = '''
    fun (f (
        thing {3[

    ]})
       ) =
        if cond
            puts "Hi"'''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f (
            thing {3[

        ]})
           ) =
        {-INDENT-}    if cond
        {-INDENT-}        puts "Hi"{-DEDENT-}{-DEDENT-}''')
    assert source_map == {6: {0: 10}, 7: {0: 10, 27: 20}}


def test_nested_indent_quotes():
    source = '''
    fun (f (
        thing {3[''

    ]})"""
       ) """=
        if cond
            puts "Hi"
    '''
    text, source_map = preprocess(source)
    assert text == dedent('''
        fun (f (
            thing {3[''

        ]})"""
           ) """=
        {-INDENT-}    if cond
        {-INDENT-}        puts "Hi"
        {-DEDENT-}{-DEDENT-}''')
    assert source_map == {6: {0: 10}, 7: {0: 10}, 8: {0: 20}}
