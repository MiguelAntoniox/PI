import os 
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from menu import Menu_Principal 
from bancoPI import BancoPI
from tkinter import *
from PIL import Image, ImageTk


""""classe que constroi a janela"""

class Login:
    def __init__(self):
        self.janela = tk.Tk()  
        self.janela.title("Login STOP.LO")
        self.janela.geometry("1427x800")
        self.janela.configure(bg = "white")
        self.tentativas = 0
        self.bancoPI = BancoPI()
        self.icone()
        
        
        """" pra por o gif na tela"""
        
        caminho_imagem = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(caminho_imagem):
            imagem_pil = Image.open(caminho_imagem).resize((200,200), Image.Resampling.LANCZOS) 
            self.imagem = ImageTk.PhotoImage(imagem_pil)
            label_imagem = tk.Label(self.janela, image= self.imagem, bg= "white")
            label_imagem.pack(pady=(20,10))
            
          
        framao = tk.Frame(self.janela, bg= "white")
        framao.pack(pady=10)
          
        tk.Label(self.janela, text= "Usuario ", bg = "white", font= ("Roboto",16,"bold"),padx=50 ).pack(pady=(20, 10))
        self.campo_usuario= tk.Entry(self.janela,width=65, highlightthickness= 15,highlightbackground= "white")
        self.campo_usuario.pack(padx=50)
        
        
        tk.Label(self.janela, text= "Senha ", bg= "white", font= ("Roboto",16,"bold"),padx=50).pack(pady=(20, 10))
        self.campo_senha= tk.Entry(self.janela, width=65,highlightthickness= 15,highlightbackground= "white", show="$")
        self.campo_senha.pack(padx=50)
        
        botao_entrar = tk.Button(self.janela, text= "Entrar", command=self.validarlogin, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_entrar.pack(pady=30)
        
        botao_cadastrar = tk.Button(self.janela, text= "Cadastrar", command=self.tela_cadastro, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_cadastrar.pack(pady=30)
        
        
      
    def icone(self):
        
        caminho = os.path.join(os.path.dirname(__file__), "money.ico")
        if os.path.exists(caminho):
            self.janela.iconbitmap(caminho) 
        
    def validarlogin(self):
        
        usuario = self.campo_usuario.get().strip()
        senha = self.campo_senha.get().strip()
        
        
        if not usuario and not senha:
            self.erro_login("preencha todos os campos")
            return
        elif not usuario:
            self.erro_login("preencha o usuario")
            return
        elif not senha: 
            self.erro_login("preencha a senha")
            return
        
        if self.bancoPI.validar_credenciais(usuario, senha):
            
            
            usuario_id = self.bancoPI.obter_id_usuario(usuario) 
            
            if usuario_id is not None:
                self.bancoPI.registrar_login(usuario)
                self.janela.withdraw()
                
                
                menu = Menu_Principal(usuario_id=usuario_id) 
                menu.iniciar()
            else:
                messagebox.showerror("Erro", "Falha ao obter o ID do usuário após o login.", parent=self.janela)
            
        else:
            self.erro_login("Usuario ou senha errados")
            
            
    def erro_login(self, mensagem):
        self.tentativas += 1
        if self.tentativas >= 3:
            messagebox.showerror("Erro","a tentativa esta incorreta")
            self.tentativas= 0
        else:
            messagebox.showerror("Erro", mensagem)      
                    
    def tela_cadastro(self):
        
        cadastro = Toplevel(self.janela)
        cadastro.title("Cadastro de usuario")
        cadastro.geometry("500x800")
        cadastro.configure(bg = "white")
        
        caminho = os.path.join(os.path.dirname(__file__), "ico.ico")
        if os.path.exists(caminho):
            self.janela.iconbitmap(caminho)
            
        Label(cadastro, text= "Usuario ", bg= "white", font= ("Roboto",16,"bold"), padx=50).pack(pady=(20, 10))
        login_novousuario = Entry(cadastro,width=65, highlightthickness= 15,highlightbackground= "white")
        login_novousuario.pack(padx=20)
    
        Label(cadastro, text= "Senha:", bg= "white", font= ("Roboto",16,"bold"), padx=50).pack(pady=(20, 10))
        senha_novousuario = Entry(cadastro,width=65,highlightthickness= 15,highlightbackground= "white", show="$")
        senha_novousuario.pack(padx=20)
        
        def salvar_usuario():
            novousuario =  login_novousuario.get()
            novasenha = senha_novousuario.get()
            
            if not novousuario or not novasenha:
                messagebox.showerror("erro", "Preencha usuario ou senha", parent = cadastro)
                return
            
            def validarusuario(usuario):
                tem_arroba = "@" in usuario
                tem_br = usuario.endswith(".com.br")
                if not tem_arroba or not tem_br:
                    return False, "Usuario precisa ter @ e .com.br"   
                return True, ""
            
            def validarsenha(senha):
                if len(senha) < 8:
                    return False, "a senha tem que ter mais de 8 caracteres" 
                
                tem_maiuscula = False
                for caractere in senha:
                    if caractere.isupper():
                        tem_maiuscula = True
                        break
                if not tem_maiuscula:
                    return False, "A senha deve ter pelo menos uma letra maiúscula."
                
                tem_numero = False
                for caractere in senha:
                    if caractere.isdigit():
                        tem_numero = True
                        break
                if not tem_numero:
                    return False, "A senha deve ter pelo menos um número."
                
                caracteres_especiais = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"
                tem_especial = False
                for caractere in senha:
                    if caractere in caracteres_especiais:
                        tem_especial = True
                        break
                if not tem_especial:
                    return False, "A senha deve ter pelo menos um caractere especial."
                
                return True, ""

            valido, mensagem = validarusuario(novousuario)
            if not valido:
                messagebox.showerror("Erro", mensagem, parent=cadastro)
                return

            valido, mensagem = validarsenha(novasenha)
            if not valido:
                messagebox.showerror("Erro", mensagem, parent=cadastro)
                return
            
            try:
                self.bancoPI.salvar_usuario(novousuario, novasenha)
                messagebox.showinfo("Sucesso", f"Usuario '{novousuario}' cadastrado com sucesso!")
                cadastro.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", str(e), parent=cadastro)             
        
        botao = Button(cadastro, text="Salvar", command=salvar_usuario, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white" )
        botao.pack(padx=20)    
            
            
    def iniciar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = Login()
    app.iniciar()