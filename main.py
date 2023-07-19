import tkinter as tk
from tkinter import filedialog as fd, messagebox, Button, ttk
from banco import Banco
from cliente import Cliente
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca

class Tela():
    
    # ---------------------------------------------------------------------------
    # Tela inicial
    # ---------------------------------------------------------------------------
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela Principal')
        self.entrada()
    
    def entrada(self):
        try:
            self.janela.grid_rowconfigure(0, weight=1)
            self.janela.grid_columnconfigure(0, weight=1)
            label = tk.Label(self.janela, text=f'Bem-vindo ao banco {self.banco.nome}!')
            label.grid(row=0, column=0, sticky='ns')
            self.menu(self.janela)
        except AttributeError:
            self.frm = tk.LabelFrame(self.janela, text='Cadastre um banco', width=200, height=200)
            self.frm.grid(row=0, column=0)
            self.lbl_nome_banco = tk.Label(self.frm, text='Nome:')
            self.lbl_nome_banco.grid(row=0, column=0, padx=10, pady=10)
            self.ent_nome_banco = tk.Entry(self.frm)
            self.ent_nome_banco.grid(row=0, column=1, padx=10, pady=10)
            self.lbl_numero_banco = tk.Label(self.frm, text='Número:')
            self.lbl_numero_banco.grid(row=1, column=0, padx=10, pady=10)
            self.ent_numero_banco = tk.Entry(self.frm)
            self.ent_numero_banco.grid(row=1, column=1, padx=10, pady=10)
            self.btn_banco = tk.Button(self.frm, text='Cadastrar Banco', command=self.cad_banco)
            self.btn_banco.grid(row=2, columnspan=2, padx=10, pady=10)
    
    def menu(self, tela):
        mnu_barra = tk.Menu(tela)
        mnu_principal = tk.Menu(mnu_barra, tearoff=0)
        mnu_principal = tk.Menu(mnu_barra, tearoff=0)
        mnu_barra.add_cascade(label='Menu', menu=mnu_principal)
        mnu_principal.add_command(label='Contas', command=self.janela_contas)
        mnu_principal.add_command(label='Clientes', command=self.janela_clientes)
        mnu_principal.add_separator()
        mnu_taxas = tk.Menu(mnu_principal, tearoff=0)
        mnu_principal.add_cascade(label='Taxas', menu=mnu_taxas)
        mnu_taxas.add_command(label='Poupança')
        mnu_taxas.add_command(label='Corrente')
        tela.config(menu=mnu_barra)
    
    # ---------------------------------------------------------------------------
    # Banco
    # ---------------------------------------------------------------------------
    def cad_banco(self):
        self.banco = Banco(self.ent_numero_banco.get(), self.ent_nome_banco.get())
        #----------------------------
        cli1 = Cliente('Daniel', 'Rua dos Bobos, nº 0', '123')
        cli2 = Cliente('Erika', 'Rua Carioca, nº 42', '321')
        cli3 = Cliente('Jo Cely', 'Rua dos Doces, nº 3', '312')
        #----------------------------
        self.banco._clientes = [cli1, cli2, cli3]
        #----------------------------
        c1 = ContaCorrente(cli1)
        c2 = ContaPoupanca(cli2)
        c3 = ContaCorrente(cli3)
        #----------------------------
        self.banco._contas = [c1, c2, c3]
        #----------------------------
        self.frm.destroy()
        self.entrada()
    
    # ---------------------------------------------------------------------------
    # Clientes
    # ---------------------------------------------------------------------------
    def janela_clientes(self):
        
        self.janela_clientes = tk.Toplevel()
        self.janela_clientes.grab_set()
        
        self.tvw_clientes = ttk.Treeview(self.janela_clientes, columns=('id', 'nome', 'endereco', 'cpf'), height=15, show='headings')
        self.tvw_clientes.grid()
        
        self.tvw_clientes.heading('id', text='Id')
        self.tvw_clientes.heading('nome', text='Nome')
        self.tvw_clientes.heading('endereco', text='Endereço')
        self.tvw_clientes.heading('cpf', text='CPF')
        
        self.tvw_clientes.column('id', minwidth=50, width=50)
        self.tvw_clientes.column('nome', minwidth=150, width=150)
        self.tvw_clientes.column('endereco', minwidth=150, width=150)
        self.tvw_clientes.column('cpf', minwidth=120, width=120)
        
        for cliente in self.banco.clientes:
            self.tvw_clientes.insert('', 'end', values=[cliente.id, cliente.nome, cliente.endereco, cliente.cpf])

        self_scb_clientes = tk.Scrollbar(self.janela_clientes, orient=tk.VERTICAL, command=self.tvw_clientes.yview)
        self_scb_clientes.grid(row=0, column=1, sticky='ns')
        self.tvw_clientes.config(yscrollcommand=self_scb_clientes.set)

        self.frm_botoes_clientes = tk.Frame(self.janela_clientes)
        self.frm_botoes_clientes.grid(row=1, column=0)
        
        btn_cadastrar_cliente = tk.Button(self.frm_botoes_clientes, text='Cadastrar', command=self.cadastrar_cliente)
        btn_cadastrar_cliente.grid(row=0, column=0)
        btn_remover_cliente = tk.Button(self.frm_botoes_clientes, text='Remover', command=self.remover_cliente)
        btn_remover_cliente.grid(row=0, column=1)
        btn_editar_cliente = tk.Button(self.frm_botoes_clientes, text='Editar', command=self.editar_cliente)
        btn_editar_cliente.grid(row=0, column=2)

    def cadastrar_cliente(self):
        self.top_cadastrar_cliente = tk.Toplevel()
        self.top_cadastrar_cliente.grab_set()
        
        self.lbl_nome_cliente = tk.Label(self.top_cadastrar_cliente, text='Nome:')
        self.lbl_nome_cliente.grid(row=0, column=0)
        self.ent_nome_cliente = tk.Entry(self.top_cadastrar_cliente)
        self.ent_nome_cliente.grid(row=0, column=1)
        
        self.lbl_endereco = tk.Label(self.top_cadastrar_cliente, text='Endereço:')
        self.lbl_endereco.grid(row=1, column=0)
        self.ent_endereco = tk.Entry(self.top_cadastrar_cliente)
        self.ent_endereco.grid(row=1, column=1)
        
        self.lbl_cpf = tk.Label(self.top_cadastrar_cliente, text='CPF:')
        self.lbl_cpf.grid(row=2, column=0)
        self.ent_cpf_cliente = tk.Entry(self.top_cadastrar_cliente)
        self.ent_cpf_cliente.grid(row=2, column=1)   
        
        self.btn_confirmar_cadastro_cliente = tk.Button(self.top_cadastrar_cliente, text='Confirmar', command=self.confirmar_cadastro_cliente)
        self.btn_confirmar_cadastro_cliente.grid(row=3, column=0)

    def confirmar_cadastro_cliente(self):
        nome = self.ent_nome_cliente.get()
        endereco = self.ent_endereco.get()
        cpf = self.ent_cpf_cliente.get()
        
        self.cliente = Cliente(nome, endereco, cpf)
        id = self.cliente.id
        self.banco.adicionar_cliente(self.cliente)
        
        if nome == '' or endereco == '' or cpf == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_cadastrar_cliente)
        else:
            self.tvw_clientes.insert('', 'end', values=(id, nome, endereco, cpf))
            self.top_cadastrar_cliente.destroy()

    def editar_cliente(self):
        self.item_selecionado = self.tvw_clientes.selection()
        if len(self.item_selecionado) > 1:
            messagebox.showwarning('Aviso', 'Selecione apenas um item')
        elif len(self.item_selecionado) == 0 :
            messagebox.showwarning('Aviso', 'Selecione um cliente para editar os dados')
        else:
            self.valores = self.tvw_clientes.item(self.item_selecionado, 'values')
            
            self.top_editar_cliente = tk.Toplevel()
            self.top_editar_cliente.grab_set()
            
            self.lbl_nome_cliente = tk.Label(self.top_editar_cliente, text='Nome:')
            self.lbl_nome_cliente.grid(row=0, column=0)
            self.ent_nome_cliente = tk.Entry(self.top_editar_cliente)
            self.ent_nome_cliente.grid(row=0, column=1)
            self.ent_nome_cliente.insert('end', self.valores[1])
            
            lbl_endereco = tk.Label(self.top_editar_cliente, text='Endereço:')
            lbl_endereco.grid(row=1, column=0)
            self.ent_endereco = tk.Entry(self.top_editar_cliente)
            self.ent_endereco.grid(row=1, column=1)
            self.ent_endereco.insert('end', self.valores[2])
            
            lbl_cpf = tk.Label(self.top_editar_cliente, text='CPF:')
            lbl_cpf.grid(row=2, column=0)
            self.ent_cpf_cliente = tk.Entry(self.top_editar_cliente)
            self.ent_cpf_cliente.grid(row=2, column=1)
            self.ent_cpf_cliente.insert('end', self.valores[3])
            
            btn_confirmar = tk.Button(self.top_editar_cliente, text='Confirmar', command=self.confirmar_edicao_cliente)
            btn_confirmar.grid(row=3, column=0)

    def confirmar_edicao_cliente(self):
        id = self.valores[0]
        nome = self.ent_nome_cliente.get()
        endereco = self.ent_endereco.get()
        cpf = self.ent_cpf_cliente.get()
        
        if nome == '' or endereco == '' or cpf == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_cadastrar_cliente)
        else:
            for cliente in self.banco.clientes:
                if cliente.id == id:
                    cliente.nome = nome
                    cliente.endereco = endereco
                    cliente.cpf = cpf
                    break

            self.tvw_clientes.item(self.item_selecionado, values=(id, nome, endereco, cpf))
            self.top_editar_cliente.destroy()
            for cliente in self.banco.clientes:
                print(cliente.id, end=' - ')
                print(cliente.nome, end=' - ')
                print(cliente.endereco, end=' - ')
                print(cliente.cpf)

    def remover_cliente(self):
        clientes_selecionados = [(self.tvw_clientes.item(cli, 'values'), cli) for cli in self.tvw_clientes.selection()]
        for cliente in clientes_selecionados:
            conta_ativa = [conta for conta in self.banco.contas if conta.titular.id == cliente[0][0] and conta.status]
            if conta_ativa:
                messagebox.showinfo('Aviso', f'Não é possível remover o cliente {cliente[0][1]} pois há contas ativas me seu nome.', parent=self.top_cadastrar_cliente)
            else:
                for c in self.banco.clientes:
                    if cliente[0][0] == c.id:
                        self.banco.clientes.remove(c)
                        self.tvw_clientes.delete(cliente[1])
                        break

    # ---------------------------------------------------------------------------
    # Contas
    # ---------------------------------------------------------------------------
    def janela_contas(self):
        self.tlv_contas = tk.Toplevel(self.janela)
        self.tlv_contas.title('Contas')
        
        self.tvw_contas = ttk.Treeview(self.tlv_contas, columns=('id', 'titular', 'saldo', 'status', 'tipo'), height=15, show='headings')
        self.tvw_contas.grid()
        
        self.tvw_contas.heading('id', text='Id')
        self.tvw_contas.heading('titular', text='Titular')
        self.tvw_contas.heading('saldo', text='Saldo')
        self.tvw_contas.heading('status', text='Status')
        self.tvw_contas.heading('tipo', text='Tipo')
        
        self.tvw_contas.column('id', minwidth=50, width=50)
        self.tvw_contas.column('titular', minwidth=150, width=150)
        self.tvw_contas.column('saldo', minwidth=100, width=150)
        self.tvw_contas.column('status', minwidth=75, width=50)
        self.tvw_contas.column('tipo', minwidth=75, width=120)

        self.carrega_tvw_conta()
        
        self_scb_contas = tk.Scrollbar(self.tlv_contas, orient=tk.VERTICAL, command=self.tvw_contas.yview)
        self_scb_contas.grid(row=0, column=1, sticky='ns')
        self.tvw_contas.config(yscrollcommand=self_scb_contas.set)

        self.frm_botoes_contas = tk.Frame(self.tlv_contas)
        self.frm_botoes_contas.grid(row=1, column=0)
        
        btn_abrir_conta = tk.Button(self.frm_botoes_contas, text='Abrir', command=self.abrir_conta)
        btn_abrir_conta.grid(row=0, column=0)
        btn_encerrar_conta = tk.Button(self.frm_botoes_contas, text='Encerrar', command=self.encerrar_conta)
        btn_encerrar_conta.grid(row=0, column=1)
        btn_operacoes_conta = tk.Button(self.frm_botoes_contas, text='Alterar saldo', command=self.operacoes)
        btn_operacoes_conta.grid(row=0, column=2)
        btn_extrato_conta = tk.Button(self.frm_botoes_contas, text='Extrato', command=self.extrato)
        btn_extrato_conta.grid(row=0, column=3)

    def carrega_tvw_conta(self):
        itens = self.tvw_contas.get_children()        
        for item in itens:
            self.tvw_contas.delete(item)
        for conta in self.banco.contas:
            self.tvw_contas.insert('', 'end', values=[conta.id, conta.titular.nome, f'R$ {conta.saldo:.2f}', 'Aberta' if conta.status else 'Fechada', 'C/C' if isinstance(conta, ContaCorrente) else 'C/P'])
    
    def abrir_conta(self):        
        contas_selecionados = [(self.tvw_contas.item(conta, 'values'), conta) for conta in self.tvw_contas.selection()]
        if contas_selecionados:
            for conta_selecionada in contas_selecionados:
                conta = [c for c in self.banco.contas if c.id == conta_selecionada[0][0]][0]
                if not conta.status:
                    conta.status = True
                    self.carrega_tvw_conta()
        else:
            self.top_abrir_conta = tk.Toplevel(self.tlv_contas)
            self.top_abrir_conta.grab_set()
            
            self.cliente_selecionado = tk.StringVar()
            lista_clientes = [f'{cliente.id} - {cliente.nome}' for cliente in self.banco.clientes]
            
            self.cbx_titular_conta = ttk.Combobox(self.top_abrir_conta, values=lista_clientes, textvariable=self.cliente_selecionado)
            self.cbx_titular_conta.grid()
            
            self.tipo_conta = tk.StringVar()
            tipo_conta_corrente = tk.Radiobutton(self.top_abrir_conta, text='Corrente', variable=self.tipo_conta, value='Corrente')
            tipo_conta_corrente.grid()
            tipo_conta_poupanca = tk.Radiobutton(self.top_abrir_conta, text='Poupança', variable=self.tipo_conta, value='Poupança')
            tipo_conta_poupanca.grid()
            
            btn_abrir_conta = Button(self.top_abrir_conta, text='Abrir Conta', command=self.confirmar_abrir_conta)
            btn_abrir_conta.grid()

    def confirmar_abrir_conta(self):
        titular = [cli for cli in self.banco.clientes if self.cliente_selecionado.get().split(' - ')[0] == str(cli.id)][0]
        tipo = self.tipo_conta.get()
        if titular == '' or tipo == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_abrir_conta)
        else:
            if tipo == 'Corrente':
                conta = ContaCorrente(titular)
            else:
                conta = ContaPoupanca(titular)
            
            self.banco.adicionar_conta(conta)
            
            self.carrega_tvw_conta()
            self.top_abrir_conta.destroy()

    def encerrar_conta(self):
        contas_selecionados = [(self.tvw_contas.item(conta, 'values'), conta) for conta in self.tvw_contas.selection()]
        for conta_selecionada in contas_selecionados:
            conta = [conta for conta in self.banco.contas if conta_selecionada[0][0] == str(conta.id)][0]
            if not conta.saldo:
                conta.status = False
                self.carrega_tvw_conta()
            else:
                messagebox.showinfo('Aviso', f'Não é possível encerrar a conta {conta.id} pois ainda possui saldo.', parent=self.tlv_contas)

    def operacoes(self):
        self.contas_selecionados = [(self.tvw_contas.item(conta, 'values'), conta) for conta in self.tvw_contas.selection()]
        if self.contas_selecionados == []:
            messagebox.showinfo('Aviso', f'Selecione uma conta para alterar seu saldo!', parent=self.tlv_contas)
        elif len(self.contas_selecionados) > 1:
            messagebox.showinfo('Aviso', f'Selecione apenas uma conta!', parent=self.tlv_contas)
        else:
            self.conta_selecionada = [c for c in self.banco.contas if c.id == self.contas_selecionados[0][0][0]][0]
            if self.conta_selecionada.status:
                self.top_operacoes = tk.Toplevel(self.tlv_contas)
                self.top_operacoes.grab_set()
                
                lbl_saldo = tk.Label(self.top_operacoes, text=f'Saldo da conta: R$ {self.contas_selecionados[0][0][2]}')
                lbl_saldo.pack()
                
                lbl_ent = tk.Label(self.top_operacoes, text=f'Insira o valor: ')
                lbl_ent.pack()
                self.valor_operacao = tk.Entry(self.top_operacoes)
                self.valor_operacao.pack()
                
                btn_operacao_depositar = tk.Button(self.top_operacoes, text='Depositar', command=self.operacao_depositar)
                btn_operacao_depositar.pack()
                btn_operacao_sacar = tk.Button(self.top_operacoes, text='Sacar', command=self.operacao_sacar)
                btn_operacao_sacar.pack()
            else:
                messagebox.showinfo('Aviso', f'Esta conta está desativada!', parent=self.tlv_contas)
    
    def operacao_depositar(self):
        conta = [c for c in self.banco.contas if c.id == self.contas_selecionados[0][0][0]][0]
        valor = float(self.valor_operacao.get())
        if isinstance(conta, ContaCorrente):
            valor -= valor * self.banco.taxa_cc
        conta.deposita(valor)
        self.carrega_tvw_conta()
        self.top_operacoes.destroy()
    
    def operacao_sacar(self):
        conta = [c for c in self.banco.contas if c.id == self.contas_selecionados[0][0][0]][0]
        valor = float(self.valor_operacao.get())
        if isinstance(conta, ContaCorrente):
            valor += valor * self.banco.taxa_cc
        if conta.saca(valor):
            self.carrega_tvw_conta()
            self.top_operacoes.destroy()
        else:
            messagebox.showinfo('Aviso', f'Saldo insuficiente!', parent=self.tlv_contas)
        
    def extrato(self):
        self.contas_selecionados = [(self.tvw_contas.item(conta, 'values'), conta) for conta in self.tvw_contas.selection()]
        conta = [c for c in self.banco.contas if c.id == self.contas_selecionados[0][0][0]][0]
        destino = fd.asksaveasfile(filetypes=[('Texto', '*.txt')], initialfile=f'{conta.id}', defaultextension='.txt')
        for transacao in conta.historico:
            destino.write(f'{transacao}\n')
        destino.write(f'\n\nSaldo Total da Conta: R$ {conta.saldo:.2f}')
        
app = tk.Tk()
janelaPrincipal = Tela(app)
app.mainloop()