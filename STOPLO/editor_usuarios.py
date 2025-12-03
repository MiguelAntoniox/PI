import tkinter as tk
from tkinter import ttk, messagebox
import os
from bancoPI import BancoPI
import pandas as pd

"""tela para editar usuarios"""
class EditorUsuarios:
    def __init__(self, master=None, usuario=None):
        self.master = master
        self.banco = BancoPI()
        self.janela = tk.Tk(master)
        self.janela.title("Editor de usuarios")
        self.janela.geometry("1427x800")
        self.janela.configure(bg="white")
        self.icone()
        
     
      
        """criando label e treeview para mostrar os usuarios cadastrados"""
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        titulo = tk.Label(self.janela, text="Usuários Cadastrados", font=("Roboto",16,"bold"), bg="white")
        titulo.pack(pady=10)

        self.frame_conteudo = tk.Frame(self.janela, bg="white", relief="sunken", bd=2)
        self.frame_conteudo.pack(expand=True, fill="both", padx=20, pady=20)

        self.treeview = ttk.Treeview(self.frame_conteudo, columns=("Usuário", "Perfil"), show="headings")
        self.treeview.heading("Usuário", text="Usuário")
        self.treeview.heading("Perfil", text="Perfil")
        self.treeview.column("Usuário", width=200)
        self.treeview.column("Perfil", width=100)
        self.treeview.pack(expand=True, fill="both", padx=10, pady=10)
        
        """chamando o metodo para carregar os usuarios"""
        self.carregar_usuarios()

        """criando botoes para excluir ,atualizar e gerar excel de usuarios"""
        btn_excluir = tk.Button(self.janela, text="Excluir", command=self.excluir_usuario, bg= "black", fg="white" ,font=("bold", 12))
        btn_excluir.pack(side="left", padx=10, pady=10)

        self.btn_atualizar = tk.Button(self.janela, text="Atualizar", command=self.abrir_edicao, state="disabled", bg= "black", fg="white" ,font=("bold", 12))
        self.btn_atualizar.pack(side="left", padx=10, pady=10)
        
        self. btn_excel = tk.Button(self.janela, text="Gerar Excel", command=self.gerarexcel, bg= "black", fg="white" ,font=("bold", 12))
        self.btn_excel.pack(side="left", padx=10, pady=10)

        self.usuario_selecionado = None

        """defininido eventos do treeview 1 clique seleciona e 2 abre a atualizaçao do usuario"""
        self.treeview.bind("<ButtonRelease-1>", self.on_treeview_select) 
        self.treeview.bind("<Double-1>", self.on_double_click)
    
    
    """método para adicionar o ícone à janela"""    
    def icone(self):
        
        caminho = os.path.join(os.path.dirname(__file__), "money.ico")
        if os.path.exists(caminho):
            self.janela.iconbitmap(caminho) 
    
    """metodo para gerar o excel dos usuarios cadastrados usadno pandas"""
    def gerarexcel(self):
        try:
        
            dados = []
            for usuario in self.treeview.get_children():
                valores = self.treeview.item(usuario)["values"]
                dados.append({
                    "Usuário": valores[0],
                    "Perfil": valores[1],
                    "Grupos": valores[2]
                })
                
            if not dados:
                messagebox.showwarning("Aviso", "vazio os usuario cadastrado.")
                return    
                
            df = pd.DataFrame(dados)

            caminho_arquivo = os.path.join(os.path.expanduser("~"), "Desktop", "usuarios_cadastrados.xlsx")
            df.to_excel(caminho_arquivo, index=False)

            messagebox.showinfo("Sucesso", f"Arquivo Excel gerado com sucesso na área de trabalho:\n{caminho_arquivo}") 
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar o arquivo Excel: {e}")      

    
    """esses dois metodos sao para selecionar o usuario no treeview e abrir a janela de ediçao com 2 cliques junto com a linha 51"""
    def on_treeview_select(self, event):
        selecionado = self.treeview.selection()  
        if selecionado:
            item_selecionado = selecionado[0]
            self.usuario_selecionado = self.treeview.item(item_selecionado)["values"]
            self.btn_atualizar.config(state="normal")  
        else:
            self.usuario_selecionado = None
            self.btn_atualizar.config(state="disabled")  

    def on_double_click(self, event):
        selecionado = self.treeview.selection()
        if selecionado:
            item_selecionado = selecionado[0]
            self.usuario_selecionado = self.treeview.item(item_selecionado)["values"]
            self.abrir_edicao()
    """metodo para carregar os usuarios cadastrados no treeview que foi criado na linha 29"""
    def carregar_usuarios(self):
        try:
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            usuarios = self.banco.obter_usuarios_com_grupos_inner_join()

            for usuario in usuarios:
                nome = usuario[0]
                perfil = usuario[1]
                grupo = usuario[2]
                 
                self.treeview.insert("", "end", values=(nome, perfil, grupo))  

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar os usuários: {e}")

    """metodo para excluir o usuario selecionado no treeview"""
    def excluir_usuario(self):
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir.")
            return

        item_selecionado = selecionado[0]
        usuario = self.treeview.item(item_selecionado)["values"][0]

      

        query = "SELECT id FROM usuarios WHERE usuario = %s"
        self.banco.cursor.execute(query, (usuario,))
        usuario_id = self.banco.cursor.fetchone()

        if not usuario_id:
            messagebox.showerror("Erro", "Usuário não encontrado no banco de dados.")
            return

        resposta = messagebox.askyesno("Exclusão", f"Tem certeza que deseja excluir o usuário '{usuario}'?")
        if resposta:
            try:
                query_del_rel = "DELETE FROM usuario_grupo WHERE usuario_id = %s"
                self.banco.cursor.execute(query_del_rel, (usuario_id[0],))

                query_delete = "DELETE FROM usuarios WHERE id = %s"
                self.banco.cursor.execute(query_delete, (usuario_id[0],))
                self.banco.conexao.commit()

                self.treeview.delete(item_selecionado)
                messagebox.showinfo("Sucesso", f"Usuário '{usuario}' excluído com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir o usuário: {e}")
            finally:
                self.carregar_usuarios()
    """funcao cria a tela de ediçao do usuario selecionado no treeview"""
    def abrir_edicao(self):
        if not self.usuario_selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar.")
            return

        usuario = self.usuario_selecionado[0]

        edicao = tk.Toplevel(self.janela)
        edicao.title("Editar Usuário")
        edicao.geometry("800x600")
        edicao.configure(bg="white")

        caminho_icone = os.path.join(os.path.dirname(__file__), "money.ico")
        if os.path.exists(caminho_icone):
            edicao.iconbitmap(caminho_icone)

        tk.Label(edicao, text="Usuário:", bg="white").pack(pady=(15, 5))
        entrada_usuario = tk.Entry(edicao, highlightthickness=1, highlightbackground="black")
        entrada_usuario.pack(padx=20)
        entrada_usuario.insert(0, usuario)

        tk.Label(edicao, text="Nova Senha:", bg="white").pack(pady=(10, 5))
        entrada_senha = tk.Entry(edicao, show="*", highlightthickness=1, highlightbackground="black")
        entrada_senha.pack(padx=20)

        query_perfil = "SELECT perfil FROM usuarios WHERE usuario = %s"
        self.banco.cursor.execute(query_perfil, (usuario,))
        perfil_atual = self.banco.cursor.fetchone()
        perfil_atual = perfil_atual[0] if perfil_atual else "usuário"

        perfis = ["usuário", "admin"]
        perfil_var = tk.StringVar(edicao)
        perfil_var.set(perfil_atual)

        tk.Label(edicao, text="Perfil:", bg="white").pack(pady=(10, 5))
        tk.OptionMenu(edicao, perfil_var, *perfis).pack(padx=20)

        """metodo para salvar a atualizaçao do usuario"""
        def salvar_edicao():
            novo_usuario = entrada_usuario.get().strip()
            nova_senha = entrada_senha.get().strip()
            perfil_novo = perfil_var.get()

            if not novo_usuario:
                messagebox.showerror("Erro", "Usuário não pode ficar vazio!")
                return

            try:

                self.banco.atualizar_usuario(usuario, novo_usuario, nova_senha if nova_senha else None, perfil_novo,)

                messagebox.showinfo("Sucesso", f"Usuário '{novo_usuario}' atualizado com sucesso!")
                edicao.destroy()
                self.carregar_usuarios()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar os dados do usuário: {e}")

        tk.Button(edicao, text="Salvar", command=salvar_edicao, bg="black", fg="white").pack(pady=20)
        
    """metodo para abrir a tela de cadastro de novo usuario pela tela de ediçao"""    
    def abrir_cadastro(self):
        cadastro = tk.Toplevel(self.janela)
        cadastro.title("Cadastrar Usuário")
        cadastro.geometry("800x600")
        cadastro.configure(bg="white")
        cadastro.resizable(False, False)

        caminho_icone = os.path.join(os.path.dirname(__file__), "../logo.ico")
        if os.path.exists(caminho_icone):
            cadastro.iconbitmap(caminho_icone)

        tk.Label(cadastro, text="Novo Usuário:", bg="white").pack(pady=(15, 5))
        entrada_novo_usuario = tk.Entry(cadastro, highlightthickness=1, highlightbackground="green")
        entrada_novo_usuario.pack(padx=20)

        tk.Label(cadastro, text="Nova Senha:", bg="white").pack(pady=(10, 5))
        entrada_nova_senha = tk.Entry(cadastro, show="*", highlightthickness=1, highlightbackground="green")
        entrada_nova_senha.pack(padx=20)

        perfis = ["usuário", "moderador", "admin"]
        perfil_var = tk.StringVar(cadastro)
        perfil_var.set("usuário")

        tk.Label(cadastro, text="Perfil:", bg="white").pack(pady=(10, 5))
        tk.OptionMenu(cadastro, perfil_var, *perfis).pack(padx=20)

        tk.Label(cadastro, text="Grupos:", bg="white").pack(pady=(10, 5))

        grupos_disponiveis = []
        try:
            self.banco.cursor.execute("SELECT nome FROM permissoes")
            grupos_disponiveis = [row[0] for row in self.banco.cursor.fetchall()]
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar grupos: {e}")

        listbox_grupos = tk.Listbox(cadastro, selectmode=tk.MULTIPLE, height=6)
        for grupo in grupos_disponiveis:
            listbox_grupos.insert(tk.END, grupo)
        listbox_grupos.pack(padx=20, pady=(0, 10), fill="x")

        """metodo para salvar o novo usuario - validaçoes inclusas e salvando no banco apos validacoes"""
        def salvar_usuario():
            novo_usuario = entrada_novo_usuario.get().strip()
            nova_senha = entrada_nova_senha.get().strip()
            self.perfil = perfil_var.get()

            indices_selecionados = listbox_grupos.curselection()
            grupos_selecionados = [listbox_grupos.get(i) for i in indices_selecionados]

           
            if not novo_usuario or not nova_senha or not self.perfil or len(grupos_selecionados) == 0:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios e pelo menos um grupo deve ser selecionado!")
                return

            def validar_usuario(usuario):
                if '@' not in usuario or not usuario.endswith('.com.br'):
                    return False, "Usuário deve conter '@' e terminar com '.com.br'."
                return True, ""

            def validar_senha(senha):
                if len(senha) < 8:
                    return False, "A senha deve ter no mínimo 8 caracteres."
                if not any(c.isupper() for c in senha):
                    return False, "A senha deve conter pelo menos uma letra maiúscula."
                if not any(c.isdigit() for c in senha):
                    return False, "A senha deve conter pelo menos um número."
                caracteres_especiais = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
                if not any(c in caracteres_especiais for c in senha):
                    return False, "A senha deve conter pelo menos um caractere especial."
                return True, ""

            valido, mensagem = validar_usuario(novo_usuario)
            if not valido:
                messagebox.showerror("Erro", mensagem)
                return

            valido, mensagem = validar_senha(nova_senha)
            if not valido:
                messagebox.showerror("Erro", mensagem)
                return

            try:
                self.banco.salvar_usuario(novo_usuario, nova_senha, self.perfil)

                self.banco.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (novo_usuario,))
                usuario_id = self.banco.cursor.fetchone()[0]

                for grupo_nome in grupos_selecionados:
                    self.banco.cursor.execute("SELECT id FROM permissoes WHERE nome = %s", (grupo_nome,))
                    grupo_id = self.banco.cursor.fetchone()[0]
                    self.banco.cursor.execute(
                        "INSERT INTO usuario_grupo (usuario_id, grupo_id) VALUES (%s, %s)",
                        (usuario_id, grupo_id)
                    )

                self.banco.conexao.commit()

                messagebox.showinfo("Sucesso", f"Usuário '{novo_usuario}' cadastrado com sucesso!")
                cadastro.destroy()
                self.carregar_usuarios()

            except ValueError as e:
                messagebox.showerror("Erro", str(e))
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

        tk.Button(cadastro, text="Salvar", command=salvar_usuario, bg="black", fg="white").pack(pady=20)
        
    def fechar_janela(self):
        self.janela.destroy()

    def iniciar(self):
        self.janela.mainloop()