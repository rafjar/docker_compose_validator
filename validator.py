from my_scanner import *
from my_parser import *

with open('compose.yaml') as f:
    text = f.read()

scanner = Scanner(text)
