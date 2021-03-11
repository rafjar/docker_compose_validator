import re
import collections

Token = collections.namedtuple('Token', ('type', 'value', 'line', 'column'))
Indent = collections.namedtuple('Indent', ('indent_lvl', 'indent_size'))


class Scanner:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.indentation_match = re.compile(r' *').match
        self.tokenize()

    def tokenize(self):
        indent_lvl = -1
        indent_size = -1
        self.indentiation = [Indent(indent_lvl, indent_size), ]
        self.line = 1
        self.position = self.line_start = 0

        token_regex = (
            ('NEW_LINE', r'\s*\n'),
        )
        token_regex = '|'.join((f'(?P<{type}>{regex})' for type, regex in token_regex))
        get_token = re.compile(token_regex).match
        match = get_token(self.text)

        while match:
            match_type = match.lastgroup
            if match_type == 'NEW_LINE':
                line += 1
                self.line_start = self.position
                self.check_indentation()

            self.position = match.end()

    def check_indentation(self):
        current_indent_size = len(self.indentation_match(self.text, self.position).group(0))
        # sprawdzić w pętli czy wcięcie jest większe niż wcięcie poprzednich bloków
