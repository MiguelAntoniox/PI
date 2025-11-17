import os 
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from menu import Menu

""""classe que constroi a janela"""

class Login:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Login STOP.LO")
        self.janela.geometry("500x800")
        self.janela.configure(bg = "white")
        self.tentativas = 0
        
        """" pra por o gif na tela"""
        
        caminho_imagem = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(caminho_imagem):
            imagem_pil = Image.open(caminho_imagem).resize((200,200), Image.Resampling.LANCZOS) 
            self.imagem = ImageTk.PhotoImage(imagem_pil)
            label_imagem = tk.Label(self.janela, image= self.imagem, bg= "gray")
            label_imagem.pack(pady=(20,10))
            
        """"criando os labeis escritos, campos de entrada e botoes"""  
        
    
        
        framao = tk.Frame(self.janela, bg= "white")
        framao.pack(pady=10)
          
        tk.Label(self.janela, text= "Usuario ", bg= "white", font= ("Roboto",16,"bold"), padx=50).pack(pady=(20, 10))
        self.campo_usuario= tk.Entry(self.janela,width=65, highlightthickness= 15,highlightbackground= "white")
        self.campo_usuario.pack(padx=50)
        
        
        tk.Label(self.janela, text= "Senha ", bg= "white", font= ("Roboto",16,"bold"),padx=50).pack(pady=(20, 10))
        self.campo_senha= tk.Entry(self.janela, width=65,highlightthickness= 15,highlightbackground= "white", show="$")
        self.campo_senha.pack(padx=50)
        
        botao_entrar = tk.Button(self.janela, text= "Entrar", command=self.validar_login, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_entrar.pack(pady=30)
        
        botao_cadastrar = tk.Button(self.janela, text= "Cadastrar", command=self.validar_login, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_cadastrar.pack(pady=30)
        
        
     
     
    def icone(self):
        
        caminho = os.path.join(os.path.dirname(__file__), "ico.ico")
        if os.path.exists(caminho):
            self.janela.iconbitmap(caminho) 
        
    def validar_login(self):
        usuario = self.campo_usuario.get().strip()
        senha =  self.campo_senha.get().strip()
        
        
        if not usuario and not senha:
            self.tentativas += 1
            if self.tentativas >= 3:
                messagebox.showerror("dados tentados invalidos", "Tente dados validos")
                self.tentativas = 0
            else:
                messagebox.showerror("Erro", "Prencha os campos")
                
            return
        elif not usuario:
            self.tentativas += 1
            if self.tentativas >= 3:
                messagebox.showerror("Usuario errado")
                self.tentativas = 0
            else:
                messagebox.showerror("prencha o campo")
            return
        
        elif not senha:
            self.tentativas += 1
            if self.tentativas >= 3:
                messagebox.showerror("senha errada ")
                self.tentativas = 0
            else:
                messagebox.showerror("prencha o campo") 
            return
        if usuario == "admin" and senha == "123":
            
            
            
           self.janela.withdraw()
           app = Menu()
           app.iniciar() 
           
            
        else:
            self.tentativas += 1
            if self.tentativas >=3:
                messagebox.showerror("errou as tentativas")  
                self.tentativas = 0
            else:
                messagebox.showerror("Erro", "Usuario ou senha invalidos")
                      
                                    
            
            
            
    def iniciar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = Login()
    app.iniciar()        