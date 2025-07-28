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

        cursor.execute("""CREATE TABLE IF NOT EXISTS acais
                       (ID INTEGER PRIMARY KEY,
                       nome TEXT,
                       leite_ninho INTEGER,
                       nutella INTEGER,
                       pacoca INTEGER,
                       morango INTEGER,
                       granola INTEGER,
                       cacau INTEGER,
                       uva INTEGER,
                       leite_condensado INTEGER
                       )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS pedidos 
                       (ID INTEGER PRIMARY KEY,
                       nome TEXT,
                       nome_acai TEXT,
                       tamanho TEXT,
                       preco INTEGER,
                       entregue INTEGER)""")


def pegar_email(email):
    with conectar_banco() as cursor:
        cursor.execute(
            """SELECT email FROM usuarios WHERE email=?""", (email,))
        return cursor.fetchone()


def criar_conta(email, senha):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO usuarios (email,senha) VALUES (?,?)""", (email, senha))


def pegar_senha(email):
    with conectar_banco() as cursor:
        cursor.execute(
            """SELECT senha FROM usuarios WHERE email=?""", (email,))
        return cursor.fetchone()


def adicionar_tipo_acai(nome, leite_ninho, nutella, pacoca, morango, granola, cacau, uva, leite_condensado):
    with conectar_banco() as cursor:
        cursor.execute("""INSERT INTO acais (nome, leite_ninho, nutella, pacoca, morango, granola, cacau, uva, leite_condensado) VALUES (?,?,?,?,?,
                       ?,?,?,?)""", (
            nome,
            leite_ninho,
            nutella,
            pacoca,
            morango,
            granola,
            cacau,
            uva,
            leite_condensado
        ))


def pegar_tipos_acai():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM acais""")
        return cursor.fetchall()


def criar_pedido_acai(nome, id, tamanho, preco,):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO pedidos (nome,nome_acai,tamanho,preco,entregue)  VALUES(?,?,?,?,?) """, (nome, id, tamanho, preco, 0))


def pegar_pedidos_nao_entregues():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM pedidos WHERE entregue=0""")
        return cursor.fetchall()


def excluir_pedido(id):
    with conectar_banco() as cursor:
        cursor.execute("""DELETE FROM pedidos WHERE id=?""", (id,))


def pegar_pedidos():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM pedidos""")
        return cursor.fetchall()


def atualizar_pedido(nome, tipo, tamanho, preco, id):
    with conectar_banco() as cursor:
        cursor.execute(
            """UPDATE pedidos SET nome=?,nome_acai=?,tamanho=?,preco=? WHERE id=?""", (nome, tipo, tamanho, preco, id))


def atualizar_entrega(id):
    with conectar_banco() as cursor:
        cursor.execute("""UPDATE pedidos SET entregue=? WHERE id=?""", (1, id))


def pegar_pedidos_entregues():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM pedidos WHERE entregue=1""")
        return cursor.fetchall()


if __name__ == "__main__":
    criar_tabela()
