from my_scanner import *
from my_parser import *
from pprint import pprint

with open('compose.yaml') as f:
    text = f.read()

scanner = Scanner(text)
pprint(scanner.tokens)
pprint('-----')

parser = Parser(scanner)
parser.start()
