import requests    # habilitando uso do requests
from tkinter import *
import tkinter as tk


class Stocks:
    """atributos da classe moedas"""
    
    def __init__(self):
       
        self.janelaacoes = tk.Toplevel()
        self.janelaacoes.title("Stocks STOP.LO")
        self.janelaacoes.geometry("1428x800")
        self.janelaacoes.configure(bg = "white")
        self.criar_botoes_label()
        
        
        
    def criar_botoes_label(self):
       
       
        tk.Label(self.janelaacoes, text= "PAINEL DE DECISÂO DO INVESTIDOR" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=1, padx=11, pady=5)
        frame =  tk.Frame(self.janelaacoes, height=2, width=1400, bg="black")
        frame.grid(row=1, column=0, columnspan=3, pady=10)
        tk.Label(frame, text= f"Cotaçao TESLA hoje: {self.cotacao_ativos()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(frame, text= f"Cotaçao IBM hoje: {self.cotacao_ativos()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(frame, text= f"Cotaçao GOOGLE hoje: {self.cotacao_ativos()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=2, padx=11, pady=5)
        
        botao_agendar = tk.Button(self.janelaacoes, text= "Agendar",command=self.agendar, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_agendar.grid(row=2, column=0, pady=20)
        
        
    def agendar(self):
        self.janelaacoes.destroy()
        self.janelagendamento = tk.Toplevel()
        self.janelagendamento.title("Agendamento STOP.LO")
        self.janelagendamento.geometry("400x300")
        self.janelagendamento.configure(bg = "white")
        
        
           
        

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
        
        
        
              
        

    
        
            

                                 


