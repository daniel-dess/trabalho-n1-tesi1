import datetime

class Conta:
        
    __slots__ = ['_id', '_titular', '_saldo', '_clientes', '_status', '_historico']

    _numero = 1 

    def __init__(self, t):
        self._id = Conta._numero
        Conta._numero += 1
        self._titular = t
        self._saldo = 0
        self._status = True
        self._historico = []

    @property
    def id(self):
        return self._id

    @property
    def titular(self):
        return self._titular

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
        if self._saldo >= valor and self._status:
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            self._saldo = self._saldo - valor
            self._historico.append(f'Saque de R$ {valor:.2f} no dia {data}\nSaldo: R$ {self._saldo:.2f}')
            return True
        return False

    def deposita(self, valor):
        if self._status:
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            self._saldo += valor
            self._historico.append(f'Deposito de R$ {valor:.2f} no dia {data}\nSaldo: R$ {self._saldo:.2f}')
            return True
        return False
    
    def encerrar_conta(self):
        if self._saldo == 0:
            self._status = False
            return True
        return False
            
    def extrato(self):
        arquivo = open(f'{self._id}', 'w')
        for transacao in self._historico:
            arquivo.write(f'{transacao}\n\n')
        arquivo.close()