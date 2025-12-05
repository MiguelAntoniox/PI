import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "PI")))

from login.login import Login
from bancodedados.bancoPI import BancoPI  

if __name__ == "__main__":
    
    banco = BancoPI()
    banco.verificar_integridade()
    app = Login(banco)
    app.iniciar()