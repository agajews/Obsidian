from .grammar import ObsidianParser
from .semantics import Semantics

indent_tok = '{-INDENT-}'
dedent_tok = '{-DEDENT-}'

parser = ObsidianParser()


def preprocess(text):
    indentations = []

    parens_depths = {
        '(': 0,
        '[': 0,
        '{': 0,
        '"': 0,
        "'": 0
    }

    def not_in_parens():
        return all(val == 0 for key, val in parens_depths.items())

    indent_depth = 0
    indent_len = None
    lines = text.split('\n')
    for line_no, line in enumerate(lines):
        stripped_len = len(line.lstrip())
        indent = len(line) - stripped_len
        if not_in_parens() and stripped_len > 0:
            if indent > 0:
                if indent_len is None:
                    indent_len = indent
                if indent % indent_len != 0:
                    raise Exception(
                        'Invalid indentation at line {}'.format(line_no))
                indent_depth = indent // indent_len
            else:
                indent_depth = 0
        indentations.append(indent_depth)
        for name, left, right in [
                ('parenthesis', '(', ')'),
                ('curly brace', '{', '}'),
                ('square bracket', '[', ']')]:
            parens_depths[left] += line.count(left) - line.count(right)
            if parens_depths[left] < 0:
                raise Exception(
                    'Unmatched {} at line {}'.format(name, line_no + 1))
        for quote in ["'", '"']:
            parens_depths[quote] = (
                parens_depths[quote] + line.count(quote)) % 2

    # print(indentations)

    source_map = {}
    indent_depth = 0
    for line_no, line in enumerate(lines):
        if indentations[line_no] - indent_depth > 1:
            raise Exception('Over-indentation at line {}'.format(line_no + 1))
        if indentations[line_no] > indent_depth:
            lines[line_no] = indent_tok + line
            source_map[line_no] = {0: len(indent_tok)}
        if indentations[line_no] < indent_depth:
            num_dedents = (indent_depth - indentations[line_no])
            prev_no = line_no - 1
            map_delta = {len(lines[prev_no]): len(dedent_tok) * num_dedents}
            if line_no - 1 in source_map:
                source_map[prev_no].update(map_delta)
            else:
                source_map[prev_no] = map_delta
            lines[prev_no] += dedent_tok * num_dedents
        indent_depth = indentations[line_no]
    if indent_depth > 0:
        line_no = len(lines) - 1
        map_delta = {len(lines[-1]): len(dedent_tok) * indent_depth}
        if line_no in source_map:
            source_map[line_no].update(map_delta)
        else:
            source_map[line_no] = map_delta
        lines[-1] += dedent_tok * indent_depth
    return '\n'.join(lines), source_map


def parse(text, trace=False):
    text, source_map = preprocess(text)
    # print(text)
    return parser.parse(text, rule_name='program', semantics=Semantics, trace=trace), source_map
