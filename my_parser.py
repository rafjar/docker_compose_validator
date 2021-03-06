
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
        base_id = ('VERSION_ID', 'SERVICES_ID', 'IMAGE_ID', 'PORTS_ID', 'NETWORKS_ID', 'DEPLOY_ID', 'VOLUMES_ID', 'ENVIRONMENT_ID', 'BUILD_ID', 'ID')
        # start -> program EOF
        if self.token.type in base_id:
            self.program()
            self.get_token('EOF')

    def program(self):
        # program -> version_prod program
        if self.token.type == 'VERSION_ID':
            self.version_prod()
            self.program()
        # program -> services_prod program
        elif self.token.type == 'SERVICES_ID':
            self.services_prod()
            self.program()
        # program -> image_prod program
        elif self.token.type == 'IMAGE_ID':
            self.image_prod()
            self.program()
        # program -> ports_prod program
        elif self.token.type == 'PORTS_ID':
            self.ports_prod()
            self.program()
        # program -> networks_prod program
        elif self.token.type == 'NETWORKS_ID':
            self.networks_prod()
            self.program()
        # program -> deploy_prod program
        elif self.token.type == 'DEPLOY_ID':
            self.deploy_prod()
            self.program()
        # program -> volumes_prod program
        elif self.token.type == 'VOLUMES_ID':
            self.volumes_prod()
            self.program()
        # program -> environment_prod program
        elif self.token.type == 'ENVIRONMENT_ID':
            self.environment_prod()
            self.program()
        # program -> BUILD_ID COLON build_prod program
        elif self.token.type == 'BUILD_ID':
            self.get_token('BUILD_ID')
            self.get_token('COLON')
            self.build_prod()
            self.program()
        # program -> ID COLON unknow_id_prod program
        elif self.token.type == 'ID':
            self.get_token('ID')
            self.get_token('COLON')
            self.unknow_id_prod()
            self.program()
        # program -> EPSILON
        else:
            pass

    def version_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered version_prod statement')

        # version_prod -> VERSION_ID COLON VERSION_VAL
        self.get_token('VERSION_ID')
        self.get_token('COLON')
        self.get_token('VERSION_VAL')

        print(f'{n_token:<3} Statement version_prod parsed correctly')

    def services_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered services_prod statement')

        # services_prod -> SERVICES_ID COLON CODE_BLOCK program END_CODE_BLOCK
        self.get_token('SERVICES_ID')
        self.get_token('COLON')
        self.get_token('CODE_BLOCK')
        self.program()
        self.get_token('END_CODE_BLOCK')

        print(f'{n_token:<3} Statement services_prod parsed correctly')

    def image_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered image_prod statement')

        # image_prod -> IMAGE_ID COLON ID
        self.get_token('IMAGE_ID')
        self.get_token('COLON')
        self.get_token('ID')

        print(f'{n_token:<3} Statement image_prod parsed correctly')

    def ports_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered ports_prod statement')

        # ports_prod -> PORTS_ID COLON SEQUENCE_BLOCK ports_sequence END_CODE_BLOCK
        self.get_token('PORTS_ID')
        self.get_token('COLON')
        self.get_token('SEQUENCE_BLOCK')
        self.ports_sequence()
        self.get_token('END_CODE_BLOCK')

        print(f'{n_token:<3} Statement ports_prod parsed correctly')

    def ports_sequence(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered ports_sequence statement')

        # ports_sequence -> DASH PORTS_VAL ports_sequence
        if self.token.type == 'DASH':
            self.get_token('DASH')
            self.get_token('PORTS_VAL')
            self.ports_sequence()
        # ports_sequence -> EPSILON
        else:
            pass

        print(f'{n_token:<3} Statement ports_sequence parsed correctly')

    def networks_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered networks_prod statement')

        # networks_prod -> NETWORKS_ID COLON unknow_id_prod
        self.get_token('NETWORKS_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement networks_prod parsed correctly')

    def deploy_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered deploy_prod statement')

        # deploy_prod -> DEPLOY_ID COLON unknow_id_prod
        self.get_token('DEPLOY_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement deploy_prod parsed correctly')

    def volumes_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered volumes_prod statement')

        # volumes_prod -> VOLUMES_ID COLON unknow_id_prod
        self.get_token('VOLUMES_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement volumes_prod parsed correctly')

    def environment_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered environment_prod statement')

        # environment_prod -> ENVIRONMENT_ID COLON unknow_id_prod
        self.get_token('ENVIRONMENT_ID')
        self.get_token('COLON')
        self.unknow_id_prod()

        print(f'{n_token:<3} Statement environment_prod parsed correctly')

    def build_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered build_prod statement')

        # build_prod -> BUILD_PATH
        if self.token.type == 'BUILD_PATH':
            self.get_token('BUILD_PATH')
        # build_prod -> build_content
        else:
            self.build_content()

        print(f'{n_token:<3} Statement build_prod parsed correctly')

    def build_content(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered build_content statement')

        # build_prod -> CODE_BLOCK CONTEXT_ID COLON BUILD_PATH program END_CODE_BLOCK
        self.get_token('CODE_BLOCK')
        self.get_token('CONTEXT_ID')
        self.get_token('COLON')
        self.get_token('BUILD_PATH')
        self.program()
        self.get_token('END_CODE_BLOCK')

        print(f'{n_token:<3} Statement build_content parsed correctly')

    def unknow_id_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered unknow_id_prod statement')

        # unknow_id_prod -> CODE_BLOCK program END_CODE_BLOCK
        if self.token.type == 'CODE_BLOCK':
            self.get_token('CODE_BLOCK')
            self.program()
            self.get_token('END_CODE_BLOCK')
        # unknow_id_prod -> SEQUENCE_BLOCK sequence_block_prod END_CODE_BLOCK
        elif self.token.type == 'SEQUENCE_BLOCK':
            self.get_token('SEQUENCE_BLOCK')
            self.sequence_block_prod()
            self.get_token('END_CODE_BLOCK')
        # unknow_id_prod -> value_prod
        else:
            self.value_prod()

        print(f'{n_token:<3} Statement unknow_id_prod parsed correctly')

    def sequence_block_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered sequence_block_prod statement')

        # sequence_block_prod -> DASH value_prod sequence_block_prod
        if self.token.type == 'DASH':
            self.get_token('DASH')
            self.value_prod()
            self.sequence_block_prod()
        # sequence_block_prod -> EPSILON
        else:
            pass

        print(f'{n_token:<3} Statement sequence_block_prod parsed correctly')

    def value_prod(self):
        n_token = self.n_token
        print(f'{n_token:<3} Entered value_prod statement')

        # value_prod -> ID
        if self.token.type == 'ID':
            self.get_token('ID')
        # value_prod -> STRING
        elif self.token.type == 'STRING':
            self.get_token('STRING')
        # value_prod -> EPSILON
        else:
            pass

        print(f'{n_token:<3} Statement value_prod parsed correctly')
