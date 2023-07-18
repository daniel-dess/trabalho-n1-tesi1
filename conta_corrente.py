import datetime
from conta import Conta


class ContaCorrente(Conta):
    def __init__(self, titular, desconto):
        super().__init__(titular)
        self.desconto = desconto

    def saca(self, valor):
        desconto = self.desconto
        if self.saldo >= valor + desconto and self.status:
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            self.saldo -= valor + desconto
            self.historico.append(f'Saque de R$ {valor:.2f} no dia {data}\nSaldo: R$ {self.saldo:.2f}')
            return True
        return False

    def deposita(self, valor):
        desconto = self.desconto
        if self.status:
            data = datetime.datetime.now().strftime("%d/%m/%Y")
            self.saldo += valor - desconto
            self.historico.append(f'Depósito de R$ {valor:.2f} no dia {data}\nSaldo: R$ {self.saldo:.2f}')
            return True
        return False
