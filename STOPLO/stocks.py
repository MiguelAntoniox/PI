import requests    # habilitando uso do requests
from tkinter import *
import tkinter as tk
import os
from PIL import Image, ImageTk
from bancoPI import BancoPI


ticker_tesla = "TSLA"
ticker_ibm = "IBM"
ticker_google = "GOOGL"

class Stocks:
    """atributos da classe moedas"""
    
    def __init__(self):
       
        self.janelaacoes = tk.Toplevel()
        self.janelaacoes.title("Stocks STOP.LO")
        self.janelaacoes.geometry("1300x800")
        self.janelaacoes.configure(bg = "white")
        self.criar_botoes_label()
        
        
    def criar_botoes_label(self):
       
       
        def formatar_preco(preco):
            if isinstance(preco, float):

                return f"${preco:,.2f}" 
            return str(preco)
        
    
        preco_tesla = self.cotacao_ativos(ticker_tesla)
        preco_ibm = self.cotacao_ativos(ticker_ibm)
        preco_google = self.cotacao_ativos(ticker_google)

        tk.Label(self.janelaacoes, text= "Stocks" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=1, padx=11, pady=5)
        
       
        self.frame = tk.Frame(self.janelaacoes, bg="white")
        self.frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        
        tk.Label(self.frame, text= f"{ticker_google}: {formatar_preco(preco_tesla)} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(self.frame, text= f"{ticker_ibm}: {formatar_preco(preco_ibm)} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(self.frame, text= f"{ticker_google}: {formatar_preco(preco_google)} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=2, padx=11, pady=5)
        
        botao_agendar = tk.Button(self.janelaacoes, text= "Configurar ordem ",command=self.agendar, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_agendar.grid(row=2, column=0, columnspan=3, pady=20) 
        
    
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
        self.janelagendamento.geometry("1427x800")
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
        botao_salvar.pack(pady=30)
       
  
        
    def enviarordem(self):
        acao = self.campo_acao.get()
        quantidade = self.campo_quantidade.get()
        valor = self.campo_valor.get()
        
        print(f"Ordem de Compra Salva:\n Ação: {acao}\n Quantidade: {quantidade}\n Valor: {valor}")      
        

    def cotacao_ativos(self, ticker):
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey=A7M18SXMV2MEY9BO"
        try:
            resposta = requests.get(url, timeout=150)
            resposta.raise_for_status()
            data = resposta.json()
          
            if "Note" in data or "Information" in data:
                print(f"AlphaVantage limite/nota: {data}")
                return "Sem dados (limite)"
            if "Global Quote" not in data or not data["Global Quote"]:
                print(f"Sem 'Global Quote' para {ticker}: {data}")
                return "Sem dados"
            quote = data["Global Quote"]
            preco_str = quote.get("05. price")
            if not preco_str:
                print(f"Sem '05. price' para {ticker}: {quote}")
                return "Sem dados"
            try:
                preco = float(preco_str)
                return f"${preco:,.2f}"
            except ValueError:
                return preco_str
        except requests.RequestException as e:
            print(f"Erro ao buscar {ticker}: {e}")
            return "Erro"
    
        except ValueError:
            # Erro de conversão para float (se o valor retornado não for um numero)
            print(f"Erro ao converter cotação para float para {ticker}.")
            return "Erro Valor"
        except Exception as qualerro:
        
            print(f"Ocorreu um erro geral para {ticker}: {qualerro}")
            return "Erro Geral"  
        
    
    def iniciar(self):
         self.janelaacoes.mainloop()
        
        
        
              
if __name__ == "__main__":
    app = Stocks()
    app.iniciar()            

    
        
            

                                 


