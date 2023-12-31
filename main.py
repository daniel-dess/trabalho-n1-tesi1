from functools import reduce
import tkinter as tk
from tkinter import filedialog as fd, messagebox, Button, ttk
from banco import Banco
from cliente import Cliente
from conta_corrente import ContaCorrente
from conta_poupanca import ContaPoupanca

class Tela():
    
    # Tela inicial
    def __init__(self, master):
          # Configurações iniciais da janela principal
        self.janela = master
        self.janela.title('Sistema de Gerenciamento Bancário')
        
        self.janela.minsize(600, 600)
        self.s = 0
        
        self.frm = tk.Frame(self.janela, background='white', width=800)
        self.frm.pack(fill=tk.Y, expand=True)
        self.frm.grid_columnconfigure(0, minsize=800)
        
        estilo_treeview = ttk.Style()
        estilo_treeview.configure('Treeview', font=('Constantia', 10))
        
        self.menu()
        
        self.janela_bancos()

    # Banco    
    def janela_bancos(self):
        
        self.limpar_tela(self.frm)
        
        if Banco._bancos == []:
            
            if self.s == 0:
                self.s = 1
                tlv_bv = tk.Toplevel()
                tlv_bv.title('Boas Vindas!')
                tlv_bv.geometry('500x400')
                tlv_bv.grab_set()
                
                tlv_bv.grid_rowconfigure(0, weight=1)
                tlv_bv.grid_rowconfigure(1, weight=1)
                tlv_bv.grid_rowconfigure(2, weight=1)
                tlv_bv.grid_rowconfigure(3, weight=1)
                tlv_bv.grid_columnconfigure(0, weight=1)
                
                lbl1 = tk.Label(tlv_bv, text='Bem-vindo ao nosso sistema!')
                lbl1.grid(row=0, column=0, pady=20)
                
                lbl2 = tk.Label(tlv_bv, text='Aqui você pode realizar diversas operações como gerenciar clientes e contas, bem como definir taxas e serviços.', wraplength=250)
                lbl2.grid(row=1, column=0, pady=20)
                
                lbl3 = tk.Label(tlv_bv, text='Para iniciar, cadastre um banco para realizar as operações!', wraplength=250)
                lbl3.grid(row=2, column=0, pady=20)
                
                def comando():
                    self.cadastrar_banco()
                    tlv_bv.destroy()
                
                btn = tk.Button(tlv_bv, text='OK', command=comando)
                btn.grid(row=3, column=0, pady=20)

                self.config_text(tlv_bv)
            else:
                self.cadastrar_banco()
        
        self.frm.grid_rowconfigure(0, weight=1)
        self.frm.grid_rowconfigure(1, weight=1)
        self.frm.grid_rowconfigure(2, weight=1)
        
        lbl = tk.Label(self.frm, text='Bancos Cadastrados')
        lbl.grid(row=0, column=0)
                
        frm = tk.Frame(self.frm)
        frm.grid(row=1, column=0)
        self.tvw_bancos = ttk.Treeview(frm, columns=('numero', 'nome', 'contas', 'clientes', 'taxa_cp','taxa_cc', 'status'), height=20, show='headings')
        self.tvw_bancos.grid(row=0, column=0)
        
        self.tvw_bancos.heading('numero', text='CNPJ')
        self.tvw_bancos.heading('nome', text='Razão Social')
        self.tvw_bancos.heading('contas', text='Contas ativas')
        self.tvw_bancos.heading('clientes', text='Clientes')
        self.tvw_bancos.heading('taxa_cp', text='Rendimento C/P')
        self.tvw_bancos.heading('taxa_cc', text='Taxas C/C')
        self.tvw_bancos.heading('status', text='Status')
        
        self.tvw_bancos.column('numero', width=100)
        self.tvw_bancos.column('nome', width=200)
        self.tvw_bancos.column('contas', width=100)
        self.tvw_bancos.column('clientes', width=100)
        self.tvw_bancos.column('taxa_cp', width=100)
        self.tvw_bancos.column('taxa_cc', width=100)
        self.tvw_bancos.column('status', width=100)
        
        for banco in Banco._bancos:
            self.tvw_bancos.insert('', 'end', values=[banco.numero, banco.nome, len([conta for conta in banco.contas if conta.status]), len(banco.clientes), banco.taxa_cp, banco.taxa_cc, 'Em uso' if banco.numero == self.banco_em_uso.numero else '--'])

        self_scb_bancos = tk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tvw_bancos.yview)
        self_scb_bancos.grid(row=0, column=1, sticky='ns')
        self.tvw_bancos.config(yscrollcommand=self_scb_bancos.set)

        frm_botoes_bancos = tk.LabelFrame(self.frm, text='Opções')
        frm_botoes_bancos.grid(row=2, column=0)
        
        def selecionar_banco():
            selecao = self.tvw_bancos.selection()
            if len(selecao) == 0:
                messagebox.showerror('Erro', 'Escolha um banco para selecionar para uso!')
            elif len(selecao) > 1:
                messagebox.showerror('Erro', 'Selecione apenas um banco!')
            else:
                valores = self.tvw_bancos.item(selecao, 'values')
                self.banco_em_uso = [banco for banco in Banco._bancos if valores[0] == banco.numero][0]
                messagebox.showinfo('Aviso', f'Banco {self.banco_em_uso.nome} está em uso!')
                self.janela_bancos()
        
        btn_cadastrar_banco = tk.Button(frm_botoes_bancos, text='Cadastrar novo banco', command=self.cadastrar_banco)
        btn_cadastrar_banco.grid(row=0, column=0, padx=5, pady=5)
        btn_editar_banco = tk.Button(frm_botoes_bancos, text='Editar Dados', command=self.editar_banco)
        btn_editar_banco.grid(row=1, column=0, padx=5, pady=5)
        btn_selecionar_banco = tk.Button(frm_botoes_bancos, text='Selecionar para uso', command=selecionar_banco)
        btn_selecionar_banco.grid(row=2, column=0, padx=5, pady=5)
        
        self.config_text(self.frm)
     
    def cadastrar_banco(self):
        
        self.top_cadastrar_banco = tk.Toplevel()
        self.top_cadastrar_banco.title('Cadastrar Banco')
        self.top_cadastrar_banco.geometry('500x400')
        self.top_cadastrar_banco.grab_set()
        self.top_cadastrar_banco.grid_columnconfigure(0, weight=1)
        self.top_cadastrar_banco.grid_rowconfigure(0, weight=1)
        
        lbl_frm = tk.LabelFrame(self.top_cadastrar_banco, text='Insira os dados do banco', width=200, height=200)
        lbl_frm.grid(row=0, column=0)
        
        lbl_nome_banco = tk.Label(lbl_frm, text='Razão social:')
        lbl_nome_banco.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.ent_nome_banco = tk.Entry(lbl_frm)
        self.ent_nome_banco.grid(row=0, column=1, padx=10, pady=10)
        
        lbl_numero_banco = tk.Label(lbl_frm, text='CNPJ:')
        lbl_numero_banco.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        
        self.ent_numero_banco = tk.Entry(lbl_frm)
        self.ent_numero_banco.grid(row=1, column=1, padx=10, pady=10)
        
        btn_banco = tk.Button(lbl_frm, text='Cadastrar Banco', command=self.confirmar_cadastro_banco)
        btn_banco.grid(row=2, columnspan=2, padx=10, pady=10)
        
        self.config_text(self.top_cadastrar_banco)
    
    def confirmar_cadastro_banco(self):
        
        numero_banco = self.ent_numero_banco.get()
        nome_banco = self.ent_nome_banco.get()
        
        if numero_banco == '' or nome_banco == '':
            messagebox.showerror('Dados Incompletos', ' Dados incompletos, os campos Razão Social e CNPJ são obrigatórios!', parent=self.top_cadastrar_banco)
        else:
            mesmo_cnpj = [banco for banco in Banco._bancos if banco.numero == numero_banco]
            if mesmo_cnpj:
                messagebox.showerror('Banco existente', 'Já existe um banco com o mesmo CNPJ!\n Por favor, verifique o CNPJ informado e tente novamente.', parent=self.top_cadastrar_banco)
            else:
                self.banco_em_uso = Banco(numero_banco, nome_banco)
                Banco._bancos.append(self.banco_em_uso)
                messagebox.showinfo('Confirmação', f'Banco {self.banco_em_uso.nome} cadastrado com sucesso!', parent=self.top_cadastrar_banco)
                self.janela_bancos()
                self.top_cadastrar_banco.destroy()
    
    def editar_banco(self):
        
        self.item_selecionado = self.tvw_bancos.selection()
        
        if len(self.item_selecionado) > 1:
            self.janela_bancos()
            messagebox.showwarning('Aviso', 'Selecione apenas um item')
            
        elif len(self.item_selecionado) == 0 :
            messagebox.showwarning('Aviso', 'Selecione um banco para editar os dados')
            
        else:
            self.valores = self.tvw_bancos.item(self.item_selecionado, 'values')
            self.banco_selecionado = [banco for banco in Banco._bancos if self.valores[0] == banco.numero][0]
            self.top_editar_banco = tk.Toplevel()
            self.top_editar_banco.title('Editar Banco')
            self.top_editar_banco.geometry('500x400')
            self.top_editar_banco.grab_set()
            self.top_editar_banco.grid_columnconfigure(0, weight=1)
            self.top_editar_banco.grid_rowconfigure(0, weight=1)
            self.top_editar_banco.grid_rowconfigure(1, weight=1)
            self.top_editar_banco.grid_rowconfigure(2, weight=1)
            
            lbl_frm1 = tk.LabelFrame(self.top_editar_banco, text='Dados cadastrais', width=400, height=400)
            lbl_frm1.grid(row=0, column=0)
            lbl_frm1.grid_columnconfigure(0, minsize=200)
            lbl_frm1.grid_columnconfigure(1, minsize=200)

            self.lbl_nome_banco = tk.Label(lbl_frm1, text='Razão Social:')
            self.lbl_nome_banco.grid(row=0, column=0, sticky='w')
            self.ent_nome_banco = tk.Entry(lbl_frm1)
            self.ent_nome_banco.grid(row=0, column=1)
            self.ent_nome_banco.insert('end', self.banco_selecionado.nome)
            
            lbl_cnpj = tk.Label(lbl_frm1, text='CNPJ:')
            lbl_cnpj.grid(row=1, column=0, sticky='w')
            self.ent_cnpj = tk.Entry(lbl_frm1)
            self.ent_cnpj.grid(row=1, column=1)
            self.ent_cnpj.insert('end', self.banco_selecionado.numero)
            
            lbl_frm2 = tk.LabelFrame(self.top_editar_banco, text='Taxas')
            lbl_frm2.grid(row=1, column=0)
            lbl_frm2.grid_columnconfigure(0, minsize=180)
            lbl_frm2.grid_columnconfigure(1, minsize=180)
            
            lbl_taxa_cp = tk.Label(lbl_frm2, text='Rendimento C/P: ')
            lbl_taxa_cp.grid(row=0, column=0, sticky='w')
            self.ent_taxa_cp = tk.Entry(lbl_frm2)
            self.ent_taxa_cp.grid(row=0, column=1)
            if self.banco_selecionado.taxa_cp != 0.0:
                self.ent_taxa_cp.insert('end', self.banco_selecionado.taxa_cp)
            
            lbl_taxa_cc = tk.Label(lbl_frm2, text='Taxa Serviço C/C: ')
            lbl_taxa_cc.grid(row=1, column=0, sticky='w')
            self.ent_taxa_cc = tk.Entry(lbl_frm2)
            self.ent_taxa_cc.grid(row=1, column=1)
            if self.banco_selecionado.taxa_cc != 0.0:
                self.ent_taxa_cc.insert('end', self.banco_selecionado.taxa_cc)
            
            btn_confirmar = tk.Button(self.top_editar_banco, text='Confirmar', command=self.confirmar_edicao_banco)
            btn_confirmar.grid(row=2, column=0)
            
            self.config_text(self.top_editar_banco)
    
    def confirmar_edicao_banco(self):
        nome = self.ent_nome_banco.get()
        cnpj = self.ent_cnpj.get()
        taxa_cp = self.ent_taxa_cp.get()
        taxa_cc = self.ent_taxa_cc.get()        
        if nome == '' or cnpj == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_editar_banco)
        else:
            self.banco_selecionado.nome = nome
            self.banco_selecionado.numero = cnpj
            self.banco_selecionado.taxa_cp = float(taxa_cp) if taxa_cp != '' else 0.0
            self.banco_selecionado.taxa_cc = float(taxa_cc) if taxa_cc != '' else 0.0
            self.janela_bancos()
            self.top_editar_banco.destroy()
    
    # Clientes
    def janela_clientes(self):

        if Banco._bancos == []:
            messagebox.showerror('Erro', 'Não há bancos cadastrados!')
            return self.janela_bancos()
            
        else:
            
            self.limpar_tela(self.frm)
            
            self.frm.grid_columnconfigure(0, weight=1)
            self.frm.grid_rowconfigure(0, weight=1)
            self.frm.grid_rowconfigure(1, weight=1)
            self.frm.grid_rowconfigure(2, weight=1)
            
            lbl = tk.Label(self.frm, text='Clientes')
            lbl.grid(row=0, column=0)
            
            frm = tk.Frame(self.frm)
            frm.grid(row=1, column=0)
            
            self.tvw_clientes = ttk.Treeview(frm, columns=('id', 'nome', 'endereco', 'cpf'), height=20, show='headings')
            self.tvw_clientes.grid()
            
            self.tvw_clientes.heading('id', text='ID')
            self.tvw_clientes.heading('nome', text='Nome')
            self.tvw_clientes.heading('endereco', text='Endereço')
            self.tvw_clientes.heading('cpf', text='CPF')
            
            self.tvw_clientes.column('id', width=100)
            self.tvw_clientes.column('nome', width=200)
            self.tvw_clientes.column('endereco', width=300)
            self.tvw_clientes.column('cpf', width=200)
            
            for cliente in self.banco_em_uso.clientes:
                self.tvw_clientes.insert('', 'end', values=[cliente.id, cliente.nome, cliente.endereco, cliente.cpf])

            self_scb_clientes = tk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tvw_clientes.yview)
            self_scb_clientes.grid(row=0, column=1, sticky='ns')
            self.tvw_clientes.config(yscrollcommand=self_scb_clientes.set)

            frm_botoes_clientes = tk.LabelFrame(self.frm, text='Opções')
            frm_botoes_clientes.grid(row=2, column=0)
            
            btn_cadastrar_cliente = tk.Button(frm_botoes_clientes, text='Cadastrar', command=self.cadastrar_cliente)
            btn_cadastrar_cliente.grid(row=0, column=0, padx=5, pady=5)
            btn_remover_cliente = tk.Button(frm_botoes_clientes, text='Remover', command=self.remover_cliente)
            btn_remover_cliente.grid(row=1, column=0, padx=5, pady=5)
            btn_editar_cliente = tk.Button(frm_botoes_clientes, text='Editar', command=self.editar_cliente)
            btn_editar_cliente.grid(row=2, column=0, padx=5, pady=5)
            
            self.config_text(frm_botoes_clientes)
            self.config_text(self.frm)

    def cadastrar_cliente(self):
        
        if Banco._bancos == []:
            messagebox.showerror('Erro', 'Não há bancos cadastrados!')
            return self.janela_bancos()
        
        self.janela_clientes()
        
        self.top_cadastrar_cliente = tk.Toplevel()
        self.top_cadastrar_cliente.grab_set()
        self.top_cadastrar_cliente.title('Cadastrar Cliente')
        self.top_cadastrar_cliente.geometry('500x400')
        
        self.top_cadastrar_cliente.grid_columnconfigure(0, weight=1)
        self.top_cadastrar_cliente.grid_rowconfigure(0, weight=1)
        self.top_cadastrar_cliente.grid_rowconfigure(1, weight=1)
        
        lbl_frm = tk.LabelFrame(self.top_cadastrar_cliente, text='Insira os dados do cliente', width=200, height=200)
        lbl_frm.grid(row=0, column=0)
        
        self.lbl_nome_cliente = tk.Label(lbl_frm, text='Nome:')
        self.lbl_nome_cliente.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ent_nome_cliente = tk.Entry(lbl_frm)
        self.ent_nome_cliente.grid(row=0, column=1, padx=10, pady=10)
        
        self.lbl_endereco = tk.Label(lbl_frm, text='Endereço:')
        self.lbl_endereco.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.ent_endereco = tk.Entry(lbl_frm)
        self.ent_endereco.grid(row=1, column=1, padx=10, pady=10)
        
        self.lbl_cpf = tk.Label(lbl_frm, text='CPF:')
        self.lbl_cpf.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.ent_cpf_cliente = tk.Entry(lbl_frm)
        self.ent_cpf_cliente.grid(row=2, column=1, padx=10, pady=10)
        
        btn_confirmar_cadastro_cliente = tk.Button(self.top_cadastrar_cliente, text='Confirmar', command=self.confirmar_cadastro_cliente)
        btn_confirmar_cadastro_cliente.grid(row=1, columnspan=2, padx=10, pady=10)
        
        self.config_text(self.top_cadastrar_cliente)

    def cpf_valido(self, cpf):
        copia_cpf = cpf
        if len(copia_cpf) == 11:
            cpf_valido = copia_cpf[:9]
            a = reduce(lambda x,y: x+y, [int(cpf_valido[i])*(10-i) for i in range(9)]) % 11
            if a < 2:
                cpf_valido += '0'
            else:
                cpf_valido += str(11-a)
            b = reduce(lambda x,y: x+y, [int(cpf_valido[i])*(11-i) for i in range(10)]) %11
            if b < 2:
                cpf_valido += '0'
            else:
                cpf_valido += str(11-b)
            
            if copia_cpf == cpf_valido:
                return True
        return False
    
    def confirmar_cadastro_cliente(self):
        nome = self.ent_nome_cliente.get()
        endereco = self.ent_endereco.get()
        cpf = ''.join([i for i in self.ent_cpf_cliente.get() if i.isdigit()])
        if nome == '' or endereco == '' or cpf == '':
            messagebox.showinfo('Aviso', 'Todos os campos são obrigatórios.')
        else:
            cpf_repetido = [cliente for cliente in self.banco_em_uso._clientes if cliente.cpf == cpf]
            if cpf_repetido:
                messagebox.showinfo('Aviso', 'Já existe um cliente cadastrado com o mesmo CPF.', parent=self.top_cadastrar_cliente)
            elif self.cpf_valido(cpf):
                self.cliente = Cliente(nome, endereco, cpf)
                self.banco_em_uso.adicionar_cliente(self.cliente)
                self.janela_clientes()
                messagebox.showinfo('Confirmação', f'Cliente {self.cliente.nome} cadastrado com sucesso!', parent=self.top_cadastrar_cliente)
                self.top_cadastrar_cliente.destroy()
            else:
                messagebox.showinfo('Aviso', 'Insira um CPF válido.', parent=self.top_cadastrar_cliente)

    def editar_cliente(self):
        
        self.item_selecionado = self.tvw_clientes.selection()
        
        if len(self.item_selecionado) > 1:
            messagebox.showwarning('Aviso', 'Selecione apenas um item')
            self.janela_clientes()
        
        elif len(self.item_selecionado) == 0 :
            messagebox.showwarning('Aviso', 'Selecione um cliente para editar os dados')
        
        else:
            self.valores = self.tvw_clientes.item(self.item_selecionado, 'values')
            
            self.top_editar_cliente = tk.Toplevel()
            self.top_editar_cliente.title('Editar Cliente')
            self.top_editar_cliente.grab_set()
            self.top_editar_cliente.geometry('500x400')
            
            self.top_editar_cliente.grid_columnconfigure(0, weight=1)
            self.top_editar_cliente.grid_rowconfigure(0, weight=1)
            
            lbl_frm = tk.LabelFrame(self.top_editar_cliente, text='Altere os dados para edição')
            lbl_frm.grid(row=0, column=0)
            
            self.lbl_nome_cliente = tk.Label(lbl_frm, text='Nome:')
            self.lbl_nome_cliente.grid(row=0, column=0, padx=5, pady=5)
            self.ent_nome_cliente = tk.Entry(lbl_frm)
            self.ent_nome_cliente.grid(row=0, column=1, padx=5, pady=5)
            self.ent_nome_cliente.insert('end', self.valores[1])
            
            lbl_endereco = tk.Label(lbl_frm, text='Endereço:')
            lbl_endereco.grid(row=1, column=0, padx=5, pady=5)
            self.ent_endereco = tk.Entry(lbl_frm)
            self.ent_endereco.grid(row=1, column=1, padx=5, pady=5)
            self.ent_endereco.insert('end', self.valores[2])
            
            lbl_cpf = tk.Label(lbl_frm, text='CPF:')
            lbl_cpf.grid(row=2, column=0, padx=5, pady=5)
            self.ent_cpf_cliente = tk.Entry(lbl_frm)
            self.ent_cpf_cliente.grid(row=2, column=1, padx=5, pady=5)
            self.ent_cpf_cliente.insert('end', self.valores[3])
            self.ent_cpf_cliente.config(state='readonly')
            
            btn_confirmar = tk.Button(lbl_frm, text='Confirmar', command=self.confirmar_edicao_cliente)
            btn_confirmar.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
            
            self.config_text(self.top_editar_cliente)

    def confirmar_edicao_cliente(self):
        id = self.valores[0]
        nome = self.ent_nome_cliente.get()
        endereco = self.ent_endereco.get()
        
        if nome == '' or endereco == '':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_editar_cliente)
        else:
            for cliente in self.banco_em_uso.clientes:
                if cliente.id == id:
                    cliente.nome = nome
                    cliente.endereco = endereco
                    messagebox.showinfo('Confirmação', f'Cliente {self.cliente.nome} cadastrado com sucesso!', parent=self.top_editar_cliente)
                    break

            self.janela_clientes()
            self.top_editar_cliente.destroy()

    def remover_cliente(self):
        selecao = [self.tvw_clientes.item(cli, 'values') for cli in self.tvw_clientes.selection()]
        if selecao == []:
            messagebox.showinfo('Aviso', 'Selecione um cliente para removê-lo!')
        elif len(selecao) > 1:
            messagebox.showinfo('Aviso', 'Selecione apenas um cliente para removê-lo!')
        else:
            cli = [cliente for cliente in self.banco_em_uso.clientes if selecao[0][0] == cliente.id][0]
            contas = [conta for conta in self.banco_em_uso.contas if conta.titular.id == cli.id]
            if contas:
                messagebox.showinfo('Aviso', f'Não é possível remover o cliente {cli.nome} pois há contas me seu nome.')
            else:
                if messagebox.askyesno('Confirmação remoção', f'Deseja mesmo remover o cliente {cli.nome}?'):
                    self.banco_em_uso.clientes.remove(cli)
                    c = [conta for conta in self.banco_em_uso.contas if conta.titular.id == cli.id]
                    for conta in c:
                        self.banco_em_uso.contas.remove(conta)
        self.janela_clientes()

    # Contas
    def janela_contas(self):

        if Banco._bancos == []:
            messagebox.showerror('Erro', 'Não há bancos cadastrados!')
            return self.janela_bancos()
            
        else:
            
            self.limpar_tela(self.frm)
            
            self.frm.grid_columnconfigure(0, weight=1)
            self.frm.grid_rowconfigure(0, weight=1)
            self.frm.grid_rowconfigure(1, weight=1)
            self.frm.grid_rowconfigure(2, weight=1)
            
            lbl = tk.Label(self.frm, text='Contas')
            lbl.grid(row=0, column=0)
            
            frm = tk.Frame(self.frm)
            frm.grid(row=1, column=0)

            self.tvw_contas = ttk.Treeview(frm, columns=('id', 'titular', 'saldo', 'status', 'tipo'), height=20, show='headings')
            self.tvw_contas.grid()
            
            self.tvw_contas.heading('id', text='Id')
            self.tvw_contas.heading('titular', text='Titular')
            self.tvw_contas.heading('saldo', text='Saldo')
            self.tvw_contas.heading('status', text='Status')
            self.tvw_contas.heading('tipo', text='Tipo')
            
            self.tvw_contas.column('id', width=100)
            self.tvw_contas.column('titular', width=250)
            self.tvw_contas.column('saldo', width=150)
            self.tvw_contas.column('status', width=150)
            self.tvw_contas.column('tipo', width=150)
            
            self._scb_contas = tk.Scrollbar(frm, orient=tk.VERTICAL, command=self.tvw_contas.yview)
            self._scb_contas.grid(row=0, column=1, sticky='ns')
            self.tvw_contas.config(yscrollcommand=self._scb_contas.set)
            
            for conta in self.banco_em_uso.contas:
                self.tvw_contas.insert('', 'end', values=[conta.id, conta.titular.nome, f'R$ {conta.saldo:.2f}', 'Aberta' if conta.status else 'Encerrada', 'C/C' if isinstance(conta, ContaCorrente) else 'C/P'])

            frm_botoes_contas = tk.LabelFrame(self.frm, text='Opções')
            frm_botoes_contas.grid(row=2, column=0)
            
            def rendimento():
                cps = [conta for conta in self.banco_em_uso.contas if isinstance(conta, ContaPoupanca)]
                if cps == []:
                    messagebox.showerror('Erro', 'Não há bancos cadastrados!')
                else:
                    self.banco_em_uso.rendimento_cp()
                    self.janela_contas()
                    messagebox.showinfo('Aviso', 'Rendimento aplicado em todas as contas poupanças!')
            
            btn_abrir_conta = tk.Button(frm_botoes_contas, text='Abrir', command=self.abrir_conta)
            btn_abrir_conta.grid(row=0, column=0, padx=5, pady=5)
            btn_encerrar_conta = tk.Button(frm_botoes_contas, text='Encerrar', command=self.encerrar_conta)
            btn_encerrar_conta.grid(row=0, column=1, padx=5, pady=5)
            btn_operacoes_conta = tk.Button(frm_botoes_contas, text='Alterar saldo', command=self.operacoes)
            btn_operacoes_conta.grid(row=1, column=0, padx=5, pady=5)
            btn_extrato_conta = tk.Button(frm_botoes_contas, text='Extrato', command=self.extrato)
            btn_extrato_conta.grid(row=1, column=1, padx=5, pady=5)
            btn_extrato_conta = tk.Button(frm_botoes_contas, text='Aplicar Rendimentos', command=rendimento)
            btn_extrato_conta.grid(row=2, column=0, padx=5, pady=5, columnspan=2)
            
            self.config_text(self.frm)
    
    def abrir_conta(self):
        try:
            selecao = self.tvw_contas.selection()
        except:
            if Banco._bancos == []:
                messagebox.showerror('Erro', 'Não há bancos cadastrados!')
                return self.janela_bancos()
            selecao = []

        self.janela_contas()

        if len(selecao) == 1:
            conta_selecionada = self.tvw_contas.item(selecao, 'values')
            conta = [c for c in self.banco_em_uso.contas if c.id == conta_selecionada[0]][0]
            if not conta.status:
                messagebox.showinfo('Aviso', f'A conta nº {conta.id} foi reaberta!')
                conta.status = True
                self.janela_contas()
            else:
                messagebox.showinfo('Aviso', f'A conta nº {conta.id} já está aberta!')
        elif len(selecao) > 1:
            messagebox.showinfo('Aviso', 'Selecione apenas uma conta para reabrir')
        else:
            lista_clientes = [f'{cliente.id} - {cliente.nome}' for cliente in self.banco_em_uso.clientes]
            if lista_clientes == []:
                messagebox.showinfo('Aviso', f'Não é possível abrir uma conta pois o Banco {self.banco_em_uso.nome} ainda não possui clientes cadastrados.')
            else:
                self.top_abrir_conta = tk.Toplevel()
                self.top_abrir_conta.title('Abrir Conta')
                self.top_abrir_conta.grab_set()
                self.top_abrir_conta.geometry('500x400')
                
                self.top_abrir_conta.grid_columnconfigure(0, weight=1)
                self.top_abrir_conta.grid_rowconfigure(0, weight=1)
                self.top_abrir_conta.grid_rowconfigure(1, weight=1)
                
                lbl_frm1 = tk.LabelFrame(self.top_abrir_conta, text='Selecione um cliente para titular da conta')
                lbl_frm1.grid(row=0, column=0)
                
                lbl_frm1.grid_columnconfigure(0, weight=1)
                lbl_frm1.grid_rowconfigure(0, weight=1)
                lbl_frm1.grid_rowconfigure(1, weight=1)
                
                self.cbx_titular_conta = ttk.Combobox(lbl_frm1, values=lista_clientes)
                self.cbx_titular_conta.grid(row=0, column=0, padx=5, pady=5)
                
                lbl_frm2 = tk.LabelFrame(lbl_frm1, text='Tipo de conta')
                lbl_frm2.grid(row=1, column=0, padx=5, pady=5)
                self.tipo_conta = tk.StringVar()
                self.tipo_conta.set(0)
                self.tipo_conta_corrente = tk.Radiobutton(lbl_frm2, variable=self.tipo_conta, text='Corrente', value='cc')
                self.tipo_conta_corrente.grid()
                self.tipo_conta_poupanca = tk.Radiobutton(lbl_frm2, variable=self.tipo_conta, text='Poupança', value='cp')
                self.tipo_conta_poupanca.grid()
                
                btn_abrir_conta = Button(self.top_abrir_conta, text='Abrir Conta', command=self.confirmar_abrir_conta)
                btn_abrir_conta.grid()
                
                self.config_text(lbl_frm1)
                self.config_text(self.top_abrir_conta)

    def confirmar_abrir_conta(self):
        cliente = self.cbx_titular_conta.get()
        tipo_conta = self.tipo_conta.get()
        if cliente == '' or tipo_conta == '0':
            messagebox.showinfo('Aviso', 'Por favor, todos os campos são obrigatórios.', parent=self.top_abrir_conta)
        else:
            titular = [cli for cli in self.banco_em_uso.clientes if cliente.split(' - ')[0] == cli.id][0]
            if tipo_conta == 'cc':
                conta = ContaCorrente(titular)
            else:
                conta = ContaPoupanca(titular)
            self.banco_em_uso.adicionar_conta(conta)
            self.top_abrir_conta.destroy()
            self.janela_contas()

    def encerrar_conta(self):
        selecao = [self.tvw_contas.item(conta, 'values') for conta in self.tvw_contas.selection()]
        if len(selecao) == 0:
            messagebox.showinfo('Aviso', 'Selecione uma conta para encerrar!')
        elif len(selecao) > 1:
            messagebox.showinfo('Aviso', 'Selecione apenas uma conta para encerrar!')
        else:
            conta = [conta for conta in self.banco_em_uso.contas if selecao[0][0] == str(conta.id)][0]
            if not conta.saldo:
                if messagebox.askyesno('Confirmação', f'Confirmar o encerramento da conta nº {conta.id}?'):
                    conta.status = False
            else:
                messagebox.showinfo('Aviso', f'Não é possível encerrar a conta {conta.id} pois ainda possui saldo.')
        self.janela_contas()

    def operacoes(self):
        self.contas_selecionadas = [(self.tvw_contas.item(conta, 'values'), conta) for conta in self.tvw_contas.selection()]
        if self.contas_selecionadas == []:
            messagebox.showinfo('Aviso', f'Selecione uma conta para alterar seu saldo!')
        elif len(self.contas_selecionadas) > 1:
            messagebox.showinfo('Aviso', f'Selecione apenas uma conta!')
        else:
            self.conta_selecionada = [c for c in self.banco_em_uso.contas if c.id == self.contas_selecionadas[0][0][0]][0]
            if self.conta_selecionada.status:
                self.top_operacoes = tk.Toplevel()
                self.top_operacoes.title('Operações')
                self.top_operacoes.grab_set()
                self.top_operacoes.geometry('500x400')
                
                self.top_operacoes.grid_columnconfigure(0, weight=1)
                self.top_operacoes.grid_rowconfigure(0, weight=1)
                self.top_operacoes.grid_rowconfigure(1, weight=1)
                self.top_operacoes.grid_rowconfigure(2, weight=1)
                
                lbl_saldo = tk.Label(self.top_operacoes, text=f'Saldo da conta: R$ {self.contas_selecionadas[0][0][2]}')
                lbl_saldo.grid(row=0, column=0)
                
                lbl_frm = tk.LabelFrame(self.top_operacoes, text=f'Insira o valor')
                lbl_frm.grid(row=1, column=0)
                
                self.valor_operacao = tk.Entry(lbl_frm)
                self.valor_operacao.grid(row=0, column=0, padx=5, pady=5)
                
                frm = tk.Frame(self.top_operacoes)
                frm.grid(row=2, column=0)
                
                btn_operacao_depositar = tk.Button(frm, text='Depositar', command=self.operacao_depositar)
                btn_operacao_depositar.grid(row=0, column=0, padx=5, pady=5)
                
                btn_operacao_sacar = tk.Button(frm, text='Sacar', command=self.operacao_sacar)
                btn_operacao_sacar.grid(row=1, column=0, padx=5, pady=5)
                
                self.config_text(self.top_operacoes)
                self.config_text(frm)
                
            else:
                messagebox.showinfo('Aviso', 'Esta conta está desativada!')

    def operacao_depositar(self):
        conta = [c for c in self.banco_em_uso.contas if c.id == self.contas_selecionadas[0][0][0]][0]
        valor = float(self.valor_operacao.get())
        if valor == '':
            messagebox.showerror('Aviso', 'Digite o valor desejado', parent=self.top_operacoes)
        else:
            if isinstance(conta, ContaCorrente):
                valor -= valor * (self.banco_em_uso.taxa_cc / 100)
            if valor < 0:
                messagebox.showerror('Aviso', 'Valor inválido', parent=self.top_operacoes)
            elif messagebox.askokcancel('Confirmação', f'Confirma o depósito no valor de R$ {valor:.2f}?', parent=self.top_operacoes):
                conta.deposita(valor)
                self.janela_contas()
                self.top_operacoes.destroy()

    def operacao_sacar(self):
        conta = [c for c in self.banco_em_uso.contas if c.id == self.contas_selecionadas[0][0][0]][0]
        valor = float(self.valor_operacao.get())
        if valor == '':
            messagebox.showerror('Aviso', 'Digite o valor desejado', parent=self.top_operacoes)
        else:
            if isinstance(conta, ContaCorrente):
                valor += valor * (self.banco_em_uso.taxa_cc / 100)
            if valor < 0:
                messagebox.showinfo('Aviso', 'Valor inválido!', parent=self.top_operacoes)
            elif conta.saca(valor):
                if messagebox.askokcancel('Confirmação', f'Confirma o saque no valor de R$ {valor:.2f}?', parent=self.top_operacoes):
                    self.janela_contas()
                    self.top_operacoes.destroy()
            else:
                messagebox.showinfo('Aviso', 'Saldo insuficiente!', parent=self.top_operacoes)

    def extrato(self):
        self.contas_selecionadas = [(self.tvw_contas.item(conta, 'values'), conta) for conta in self.tvw_contas.selection()]
        if len(self.contas_selecionadas) == 0:
            messagebox.showinfo('Aviso', 'Selecione uma conta para emitir o relatório de transações!')
        elif len(self.contas_selecionadas) > 1:
            messagebox.showinfo('Aviso', 'Selecione apenas uma conta!')
        else:
            conta = [c for c in self.banco_em_uso.contas if c.id == self.contas_selecionadas[0][0][0]][0]
            destino = fd.asksaveasfile(filetypes=[('Texto', '*.txt')], initialfile=f'{conta.id}', defaultextension='.txt')
            for transacao in conta.historico:
                destino.write(f'{transacao}\n')
            destino.write(f'\n\nSaldo Total da Conta: R$ {conta.saldo:.2f}')

# Configurações da tela
    def config_text(self, componente):
        componente.config(bg='white')
        self.janela.config(background='#4D8EBB')
        for child in componente.winfo_children():
            try:
                child.config(font=('Constantia', 12), bg=child.master.cget('bg'))
                if isinstance(child, tk.Button):
                    child.config(bg='#1F485E', fg='white', width=20)
                if child.winfo_children():
                    self.config_text(child)
            except:
                pass

    def menu(self):

        menu = tk.Menu(self.janela)

        menu_bancos = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Bancos', menu=menu_bancos)
        menu_bancos.add_command(label='Listar Bancos', command=self.janela_bancos)
        menu_bancos.add_command(label='Cadastrar Novo Banco', command=self.cadastrar_banco)
        
        menu_clientes = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Clientes', menu=menu_clientes)
        menu_clientes.add_command(label='Listar Clientes', command=self.janela_clientes)
        menu_clientes.add_command(label='Cadastrar Cliente', command=self.cadastrar_cliente)

        menu_contas = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='Contas', menu=menu_contas)
        menu_contas.add_command(label='Listar Contas', command=self.janela_contas)
        menu_contas.add_command(label='Abrir Conta', command=self.abrir_conta)

        self.janela.config(menu=menu)

    def limpar_tela(self, tela):
        self.janela.state('zoomed')
        try:
            for i in range(tela.grid_size()[1]):
                tela.grid_rowconfigure(i, weight=0)
        except: pass
        try:
            for child in self.frm.winfo_children():
                child.destroy()
        except:
            pass

app = tk.Tk()
janelaPrincipal = Tela(app)
app.mainloop()