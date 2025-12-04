import bcrypt
import mysql.connector
from mysql.connector import Error

"""classe para conectar e manipular o banco de dados MySQL  - criadno o banco e as tabelas caso nao existam"""
class BancoPI():
    
    def __init__(self):
        
        conex = mysql.connector.connect(
            host="127.0.0.1",
            user = "root",
            password="057213"
        )
        
        cursor = conex.cursor()
        cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "banco_PI";')
        num_results = cursor.fetchone()[0]
        conex.close()
        
        if num_results == 0:
            conex = mysql.connector.connect(
                host = "127.0.0.1",
                user = "root",
                password="057213"
            ) 
            cursor = conex.cursor()
            cursor.execute('CREATE DATABASE banco_PI')
            conex.commit()
            conex.close()
            
        try:
            self.conexao = mysql.connector.connect(
                host= 'localhost',
                user = 'root',
                password='057213',
                database = 'banco_PI'
            )
            self.cursor = self.conexao.cursor()
            self.criar_usuarios()
            self.criar_logins()
            self.criar_grupos()
            self.criar_grupos_padrao()
            self.usuario_admin()
            self._criar_tabela_testes()
            self._criar_tabela_defeitos()
            self.criar_Historico_moedas()
            self.salva_cotacoes()
            self.criar_historico_agendamentos()
        except Error as e:
            print(f"Erro ao conectar o MySql: {e}")
    
            raise
     
    """funcao que descobre o ID do usuario"""        
    def obter_id_usuario(self, usuario):
        query = "SELECT id FROM usuarios WHERE usuario = %s"
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            return resultado[0]
        return None

    """metodo que cria a tabela de salva cotacoes no banco de dados"""
    def salva_cotacoes(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS salva_cotacao(
                id INT AUTO_INCREMENT PRIMARY KEY,
                ativo VARCHAR(255) NOT NULL,
                data_cotacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                valor DECIMAL(15, 2) NOT NULL)""")
        self.conexao.commit()   
        
    """metodo que cria a tabela de usuarios no banco de dados"""    
    def criar_usuarios(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(255) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                perfil VARCHAR(50) NOT NULL DEFAULT 'usuario')""")
        self.conexao.commit()
        
    """metodo que cria a tabela de historico de moedas no banco de dados"""    
    def criar_Historico_moedas(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_moedas(
                id INT AUTO_INCREMENT PRIMARY KEY,
                valor DECIMAL(15, 2) NOT NULL,
                data DATETIME NOT NULL,
                moeda VARCHAR(50) NOT NULL )""")
        self.conexao.commit()    

    """metodo que cria a tabela de historico de agendamentos no banco de dados"""
    def criar_historico_agendamentos(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS historico_agendamentos(
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT ,
                acao VARCHAR(10) NOT NULL,
                quantidade INT NOT NULL,
                valor DECIMAL(15, 2) NOT NULL,
                data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
        self.conexao.commit()
        
    """metodo que cria a tabela de logins no banco de dados"""
    def criar_logins(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS logins(
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE)""")
        self.conexao.commit()
        
    """metodo que cria a tabela de grupos e usuario_grupo no banco de dados"""    
    def criar_grupos(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS grupos(
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) UNIQUE NOT NULL)""")
        
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS usuario_grupo(
                usuario_id INT NOT NULL,
                grupo_id INT NOT NULL,
                PRIMARY KEY (usuario_id, grupo_id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE CASCADE)""")
        self.conexao.commit()
        
    """metodo que cria os grupos padrao no banco de dados"""    
    def criar_grupos_padrao(self):
        setores = ["Usuario", "Administrador"]
        for grupo in setores :
            self.adicionar_grupo(grupo)
            
    
    """metodo que cria a tabela de testes no banco de dados"""        
    def _criar_tabela_testes(self):
       
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS testes_sistema (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                funcao_testada VARCHAR(255) NOT NULL,
                tipo_teste VARCHAR(50) NOT NULL,
                caso_teste VARCHAR(255) NOT NULL,
                entrada TEXT,
                resultado_esperado TEXT,
                resultado_obtido TEXT,
                status VARCHAR(20),
                observacoes TEXT
            )
        """)
        self.conexao.commit()   
    
    """metodo que cria a tabela de defeitos no banco de dados"""    
    def _criar_tabela_defeitos(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS defeitos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                modulo VARCHAR(100),
                descricao VARCHAR(255),
                data_ocorrencia DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conexao.commit()    
        
    """metodo que registra defeitos no banco de dados"""    
    def registrar_defeito(self, modulo, descricao):
        self.cursor.execute("""
            INSERT INTO defeitos (modulo, descricao) VALUES (%s, %s)
        """, (modulo, descricao))
        self.conexao.commit() 
     
    """metodo que registra testes no banco de dados"""   
    def registrar_teste(self, funcao, tipo, caso, entrada, esperado, obtido, status, observacoes=""):
        self.cursor.execute("""
            INSERT INTO testes_sistema
            (funcao_testada, tipo_teste, caso_teste, entrada, resultado_esperado, resultado_obtido, status, observacoes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (funcao, tipo, caso, entrada, esperado, obtido, status, observacoes))
        self.conexao.commit()    
                 
    """metodo que adiciona grupos no banco de dados"""    
    def adicionar_grupo(self, nome_grupo):
        try:
            self.cursor.execute("INSERT INTO grupos (nome) VALUES (%s)", (nome_grupo,))
            self.conexao.commit()
        except mysql.connector.IntegrityError:
            pass    
             
    """"metodo que associa usuario a grupos no banco de dados"""    
    def associar_usuario_grupo(self, usuario_id, grupo_nome):
        self.cursor.execute("SELECT id FROM grupos WHERE nome = %s", (grupo_nome,))
        grupo = self.cursor.fetchone()
        if not grupo:
            self.adicionar_grupo(grupo_nome)
            self.cursor.execute("SELECT id FROM grupos WHERE nome = %s", (grupo_nome,))
            grupo = self.cursor.fetchone()

        grupo_id = grupo[0]

        self.cursor.execute(
            "SELECT * FROM usuario_grupo WHERE usuario_id = %s AND grupo_id = %s",
            (usuario_id, grupo_id)
        )
        if self.cursor.fetchone():
            return

        self.cursor.execute(
            "INSERT INTO usuario_grupo (usuario_id, grupo_id) VALUES (%s, %s)",
            (usuario_id, grupo_id)
        )
        self.conexao.commit()

    """metod o que salva usuario no banco de dados  e registra testes e defeitos"""
    def salvar_usuario(self, usuario, senha,perfil="usuario",grupo_nome = None):

        try:

            self.cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
            if self.cursor.fetchone():
                self.registrar_teste(
                    funcao="salvar_usuario",
                    tipo="Dinâmico",
                    caso="Tentativa de cadastro com usuário existente",
                    entrada=f"Usuário: {usuario}",
                    esperado="Erro de duplicidade",
                    obtido="Usuário já existe",
                    status="FALHA",
                    observacoes="Validação falhou — usuário duplicado."
                )
                
                self.registrar_defeito("Bancofinal.salvar_usuario",f"Usuario: {usuario} ja existe no banco")
                raise ValueError("Usuário já existe.")

            senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

            self.cursor.execute(
                "INSERT INTO usuarios (usuario, senha, perfil) VALUES (%s, %s, %s)",
                (usuario, senha_hash, perfil)   
            )
            self.conexao.commit()

            self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
            usuario_id = self.cursor.fetchone()[0]
            
            if grupo_nome:
                self.associar_usuario_grupo(usuario_id, grupo_nome)
                
            self.registrar_teste(
                funcao = "Salvar usuario",
                tipo = "Dinamico",
                caso="Cadastrar novo usuário",
                entrada = f"Usuario: {usuario}, Perfil: {perfil}, Grupo: {grupo_nome}",
                esperado= "Usuário cadastrado com sucesso",
                obtido = "Usuário cadastrado com sucesso",
                status = "SUCESSO",
                observacoes="Teste automático ao iniciar o sistema",
            
            )    

        except mysql.connector.IntegrityError as e:
            self.registrar_defeito("bancoMySQL.salvar_usuario",str(e))
            self.registrar_teste(
                funcao = "Salvar usuario",
                tipo = "Dinamico",
                caso="Erro ao cadastrar novo usuário",
                entrada = f"Usuario: {usuario}",
                esperado= "Usuário cadastrado com sucesso",
                obtido = f"Erro ao cadastrar usuário: {e}",
                status = "FALHA",
                observacoes="Teste automático ao iniciar o sistema",
                
            )
            raise

        except Exception as e:
            self.registrar_defeito("bancoMySQL.salvar_usuario",str(e))
            self.registrar_teste(
                funcao = "Salvar usuario",
                tipo = "Dinamico",
                caso="Erro inesperado ao cadastrar novo usuário",
                entrada = f"Usuario: {usuario}",
                esperado= "Usuário cadastrado com sucesso",
                obtido = f"Erro ao cadastrar usuário: {e}",
                status = "FALHA",
                observacoes="Teste automático ao iniciar o sistema",
               
            )
            raise
        
    """metodo que registra login no banco de dados"""        
    def registrar_login(self, usuario):
        self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (usuario,))
        usuario_id = self.cursor.fetchone()
        if usuario_id:
            self.cursor.execute("INSERT INTO logins (usuario_id) VALUES (%s)", (usuario_id[0],))
            self.conexao.commit()   
             
    """metodo que valida credenciais do usuario no banco de dados"""
    def validar_credenciais(self, usuario, senha):
        query = "SELECT senha FROM usuarios WHERE usuario = %s"
        self.cursor.execute(query, (usuario,))
        resultado = self.cursor.fetchone()
        if resultado:
            senha_hash = resultado[0]
            return bcrypt.checkpw(senha.encode(), senha_hash.encode())
        return False
    
    """metodo que verifica a integridade do banco de dados e registra testes e defeitos"""
    def verificar_integridade(self):
    
        tabelas_necessarias = [
            "usuarios", "logins", "permissoes", "usuario_grupo", "testes_sistema", "defeitos"
        ]
        
        self.cursor.execute("SHOW TABLES")
        existentes = [t[0] for t in self.cursor.fetchall()]
        faltando = [t for t in tabelas_necessarias if t not in existentes]
        
        if faltando:
            status = "FALHA"
            resultado = f"Tabelas faltando: {', '.join(faltando)}"
            self.registrar_defeito("BancoMySQL", resultado)
        else:
            status = "SUCESSO"
            resultado = "Todas as tabelas essenciais estão presentes."
        
        self.registrar_teste(
            funcao="verificar_integridade",
            tipo="Estático",
            caso="Verificação da estrutura inicial do banco",
            entrada="Inicialização do sistema",
            esperado="Todas as tabelas presentes",
            obtido=resultado,
            status=status,
            observacoes="Teste automático ao iniciar o sistema"
        )
        
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = 'admin'")
        tem_admin = self.cursor.fetchone()[0] > 0
        
        if not tem_admin:
            self.registrar_defeito("BancoMySQL", "Usuário admin não encontrado na inicialização.")
            self.registrar_teste(
                funcao="usuario_admin",
                tipo="Estático",
                caso="Criação automática do usuário admin",
                entrada="Banco inicializado",
                esperado="Usuário admin existente",
                obtido="Usuário admin ausente",
                status="FALHA",
                observacoes="Recriar o admin automaticamente"
            )
            self.usuario_admin() 
        else:
            self.registrar_teste(
                funcao="usuario_admin",
                tipo="Estático",
                caso="Verificação de existência do admin",
                entrada="Banco inicializado",
                esperado="Usuário admin existente",
                obtido="Usuário admin presente",
                status="SUCESSO")

    """cria o usuario admin no banco de dados"""
    def usuario_admin(self):
        self.cursor.execute("SELECT COUNT(*) FROM usuarios WHERE usuario = %s", ("admin",))
        if self.cursor.fetchone()[0] == 0:
            senha_hash = bcrypt.hashpw("123".encode(), bcrypt.gensalt()).decode()
            self.cursor.execute(
                "INSERT INTO usuarios (usuario, senha, perfil) VALUES (%s, %s, %s)",
                ("admin", senha_hash, "administrador")
            )
            self.conexao.commit()
            self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", ("admin",))
            admin_id = self.cursor.fetchone()[0]
            self.associar_usuario_grupo(admin_id, "administrador")
            print("Usuário 'admin' criado com sucesso.")

    def obter_grupos_usuario(self, usuario):
        query = """
            SELECT g.nome FROM grupos g
            JOIN usuario_grupo ug ON g.id = ug.grupo_id
            JOIN usuarios u ON u.id = ug.usuario_id
            WHERE u.usuario = %s
        """
        self.cursor.execute(query, (usuario,))
        return [row[0] for row in self.cursor.fetchall()]
    
    """funcao que atualiza usuario no banco de dados chamada pelo editor de usuarios"""
    def atualizar_usuario(self, usuario_antigo, novo_usuario, nova_senha=None, novo_perfil='usuário', grupos=None):
        if usuario_antigo != novo_usuario:
            self.cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (novo_usuario,))
            if self.cursor.fetchone():
                raise ValueError("Usuário já existe.")

        
        if nova_senha:
            senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
            self.cursor.execute(
                "UPDATE usuarios SET usuario = %s, senha = %s, perfil = %s WHERE usuario = %s",
                (novo_usuario, senha_hash, novo_perfil, usuario_antigo)
            )
        else:
            self.cursor.execute(
                "UPDATE usuarios SET usuario = %s, perfil = %s WHERE usuario = %s",
                (novo_usuario, novo_perfil, usuario_antigo)
            )

        self.conexao.commit()

        
        self.cursor.execute("SELECT id FROM usuarios WHERE usuario = %s", (novo_usuario,))
        usuario_id = self.cursor.fetchone()[0]

        
        self.cursor.execute("DELETE FROM usuario_grupo WHERE usuario_id = %s", (usuario_id,))

     
        if grupos:
            for grupo_nome in grupos:
                self.associar_usuario_grupo(usuario_id, grupo_nome)

        self.conexao.commit()


    """metodo que obtém usuarios com grupos usando INNER JOIN no banco de dados"""
    def obter_usuarios_com_grupos_inner_join(self):
        """
        INNER JOIN: Retorna apenas os usuários que estão associados a algum grupo.
        """
        query = """
            SELECT u.usuario, u.perfil, GROUP_CONCAT(g.nome SEPARATOR ', ') as grupos
            FROM usuarios u
            LEFT JOIN usuario_grupo ug ON u.id = ug.usuario_id
            LEFT JOIN grupos g ON ug.grupo_id = g.id
            GROUP BY u.id, u.usuario, u.perfil
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

   
    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conexao') and self.conexao:
            self.conexao.close()



