class Cliente:
    
    __slots__ = ['_id', '_nome', '_endereco', '_cpf']
    
    _numero = 0
    
    def __init__(self, nome, endereco, cpf):
        Cliente._numero += 1
        self._id = f'{Cliente._numero:06d}'
        self._nome = nome
        self._endereco = endereco
        self._cpf = cpf
    
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        self._nome = novo_nome

    @property
    def endereco(self):
        return self._endereco

    @endereco.setter
    def endereco(self, novo_endereco):
        self._endereco = novo_endereco

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, novo_cpf):
        self._cpf = novo_cpf