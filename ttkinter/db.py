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
                         endereco TEXT,
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


def atualizar_tipo_acai(nome, *ingredientes):
    """
    Atualiza os ingredientes de um açaí existente.
    Os ingredientes são passados como uma tupla de valores 0 ou 1.
    """
    with conectar_banco() as cursor:
        cursor.execute("""UPDATE acais SET leite_ninho=?, nutella=?, pacoca=?, morango=?, granola=?, cacau=?, uva=?, leite_condensado=? WHERE nome=?""",
                       (ingredientes[0], ingredientes[1], ingredientes[2], ingredientes[3], ingredientes[4], ingredientes[5], ingredientes[6], ingredientes[7], nome))


def renomear_tipo_acai(nome_antigo, novo_nome):
    """
    Renomeia um tipo de açaí.
    """
    with conectar_banco() as cursor:
        cursor.execute("""UPDATE acais SET nome=? WHERE nome=?""",
                       (novo_nome, nome_antigo))


def excluir_tipo_acai(nome_acai):
    """
    Exclui um tipo de açaí do banco de dados.
    """
    with conectar_banco() as cursor:
        cursor.execute("""DELETE FROM acais WHERE nome=?""", (nome_acai,))


def pegar_tipos_acai():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM acais""")
        return cursor.fetchall()


def criar_pedido_acai(nome, endereco, escolha, tamanho, preco):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO pedidos (nome, endereco, nome_acai, tamanho, preco, entregue) VALUES (?,?,?,?,?,?)""", (nome, endereco, escolha, tamanho, preco, 0))


def pegar_pedidos_nao_entregues():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM pedidos WHERE entregue=0""")
        return cursor.fetchall()


def excluir_pedido(id_pedido):
    with conectar_banco() as cursor:
        cursor.execute("""DELETE FROM pedidos WHERE id=?""", (id_pedido,))


def pegar_todos_pedidos():
    """
    Retorna todos os pedidos, entregues e não entregues.
    """
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


criar_tabela()
