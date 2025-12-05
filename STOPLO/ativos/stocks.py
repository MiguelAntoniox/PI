from tkinter import messagebox
import requests    # habilitando uso do requests
from tkinter import *
import tkinter as tk
import os
from PIL import Image, ImageTk
from STOPLO.bancodedados.bancoPI import BancoPI

"""definindo os tickers das ações"""
ticker_tesla = "TSLA"
ticker_ibm = "IBM"
ticker_google = "GOOGL"

class Stocks:
    """atributos da classe moedas"""
    
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.janelaacoes = tk.Toplevel()
        self.janelaacoes.title("Stocks STOP.LO")
        self.janelaacoes.geometry("1300x800")
        self.janelaacoes.configure(bg = "white")
        self.criar_botoes_label()
        self.icone()
        
    """método para criar os botões e labels na tela - também chama funções para mostrar no label"""    
    def criar_botoes_label(self):
       
       
        def formatar_preco(preco):
            if isinstance(preco, float):

                return f"${preco:,.2f}" 
            return str(preco)
        
    
        preco_tesla = self.cotacao_ativos(ticker_tesla)
        preco_ibm = self.cotacao_ativos(ticker_ibm)
        preco_google = self.cotacao_ativos(ticker_google)

        tk.Label(self.janelaacoes, text= "Stocks" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=2, padx=11, pady=5)
        
       
        self.frame = tk.Frame(self.janelaacoes, bg="white")
        self.frame.grid(row=1, column=1, columnspan=3, pady=10)
        
        
        tk.Label(self.frame, text= f"{ticker_tesla}: {formatar_preco(preco_tesla)} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(self.frame, text= f"{ticker_ibm}: {formatar_preco(preco_ibm)} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(self.frame, text= f"{ticker_google}: {formatar_preco(preco_google)} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=2, padx=11, pady=5)
        
        """chamando as imagens para aparecer na tela"""
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
        self.agendar()    
    """criando o método para adicionar o ícone à janela"""             
    def icone(self):
        
        caminho = os.path.join(os.path.dirname(__file__), "money.ico")
        if os.path.exists(caminho):
            self.janelaacoes.iconbitmap(caminho) 
                
    """método para criar a estrtura para agendar ordens de compra e venda"""    
    def agendar(self):
        
        tk.Label(self.frame, text= "Qual ação deseja comprar ?", bg = "white", font= ("Roboto",16,"bold"),padx=50 ).grid(row=4, column=1, padx=11, pady=5)
        self.campo_acao= tk.Entry(self.frame,width=30, highlightthickness= 15,highlightbackground= "white")
        self.campo_acao.grid(row=5, column=1, padx=11, pady=5)
        
        
        tk.Label(self.frame, text= "Quantas açoes deseja comprar ?", bg= "white", font= ("Roboto",16,"bold"),padx=50).grid(row=6, column=1, padx=11, pady=5)
        self.campo_quantidade= tk.Entry(self.frame, width=30,highlightthickness= 15,highlightbackground= "white")
        self.campo_quantidade.grid(row=7, column=1, padx=11, pady=5)
        
        tk.Label(self.frame, text= "Qual valor de compra da ação ?", bg= "white", font= ("Roboto",16,"bold"),padx=50).grid(row=8, column=1, padx=11, pady=5)
        self.campo_valor= tk.Entry(self.frame, width=30,highlightthickness= 15,highlightbackground= "white")
        self.campo_valor.grid(row=9, column=1, padx=11, pady=5)
        
        botao_salvar = tk.Button(self.frame, text= "Ordem de compra", command=self.enviarordemcompra, bg = "green", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_salvar.grid(row=10, column=1, padx=11, pady=5)
        
        botao_salvarvenda = tk.Button(self.frame, text= "Ordem de venda", command=self.enviarordemvenda, bg = "red", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_salvarvenda.grid(row=11, column=1, padx=11, pady=5)

    """função para salvar o agendamento no banco de dados"""
    def salvar_agendamento_banco(self):
        acao = self.campo_acao.get()
        quantidade = self.campo_quantidade.get()
        valor = self.campo_valor.get()
        banco = BancoPI()
        cursor = banco.conexao.cursor()

        comando_sql = "INSERT INTO historico_agendamentos (usuario_id,acao, quantidade, valor) VALUES (%s, %s, %s, %s)"
        valores = (self.usuario_id, acao, quantidade, valor)
        cursor.execute(comando_sql, valores)
        banco.conexao.commit()
        cursor.close()
        print(f"Agendamento salvo ID : {self.usuario_id}.")
        
    """metodo para enviar a ordem de compra"""
    def enviarordemcompra(self):
        acao = self.campo_acao.get()
        quantidade = self.campo_quantidade.get()
        valor = self.campo_valor.get()

        print(f"Ordem de Compra Salva:\n Ação: {acao}\n Quantidade: {quantidade}\n Valor: {valor}")
        messagebox.showinfo("Ordem Salva", "Sua ordem de compra foi salva com sucesso!")
        self.salvar_agendamento_banco()
        
    """metodo para enviar a ordem de venda"""    
    def enviarordemvenda(self):
        acao = self.campo_acao.get()
        quantidade = self.campo_quantidade.get()
        valor = self.campo_valor.get()

        print(f"Ordem de venda Salva:\n Ação: {acao}\n Quantidade: {quantidade}\n Valor: {valor}")
        messagebox.showinfo("Ordem Salva", "Sua ordem de venda foi salva com sucesso!")
        self.salvar_agendamento_banco()    
        
    """função para obter a cotação dos ativos usando a API AlphaVantage"""
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








