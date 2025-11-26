from cotacoes import Moedas
from stocks import Stocks
from etfs import Etf
from reits import Reits
import tkinter as tk
from tkinter import *
import os


class Menu_Principal:
    def __init__(self):
        self.janelamenu = tk.Tk()
        self.janelamenu.title("Menu STOP.LO")
        self.janelamenu.geometry("1428x800")
        self.janelamenu.configure(bg="white")
        self.icone()
        self.criar_botoes()
       
       
             
    def icone(self):
       
        caminho = os.path.join(os.path.dirname(__file__), "money.ico")
        if os.path.exists(caminho):
            self.janelamenu.iconbitmap(caminho)
           
    def criar_botoes(self):
       
        moeda = Moedas("Moeda")
       
        tk.Label(self.janelamenu, text= "PAINEL DE DECISÂO DO INVESTIDOR" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=1, padx=11, pady=5)
        frame =  tk.Frame(self.janelamenu, height=2, width=1400, bg="black")
        frame.grid(row=1, column=0, columnspan=3, pady=10)
        tk.Label(frame, text= f"Cotaçao Dolar hoje: {moeda.cotacao_dolar()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(frame, text= f"Cotação Euro hoje: {moeda.cotacao_euro()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(frame, text= f"Cotação Yuan hoje: {moeda.cotacao_yuan()}", bg= "white", font= ("Roboto",16,"bold"), padx=80, ).grid(row=1, column=2, padx=11, pady=5)
        botao_acoes = tk.Button(self.janelamenu, text= "Stocks",command=self.cotacao, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_acoes.grid(row=2, column=0, pady=20)
        botao_ETF = tk.Button(self.janelamenu, text= "ETF's",command=self.etf, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_ETF.grid(row=2, column=1, pady=20)
        botao_reits = tk.Button(self.janelamenu, text= "Reits",command=self.reits, bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_reits.grid(row=2, column=2, pady=20)
       
     
     
    def reits(self):
        Reits().iniciar()
         
   
    def cotacao(self):
        Stocks().iniciar()

    def etf(self):
        Etf().iniciar()
       

   
    def iniciar(self):
         self.janelamenu.mainloop()
         


if __name__ == "__main__":
    app = Menu_Principal()
    app.iniciar() 