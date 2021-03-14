import re
import collections

Token = collections.namedtuple('Token', ('type', 'value', 'line', 'column'))
Indent = collections.namedtuple('Indent', ('indent_lvl', 'indent_size'))


class Scanner:
    def __init__(self, path):
        with open(path) as f:
            text = f.read()

        self.text = '\n'.join(list(filter(lambda x: not re.match(r'^\s*$', x), text.split('\n')))) + '\n'

        with open(path, 'w') as f:
            f.write(self.text)

        self.tokens = []
        self.indentation_match = re.compile(r'[ \t]*').match
        self.sequence_match = re.compile(r'[ \t]*\-').match
        self.tokenize()

    def tokenize(self):
        self.indent_lvl = 0
        self.indentiation = [Indent(self.indent_lvl, 0), ]
        self.line = 1
        self.position = self.line_start = 0

        token_regex = (
            ('VERSION_ID', r'version'),         # DONE
            ('SERVICES_ID', r'services'),       # DONE
            ('IMAGE_ID', r'image'),             # DONE
            ('PORTS_ID', r'ports'),             # DONE
            ('NETWORKS_ID', r'networks'),       # DONE
            ('DEPLOY_ID', r'deploy'),           # DONE
            ('VOLUMES_ID', r'volumes'),         # DONE
            ('ENVIRONMENT_ID', r'environment'),
            ('BUILD_ID', r'build'),             # DONE

            ('VERSION_VAL', r'"\d+(\.\d+)?"'),
            ('PORTS_VAL', r'"(\d+([\-:]\d+)?)"|("\d+\-\d+:\d+\-\d+")'),
            ('CONTEXT_ID', r'context'),

            ('NEW_LINE', r'[ \t]*\n'),
            ('ID', r'[\w:\-\/]*\w'),
            ('BUILD_PATH', r'(\.{0,2}?\/?\w+\d*\w*\/?)+'),
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
        self.tokens.append(Token('EOF', '', self.line, 1))

    def check_indentation(self):
        begin_sequence = self.sequence_match(self.text, self.position)
        current_indent_size = self.indentation_match(self.text, self.position)
        if current_indent_size:
            start = current_indent_size.start()
            current_indent_size = len(current_indent_size.group(0))

            if current_indent_size > self.indentiation[-1].indent_size:
                self.indent_lvl += 1
                if begin_sequence:
                    self.tokens.append(Token('SEQUENCE_BLOCK', self.indent_lvl, self.line, start-self.line_start+1))
                else:
                    self.tokens.append(Token('CODE_BLOCK', self.indent_lvl, self.line, start-self.line_start+1))
                self.indentiation.append(Indent(self.indent_lvl, current_indent_size))
            else:
                for indent in self.indentiation[::-1]:
                    indent_lvl = indent.indent_lvl
                    indent = indent.indent_size
                    if current_indent_size >= indent:
                        break
                    self.tokens.append(Token('END_CODE_BLOCK', indent_lvl, self.line, start-self.line_start+1))
                    self.indent_lvl -= 1
                    self.indentiation.pop()

            self.position = self.indentation_match(self.text, self.position).end()

    def next_token(self):
        return self.tokens.pop(0) if self.tokens else None
