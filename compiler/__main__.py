import argparse


parser = argparse.ArgumentParser(prog='compiler', description='Compile to golang')
parser.add_argument('-o', '--out', metavar='PATH', type=str, help='the path to the output-file')
parser.add_argument('path', metavar='path', type=str, help='the path to the input-file')

args = parser.parse_args()

print(f"Compiling '{args.path}' to '{args.out}'")
