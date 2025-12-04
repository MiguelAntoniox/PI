import requests    # habilitando uso do requests

 
""" esse  modulo esta puxando dados de moedas USD, EUR, CNY  de uma api """
class Moedas:
    """atributos da classe moedas"""
    
    def __init__(self, tipomoeda):
        self.tipomoeda = tipomoeda
        
    """metodos da classe moedas"""

    def cotacao_dolar(self): # criando uma função
        """esse metodo esta recebendo os dados selecionados atraves de uma API e retornando o valor atual da moeda"""
        
        url = "https://economia.awesomeapi.com.br/last/USD-BRL" # variavel url recebe o link da APi 

        try: # serve para caso o codigo aq dentro der erro, ele mostrar uma mensagem pra esse erro ao usuario usando o EXCEPT
            resposta = requests.get(url) # variavel resposta recebe o Valor do dolar usando o requests.get
            resposta.raise_for_status()   # verifica se a resposta possui algum erro de recebimento usando o .raise_for_status()
            dados = resposta.json() # armazena na variavel dados a resposta convertida pelo .json() em um dicionario python
            cotacao = dados["USDBRL"]["bid"] # pega o valor de "bid" é um valor que vem dentro do arquivo solicitado na url 
            return float(cotacao) # retorna o valor da funcao usando numero flutuante
        
        except Exception as qualerro:   # except identifica um erro # Exception é a classe que nos diz qual erro ocorreu # as qual erro armazena esse erro dentro da variavel qual erro
            print("Ocorreu um erro na puxagem dos dados: " , qualerro)
            return None  
        
    
    def cotacao_euro(self):
        """esse metodo esta recebendo os dados selecionados atraves de uma API e retornando o valor atual da moeda"""
        
        url = "https://economia.awesomeapi.com.br/last/EUR-BRL"
        
        try :
            resposta = requests.get(url)     
            resposta.raise_for_status()
            dados = resposta.json()
            cotacao = dados["EURBRL"]["bid"]    
            return float(cotacao)
        
    
        
        except Exception as qualerro:
            print("Ocorreu um erro na puxagem dos dados: " , qualerro)
            return None
        
    def cotacao_yuan(self):
        """esse metodo esta recebendo os dados selecionados atraves de uma API e retornando o valor atual da moeda"""
        
        url = "https://economia.awesomeapi.com.br/last/CNY-BRL" 
        
        try:
            resposta = requests.get(url)       
            resposta.raise_for_status()
            dados = resposta.json()
            cotacao = dados["CNYBRL"]["bid"]
            return float(cotacao)
        
        except Exception as qualerro:
            print("Ocorreu um erro na puxagem dos dados: " , qualerro)
            return None
        
        
        
        
              
        

    
        
            

                                 


