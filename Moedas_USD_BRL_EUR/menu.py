from cotacoes import Moedas


moeda = Moedas("Moeda")

def menu():
    
    print("Escolha uma opção do sistema:	")
    print("1 - Cotação das moedas")
    print("2 - Sair")
    
    
    escolha = input("Escolha uma opção:  ")
    
    
    if escolha == "1":
        print(f"Obtendo cotação atual do Dolar : {moeda.cotacao_dolar()}")
        print(f"Obtendo cotação atual do Euro : {moeda.cotacao_euro()}")
        print(f"Obtendo cotação atual do Yuan : {moeda.cotacao_yuan()}")
       
    if escolha == "2":
            pass

    
    
    
    
    




     
        
        
if __name__ == "__main__": ## tem que usar essa merda aq por algum motivo pra rodar
        menu()        