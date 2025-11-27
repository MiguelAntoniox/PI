import requests    # habilitando uso do requests
from tkinter import *
import tkinter as tk
import os
from PIL import Image, ImageTk

class Stocks:
    """atributos da classe moedas"""
    
    def __init__(self):
       
        self.janelaacoes = tk.Toplevel()
        self.janelaacoes.title("Stocks STOP.LO")
        self.janelaacoes.geometry("1428x800")
        self.janelaacoes.configure(bg = "white")
        self.criar_botoes_label()
        
        
        
    def criar_botoes_label(self):
       
       
        tk.Label(self.janelaacoes, text= "Stocks" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=0, padx=11, pady=5)
        self.frame =  tk.Frame(self.janelaacoes, height=2, width=1400, bg="black")
        self.frame.grid(row=1, column=0, columnspan=3, pady=10)
        tk.Label(self.frame, text= f"TESLA: {self.cotacao_ativos()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(self.frame, text= f"IBM: {self.cotacao_ativos()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(self.frame, text= f"GOOGLE: {self.cotacao_ativos()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=2, padx=11, pady=5)
        
        botao_agendar = tk.Button(self.janelaacoes, text= "Configurar ordem ",command=self.agendar, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_agendar.grid(row=2, column=0, pady=20)
        
        
        
        caminho_imagem = os.path.join(os.path.dirname(__file__), "tesla.png")
        if os.path.exists(caminho_imagem):
            imagem_pil = Image.open(caminho_imagem).resize((200,200), Image.Resampling.LANCZOS) 
            self.imagem_tesla = ImageTk.PhotoImage(imagem_pil)
            label_imagem_tesla = tk.Label(self.frame, image= self.imagem_tesla, bg= "white")
            label_imagem_tesla.grid(row=3, column=0, pady=10)
            
        caminho_imagem = os.path.join(os.path.dirname(__file__), "ibm.png")
        if os.path.exists(caminho_imagem):
            imagem_pil = Image.open(caminho_imagem).resize((200,200), Image.Resampling.LANCZOS) 
            self.imagem_ibm = ImageTk.PhotoImage(imagem_pil)
            label_imagem_ibm = tk.Label(self.frame, image= self.imagem_ibm, bg= "white")
            label_imagem_ibm.grid(row=3, column=1, pady=10)
            
        caminho_imagem = os.path.join(os.path.dirname(__file__), "google.png")
        if os.path.exists(caminho_imagem):
            imagem_pil = Image.open(caminho_imagem).resize((200,200), Image.Resampling.LANCZOS) 
            self.imagem_google = ImageTk.PhotoImage(imagem_pil)
            label_imagem_google = tk.Label(self.frame, image= self.imagem_google, bg= "white")
            label_imagem_google.grid(row=3, column=2, pady=10)        
        
        
    def agendar(self):
        self.janelaacoes.destroy()
        self.janelagendamento = tk.Toplevel()
        self.janelagendamento.title("Agendamento STOP.LO")
        self.janelagendamento.geometry("1428x800")
        self.janelagendamento.configure(bg = "white")
       
        
        
    
        framao = tk.Frame(self.janelagendamento, bg= "white")
        framao.pack(pady=30)
        
        tk.Label(framao, text= "Qual ação deseja comprar ?", bg = "white", font= ("Roboto",16,"bold"),padx=50 ).pack(pady=(20, 10))
        self.campo_acao= tk.Entry(framao,width=30, highlightthickness= 15,highlightbackground= "white")
        self.campo_acao.pack(padx=50)
        
        
        tk.Label(framao, text= "Quantas açoes deseja comprar ?", bg= "white", font= ("Roboto",16,"bold"),padx=50).pack(pady=(30, 10))
        self.campo_quantidade= tk.Entry(framao, width=30,highlightthickness= 15,highlightbackground= "white")
        self.campo_quantidade.pack(padx=50)
        
        tk.Label(framao, text= "Qual valor de compra da ação ?", bg= "white", font= ("Roboto",16,"bold"),padx=50).pack(pady=(30, 10))
        self.campo_valor= tk.Entry(framao, width=30,highlightthickness= 15,highlightbackground= "white")
        self.campo_valor.pack(padx=50)
        
        botao_salvar = tk.Button(framao, text= "Salvar ordem", command=self.enviarordem, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_salvar.grid(pady=30,column=3)
       
        
  
        
    def enviarordem(self):
        pass       
        

    def cotacao_ativos(self): # criando uma função
        """esse metodo esta recebendo os dados selecionados atraves de uma API e retornando o valor atual da moeda"""
        
        url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=A7M18SXMV2MEY9BO " # variavel url recebe o link da APi 

        try: # serve para caso o codigo aq dentro der erro, ele mostrar uma mensagem pra esse erro ao usuario usando o EXCEPT
            resposta = requests.get(url) # variavel resposta recebe o Valor do dolar usando o requests.get
            resposta.raise_for_status()   # verifica se a resposta possui algum erro de recebimento usando o .raise_for_status()
            dados = resposta.json() # armazena na variavel dados a resposta convertida pelo .json() em um dicionario python
            cotacao = dados[""][""] # pega o valor de "bid" é um valor que vem dentro do arquivo solicitado na url 
            return float(cotacao) # retorna o valor da funcao usando numero flutuante
        
        except Exception as qualerro:   # except identifica um erro # Exception é a classe que nos diz qual erro ocorreu # as qual erro armazena esse erro dentro da variavel qual erro
            print("Ocorreu um erro na puxagem dos dados: " , qualerro)
            return None  
        
    
    def iniciar(self):
         self.janelaacoes.mainloop()
        
        
        
              
if __name__ == "__main__":
    app = Stocks()
    app.iniciar()            

    
        
            

                                 


