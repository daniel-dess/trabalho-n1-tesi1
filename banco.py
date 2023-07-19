from conta_poupanca import ContaPoupanca


class Banco:    
    
    __slots__ = ['_numero', '_nome', '_contas', '_clientes', '_taxa_cp','_taxa_cc']
    
    def __init__(self, numero, nome):
        self._numero = numero
        self._nome = nome
        self._contas = []
        self._clientes = []
        self._taxa_cp = 0
        self._taxa_cc = 0
        
    @property
    def numero(self):
        return self._numero
    
    @numero.setter
    def numero(self, numero):
        self._numero = numero

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome
 
    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def clientes(self):
        return self._clientes
    
    def adicionar_cliente(self, cliente):
        self._clientes.append(cliente)
     
    @property
    def taxa_cp(self):
        return self._taxa_cp
    
    @taxa_cp.setter
    def taxa_cp(self, taxa):
        self._taxa_cp = taxa
                
    @property
    def taxa_cc(self):
        return self._taxa_cc
    
    @taxa_cc.setter
    def taxa_cc(self, taxa):
        self._taxa_cc = taxa
        
    def rendimento_cp(self):
        for conta in self.contas:
            if isinstance(conta, ContaPoupanca):
                conta.saldo += conta.saldo * self.taxa_cp