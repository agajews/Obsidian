from parser import parse
from argparse import ArgumentParser


def parse_from_file(fnm):
    with open(fnm, 'r') as f:
        ast, source_map = parse(f.read())
    print(ast)


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('filename', help='file to interpret')
    args = argparser.parse_args()

    parse_from_file(args.filename)
