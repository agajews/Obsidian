from .grammar import ObsidianParser
from .semantics import Semantics

parser = ObsidianParser()

def parse(text, trace=False):
    return parser.parse(text, rule_name='program', semantics=Semantics, trace=trace)
