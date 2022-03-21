import argparse

from compiler import compile_c


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Prism Compiler')
    parser.add_argument('-o', '--output', metavar='output', type=str, help='path to output file')
    parser.add_argument('input', metavar='input', type=str, help='path to input file')

    args = parser.parse_args()

    compile_c(args.input, args.output)
