from cotacoes import Moedas
# from stocks import Stocks
import tkinter as tk
from tkinter import messagebox


class Menu:
    def __init__(self):
        self.janelamenu = tk.Toplevel()
        self.janelamenu.title("Menu STOP.LO")
        self.janelamenu.geometry("1500x800")
        self.janelamenu.configure(bg="white")
        moeda = Moedas("Moeda")
        # stock = Stocks("Stock")
        
        tk.Label(self.janelamenu, text= "PAINEL DE DECISÂO DO INVESTIDOR" , bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=0, column=1, padx=11, pady=5)
        tk.Label(self.janelamenu, text= f"Cotaçao Dolar hoje: {moeda.cotacao_dolar()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=0, padx=11, pady=5)
        tk.Label(self.janelamenu, text= f"Cotação Euro hoje: {moeda.cotacao_euro()} ", bg= "white", font= ("Roboto",16,"bold"), padx=80).grid(row=1, column=1, padx=11, pady=5)
        tk.Label(self.janelamenu, text= f"Cotação Yuan hoje: {moeda.cotacao_yuan()}", bg= "white", font= ("Roboto",16,"bold"), padx=80, ).grid(row=1, column=2, padx=11, pady=5)
        #tk.Label(self.janelamenu, text= f"Cotação TESLA hoje: {moeda.cotacao_yuan()}", bg= "#8A2BE2", font= "Roboto", padx=80, ).grid(row=2, column=0, padx=11, pady=5)
        
    

            
    def iniciar(self):
        self.janelamenu.mainloop()


if __name__ == "__main__":
    app = Menu()
    app.iniciar()        
    
    
    
    
    




     
        
