import datetime

class Conta:
        
    __slots__ = ['_id', '_titular', '_saldo', '_status', '_historico']

    _numero = 0

    def __init__(self, t):
        Conta._numero += 1
        self._id = f'{Conta._numero:06d}'
        self._titular = t
        self._saldo = 0.0
        self._status = True
        self._historico = []

    @property
    def id(self):
        return self._id

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, novo_titular):
        self._titular = novo_titular

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, novo_saldo):
        self._saldo = novo_saldo

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, novo_status):
        self._status = novo_status

    @property
    def historico(self):
        return self._historico

    def saca(self, valor):
        if self._saldo < valor:
            return False
        else:
            data = datetime.datetime.now().strftime("%d-%m-%Y")
            self._saldo = self._saldo - valor
            self._historico.append(f'{data},saque,{valor:.2f}')
            return True

    def deposita(self, valor):
        data = datetime.datetime.now().strftime("%d-%m-%Y")
        self._saldo += valor
        self._historico.append(f'{data},deposito,{valor:.2f}')
            
    def extrato(self):
        arquivo = open(f'{self._id}.txt', 'w')
        for transacao in self._historico:
            arquivo.write(f'{transacao}\n\n')
        arquivo.close()