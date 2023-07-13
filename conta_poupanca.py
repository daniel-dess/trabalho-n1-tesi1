from conta import Conta


class ContaPoupanca(Conta):
    def __init__(self, titular, taxa_juros):
        super().__init__(titular)
        self.taxa_juros = taxa_juros

    def atualizar_saldo(self):
        self.saldo += self.saldo * self.taxa_juros