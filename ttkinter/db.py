import sqlite3
from contextlib import contextmanager


@contextmanager
def conectar_banco():
    conexao = sqlite3.connect("acai.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    try:
        yield cursor
    finally:
        conexao.commit()
        cursor.close()
        conexao.close()


def criar_tabela():
    with conectar_banco() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios 
                       (ID INTEGER PRIMARY KEY,
                       email TEXT UNIQUE,
                       senha TEXT)""")
        
def pegar_email(email):
    with conectar_banco() as cursor:
        cursor.execute("""SELECT email FROM usuarios WHERE email=?""",(email ,))
        return cursor.fetchone()
    
def criar_conta(email,senha):
    with conectar_banco() as cursor:
        cursor.execute("""INSERT INTO usuarios (email,senha) VALUES (?,?)""",(email,senha))
    
    
if __name__ == "__main__":
    criar_tabela()
    
        
    