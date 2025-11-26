import requests    # habilitando uso do requests
from tkinter import *
import tkinter as tk




class Reits:
    """atributos da classe moedas"""
   
    def __init__(self):
        
        self.janelaacoes = tk.Toplevel()
        self.janelaacoes.title("Ações STOP.LO")
        self.janelaacoes.geometry("400x300")
        self.janelaacoes.configure(bg = "white")
       
       
       
       
    def iniciar(self):
        self.janelaacoes.mainloop()