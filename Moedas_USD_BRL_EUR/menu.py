from cotacoes import Moedas


moeda = Moedas("Moeda")

def menu():
    
    
    
    print(f"Obtendo cotação atual do Dolar : {moeda.cotacao_dolar()}")
    print(f"Obtendo cotação atual do Euro : {moeda.cotacao_euro()}")
    print(f"Obtendo cotação atual do Yuan : {moeda.cotacao_yuan()}")

     
        
        
if __name__ == "__main__": ## tem que usar essa merda aq por algum motivo pra rodar
        menu()        