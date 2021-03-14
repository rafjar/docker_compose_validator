
class Parser:
    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.token = self.next_token()
        self.n_token = 1

    def get_token(self, token_type):
        if self.token.type != token_type:
            raise RuntimeError(f'Praser error!!!\nUnexpected token: {self.token}\nExpected token of type: {token_type}')
        self.token = self.next_token()
        self.n_token += 1

    def start(self):
        base_id = ('VERSION_ID', 'SERVICES_ID', )
        if self.token.type in base_id:
            self.program()
            self.get_token('EOF')

    def program(self):
        if self.token.type == 'VERSION_ID':
            self.version_prod()
            self.program()
        elif self.token.type == 'SERVICES_ID':
            self.services_prod()
            self.program()
        elif self.token.type == 'IMAGE_ID':
            self.image_prod()
            self.program()
        elif self.token.type == 'PORTS_ID':
            self.ports_prod()
            self.program()
        elif self.token.type == 'NETWORKS_ID':
            self.networks_prod()
            self.program()
        elif self.token.type == 'DEPLOY_ID':
            self.deploy_prod()
            self.program()
        elif self.token.type == 'VOLUMES_ID':
            self.volumes_prod()
            self.program()
        elif self.token.type == 'ENVIRONMENT_ID':
            self.environment_prod()
            self.program()
        elif self.token.type == 'BUILD_ID':
            self.get_token('BUILD_ID')
            self.get_token('COLON')
            self.build_prod()
            self.program()
        elif self.token.type == 'ID':
            self.get_token('ID')
            self.get_token('COLON')
            self.unknow_id_prod()
            self.program()
        else:
            pass

    def build_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered build_prod statement')

        if self.token.type == 'BUILD_PATH':
            self.get_token('BUILD_PATH')
        else:
            self.build_content()

        print(f'{n_token:<3} Statement build_prod parsed correctly')

    def build_content(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered build_content statement')

        self.get_token('CODE_BLOCK')
        self.get_token('CONTEXT_ID')
        self.get_token('COLON')
        self.get_token('BUILD_PATH')
        self.program()
        self.get_token('END_CODE_BLOCK')

        print(f'{n_token:<3} Statement build_content parsed correctly')

    def environment_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered environment_prod statement')

        self.get_token('ENVIRONMENT_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement environment_prod parsed correctly')

    def volumes_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered volumes_prod statement')

        self.get_token('VOLUMES_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement volumes_prod parsed correctly')

    def deploy_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered deploy_prod statement')

        self.get_token('DEPLOY_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement deploy_prod parsed correctly')

    def networks_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered networks_prod statement')

        self.get_token('NETWORKS_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement networks_prod parsed correctly')

    def ports_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered ports_prod statement')

        self.get_token('PORTS_ID')
        self.get_token('COLON')
        self.get_token('SEQUENCE_BLOCK')
        self.ports_sequence()
        self.get_token('END_CODE_BLOCK')

        print(f'{n_token:<3} Statement ports_prod parsed correctly')

    def ports_sequence(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered ports_sequence statement')

        if self.token.type == 'DASH':
            self.get_token('DASH')
            self.get_token('PORTS_VAL')
            self.ports_sequence()
        else:
            pass

        print(f'{n_token:<3} Statement ports_sequence parsed correctly')

    def image_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered image_prod statement')

        self.get_token('IMAGE_ID')
        self.get_token('COLON')
        self.get_token('ID')

        print(f'{n_token:<3} Statement image_prod parsed correctly')

    def unknow_id_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered unknow_id_prod statement')

        if self.token.type == 'CODE_BLOCK':
            self.get_token('CODE_BLOCK')
            self.program()
            self.get_token('END_CODE_BLOCK')
        elif self.token.type == 'SEQUENCE_BLOCK':
            self.get_token('SEQUENCE_BLOCK')
            self.sequence_block_prod()
            self.get_token('END_CODE_BLOCK')
        else:
            self.value_prod()

        print(f'{n_token:<3} Statement unknow_id_prod parsed correctly')

    def value_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered value_prod statement')

        if self.token.type == 'ID':
            self.get_token('ID')
        elif self.token.type == 'STRING':
            self.get_token('STRING')
        else:
            pass

        print(f'{n_token:<3} Statement value_prod parsed correctly')

    def sequence_block_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered sequence_block_prod statement')

        if self.token.type == 'DASH':
            self.get_token('DASH')
            self.value_prod()
            self.sequence_block_prod()
        else:
            pass

        print(f'{n_token:<3} Statement sequence_block_prod parsed correctly')

    def services_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered services_prod statement')

        self.get_token('SERVICES_ID')
        self.get_token('COLON')
        self.get_token('CODE_BLOCK')
        self.program()
        self.get_token('END_CODE_BLOCK')

        print(f'{n_token:<3} Statement services_prod parsed correctly')

    def version_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered version_prod statement')

        self.get_token('VERSION_ID')
        self.get_token('COLON')
        self.get_token('VERSION_VAL')

        print(f'{n_token:<3} Statement version_prod parsed correctly')
