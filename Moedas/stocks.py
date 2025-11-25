import requests    # habilitando uso do requests
from tkinter import *
import tkinter as tk




class Stocks:
    """atributos da classe moedas"""
    
    def __init__(self, tipoacao):
        self.tipoacaoa = tipoacao
        
        
    """metodos da classe stocks"""

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
        
    

        
        
        
              
        

    
        
            

                                 


