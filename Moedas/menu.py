from cotacoes import Moedas
from stocks import Stocks
import tkinter as tk
from tkinter import *
import os


class Menu_Principal:
    def __init__(self):
        self.janelamenu = tk.Tk()
        self.janelamenu.title("Menu STOP.LO")
        self.janelamenu.geometry("1424x800")
        self.janelamenu.configure(bg="white")
        self.icone()
        moeda = Moedas("Moeda")
        # stock = Stocks("Stock")
        
        tk.Label(self.janelamenu, text= "PAINEL DE DECISÂO DO INVESTIDOR" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=1, padx=11, pady=5)
        frame =  tk.Frame(self.janelamenu, height=2, width=1400, bg="black")
        frame.grid(row=1, column=0, columnspan=3, pady=10)
        tk.Label(frame, text= f"Cotaçao Dolar hoje: {moeda.cotacao_dolar()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(frame, text= f"Cotação Euro hoje: {moeda.cotacao_euro()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(frame, text= f"Cotação Yuan hoje: {moeda.cotacao_yuan()}", bg= "white", font= ("Roboto",16,"bold"), padx=80, ).grid(row=1, column=2, padx=11, pady=5)
        
        botao_acoes = tk.Button(self.janelamenu, text= "Ações", bg = "black", font= ("Roboto",16,"bold"), padx=100, fg= "white")
        botao_acoes.grid(row=2, column=1, pady=20)
        
        
        
        
        
    def icone(self):
        
        caminho = os.path.join(os.path.dirname(__file__), "money.ico")
        if os.path.exists(caminho):
            self.janelamenu.iconbitmap(caminho) 
      
    def iniciar(self):
         self.janelamenu.mainloop()
         


if __name__ == "__main__":
    app = Menu_Principal()
    app.iniciar()        
    
    
    
    
    




     
        
