import re
import collections

Token = collections.namedtuple('Token', ('type', 'value', 'line', 'column'))
Indent = collections.namedtuple('Indent', ('indent_lvl', 'indent_size'))


class Scanner:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.indentation_match = re.compile(r'[ \t]*').match
        self.tokenize()

    def tokenize(self):
        self.indent_lvl = 0
        self.indentiation = [Indent(self.indent_lvl, 0), ]
        self.line = 1
        self.position = self.line_start = 0

        token_regex = (
            ('NEW_LINE', r'[ \t]*\n'),
            ('ID', r'[\w:\-/]*\w'),
            ('COLON', r'[ \t]*:[ \t]*'),
            ('STRING', r'\'[\w.:]*\'|"[\w.:]*\"'),
            ('DASH', r'[ \t]*-[ \t]*')
        )
        token_regex = '|'.join((f'(?P<{type}>{regex})' for type, regex in token_regex))
        get_token = re.compile(token_regex).match
        match = get_token(self.text)

        while match:
            match_type = match.lastgroup
            if match_type == 'NEW_LINE':
                self.line += 1
                self.position = match.end()
                self.line_start = self.position
                self.check_indentation()
            else:
                value = match.group(match_type)
                self.tokens.append(Token(match_type, value, self.line, match.start()-self.line_start+1))
                self.position = match.end()

            match = get_token(self.text, self.position)

    def check_indentation(self):
        current_indent_size = self.indentation_match(self.text, self.position)
        if current_indent_size:
            start = current_indent_size.start()
            current_indent_size = len(current_indent_size.group(0))

            if current_indent_size > self.indentiation[-1].indent_size:
                self.indent_lvl += 1
                self.tokens.append(Token('CODE_BLOCK', self.indent_lvl, self.line, start-self.line_start+1))
                self.indentiation.append(Indent(self.indent_lvl, current_indent_size))
            else:
                for indent in self.indentiation[::-1]:
                    indent_lvl = indent.indent_lvl
                    indent = indent.indent_size
                    if current_indent_size >= indent:
                        break
                    self.tokens.append(Token('END_CODE_BLOCK', indent_lvl, self.line, start-self.line_start+1))
                    self.indentiation.pop()

            self.position = self.indentation_match(self.text, self.position).end()
