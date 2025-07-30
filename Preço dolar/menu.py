from cotacao_dolar import Moedas


moeda = Moedas("Dolar")

def main():
    print("Obtendo cotação atual do dolar... ")
    moeda.cotacao_dolar()
     
        
        
if __name__ == "__main__": ## tem que usar essa merda aq por algum motivo pra rodar
        main()        