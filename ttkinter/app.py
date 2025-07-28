import customtkinter as tk
import db
from werkzeug.security import check_password_hash, generate_password_hash


tk.set_appearance_mode("dark")


class CustomMessageBox(tk.CTkToplevel):
    def __init__(self, master, title="Mensagem", message="Texto da mensagem"):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()  # Torna a janela modal

        # Centralizar
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - 150
        y = master.winfo_y() + (master.winfo_height() // 2) - 75
        self.geometry(f"+{x}+{y}")

        # Layout
        self.label = tk.CTkLabel(self, text=message, wraplength=260)
        self.label.pack(pady=(20, 10), padx=20)

        self.button = tk.CTkButton(self, text="OK", command=self.close)
        self.button.pack(pady=(0, 20))

    def close(self):
        self.destroy()


def registro():
    janela.withdraw()
    subjanela = tk.CTkToplevel(janela)
    subjanela.title("Registro")
    subjanela.geometry("1280x720")
    subjanela.grab_set()

    label_email = tk.CTkLabel(subjanela, text="Usuário:")
    label_email.pack()

    entry_email = tk.CTkEntry(subjanela)
    entry_email.pack()

    label_senha = tk.CTkLabel(subjanela, text="Senha:")
    label_senha.pack()

    entry_senha = tk.CTkEntry(subjanela, show="*")
    entry_senha.pack()

    botao_login = tk.CTkButton(subjanela, text="Registrar", command=lambda: verificar_registro(
        entry_email.get(), entry_senha.get(), subjanela))
    botao_login.pack()


def verificar_registro(email, senha, subjanela):

    if db.pegar_email(email):
        CustomMessageBox(subjanela, "Email em uso",
                         "Esse email ja foi cadastrado")

    else:
        db.criar_conta(email, generate_password_hash(senha))
        subjanela.withdraw()
        login()
        CustomMessageBox(subjanela, "Conta criada",
                         "A conta foi criada com sucesso")


def login():
    janela.withdraw()
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Login")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()

    label_email = tk.CTkLabel(nova_janela, text="Usuário:")
    label_email.pack()

    entry_email = tk.CTkEntry(nova_janela)
    entry_email.pack()

    label_senha = tk.CTkLabel(nova_janela, text="Senha:")
    label_senha.pack()

    entry_senha = tk.CTkEntry(nova_janela, show="*")
    entry_senha.pack()

    botao_login = tk.CTkButton(nova_janela, text="Efetuar Login", command=lambda: verificar_login(
        entry_email.get(), entry_senha.get(), nova_janela))
    botao_login.pack()


def verificar_login(email, senha, janela):
    senha_criptografada = db.pegar_senha(email)
    if check_password_hash(senha_criptografada[0], senha):
        global usuario
        usuario = db.pegar_email(email)
        janela.withdraw()
        CustomMessageBox(janela, "Logado com sucesso!",
                         "Login efetuado com sucesso.")
        pagina_principal()
    else:
        CustomMessageBox(janela, "Acesso negado",
                         "Email ou Senha estão incorretos.")


def pagina_principal():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Menu Principal")
    nova_janela.geometry("1280x720")
    if usuario[0] == "rafa":
        botao_criar_acai = tk.CTkButton(
            nova_janela, text="Criar Açai", command=criar_acai)
        botao_criar_acai.pack(pady=10)
    botao_criar_pedido = tk.CTkButton(
        nova_janela, text="Criar pedido", command=criar_pedido)
    botao_criar_pedido.pack(pady=10)

    botao_deletar_pedido = tk.CTkButton(
        nova_janela, text="Deletar Pedido", command=deletar_pedido)
    botao_deletar_pedido.pack(pady=10)

    botao_ver_pedidos = tk.CTkButton(
        nova_janela, text="Editar pedido", command=atualizar_pedido)
    botao_ver_pedidos.pack(pady=10)

    botao_ver_pedidos = tk.CTkButton(
        nova_janela, text="Confirmar Entrega", command=confirmar_entrega)
    botao_ver_pedidos.pack(pady=10)

    botao_ver_pedidos = tk.CTkButton(
        nova_janela, text="Ver Lucros", command=ver_lucros)
    botao_ver_pedidos.pack(pady=10)


def confirmar_entrega():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Confirmar entrega")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    itens = db.pegar_pedidos_nao_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=250, height=250)
    frame_lista.pack(pady=20, padx=20)
    for item in itens:
        label = tk.CTkLabel(master=frame_lista,
                            text=f"ID: {item["id"]} | Nome : {item["nome"]} ")
        label.pack(pady=5, padx=10)

    id = tk.CTkEntry(
        nova_janela, placeholder_text="Digite o ID para excluir o pedido")
    id.pack(pady=10)

    botao_enviar = tk.CTkButton(
        nova_janela, text="Enviar", command=lambda: entrega(id.get(), nova_janela))
    botao_enviar.pack()


def entrega(id, subjanela):
    db.atualizar_entrega(id)
    CustomMessageBox(master=subjanela, title="Sucesso",
                     message="Entrega do pedido alterada")
    subjanela.withdraw()


def deletar_pedido():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Deletar Pedidos")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    itens = db.pegar_pedidos_nao_entregues()

    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=500, height=500)
    frame_lista.pack(pady=20, padx=20)

    for item in itens:
        label = tk.CTkLabel(master=frame_lista,
                            text=f"ID: {item["id"]} | Nome : {item["nome"]}")
        label.pack(pady=5, padx=10)

    id = tk.CTkEntry(
        nova_janela, placeholder_text="Digite o ID para excluir o pedido")
    id.pack(pady=10)

    botao_enviar = tk.CTkButton(nova_janela, text="Enviar", command=lambda: excluir_pedido(
        id.get(), nova_janela))
    botao_enviar.pack()


def excluir_pedido(id, subjanela):
    db.excluir_pedido(id)
    CustomMessageBox(master=subjanela, title="Sucesso!",
                     message="Pedido deletado com sucesso!")
    subjanela.withdraw()


def ver_lucros():
    lucro = 0
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Lucros totais")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()

    itens = db.pegar_pedidos_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=250, height=250)
    frame_lista.pack(pady=20, padx=20)
    for item in itens:
        lucro = lucro + item["preco"]
        label = tk.CTkLabel(master=frame_lista,
                            text=f"ID: {item["id"]} | Nome : {item["nome"]} | {item["preco"]}")
        label.pack(pady=5, padx=10)

    label_tipo = tk.CTkLabel(
        master=nova_janela, text=f"O lucro total foi de {lucro}")
    label_tipo.pack()


def atualizar_pedido():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Alterar Pedido")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    itens = db.pegar_pedidos_nao_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=250, height=250)
    frame_lista.pack(pady=20, padx=20)
    for item in itens:
        label = tk.CTkLabel(master=frame_lista,
                            text=f"ID: {item["id"]} | Nome : {item["nome"]} ")
        label.pack(pady=5, padx=10)

    opcoes = db.pegar_tipos_acai()

    label_id = tk.CTkLabel(
        master=nova_janela, text="Digite o ID que deseja Mudar")
    label_id.pack()
    id_cliente = tk.CTkEntry(master=nova_janela)
    id_cliente.pack(pady=5, padx=5)
    label_nome = tk.CTkLabel(
        master=nova_janela, text="Digite o nome do cliente")
    label_nome.pack()
    nome_cliente = tk.CTkEntry(master=nova_janela)
    nome_cliente.pack(pady=5, padx=5)
    nova_lista = [opcao["nome"] for opcao in opcoes]
    label_tipo = tk.CTkLabel(
        master=nova_janela, text="Escolha o açai")
    label_tipo.pack()
    combobox = tk.CTkComboBox(master=nova_janela, values=nova_lista)
    combobox.pack(padx=5, pady=5)
    tamanho = tk.CTkLabel(
        master=nova_janela, text="Escolha o Tamanho")
    tamanho.pack()
    tamanho_lista = ["Pequeno", "Médio", "Grande"]
    tamanho = tk.CTkComboBox(master=nova_janela, values=tamanho_lista)
    tamanho.pack(padx=5, pady=5)

    botao_enviar = tk.CTkButton(nova_janela, text="Enviar", command=lambda: alterar_pedido(
        nome_cliente.get(), combobox.get(), tamanho.get(), nova_janela, id_cliente.get()))
    botao_enviar.pack()


def alterar_pedido(nome, combobox, tamanho, novajanela, id):
    precos = {
        "Pequeno": 16,
        "Médio": 19,
        "Grande": 26
    }

    preco = precos.get(tamanho, 0)
    db.atualizar_pedido(nome, combobox, tamanho, preco, id)
    CustomMessageBox(master=novajanela, title="Sucesso!",
                     message="Pedido Alterado com sucesso")
    novajanela.withdraw()


def criar_acai():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Menu Principal")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nome = tk.CTkEntry(nova_janela, placeholder_text="Nome do açaí")
    nome.pack(pady=10)
    leite_ninho = tk.CTkCheckBox(nova_janela, text="Leite Ninho")
    leite_ninho.pack(pady=5)
    nutella = tk.CTkCheckBox(nova_janela, text="Nutella")
    nutella.pack(pady=5)
    pacoca = tk.CTkCheckBox(nova_janela, text="Paçoca")
    pacoca.pack(pady=5)
    uva = tk.CTkCheckBox(nova_janela, text="Uva")
    uva.pack(pady=5)
    cacau = tk.CTkCheckBox(nova_janela, text="Cacau")
    cacau.pack(pady=5)
    granola = tk.CTkCheckBox(nova_janela, text="Granola")
    granola.pack(pady=5)
    morango = tk.CTkCheckBox(nova_janela, text="Morango")
    morango.pack(pady=5)
    leite_condensado = tk.CTkCheckBox(nova_janela, text="Leite Condensado")
    leite_condensado.pack(pady=5)

    botao_criar = tk.CTkButton(nova_janela, text="Criar Açai", command=lambda: adicionar_acai_ao_banco(nome.get(),
                                                                                                       leite_ninho.get(),
                                                                                                       nutella.get(),
                                                                                                       morango.get(),
                                                                                                       pacoca.get(),
                                                                                                       uva.get(),
                                                                                                       cacau.get(),
                                                                                                       granola.get(),
                                                                                                       leite_condensado.get(),
                                                                                                       nova_janela))
    botao_criar.pack(pady=5)


def adicionar_acai_ao_banco(nome, leite_ninho, nutella, morango, pacoca, uva, cacau, granola, leite_condensado, nova_janela):
    CustomMessageBox(nova_janela, title="Açai Criado com sucesso",
                     message="O açai foi criado.")
    db.adicionar_tipo_acai(
        nome,
        int(leite_ninho),
        int(nutella),
        int(pacoca),
        int(morango),
        int(granola),
        int(cacau),
        int(uva),
        int(leite_condensado)
    )

    nova_janela.withdraw()


def criar_pedido():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Adicionar pedido")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    opcoes = db.pegar_tipos_acai()
    label_nome = tk.CTkLabel(
        master=nova_janela, text="Digite o nome do cliente")
    label_nome.pack()
    nome_cliente = tk.CTkEntry(master=nova_janela)
    nome_cliente.pack(pady=10, padx=10)
    nova_lista = [opcao["nome"] for opcao in opcoes]
    combobox = tk.CTkComboBox(master=nova_janela, values=nova_lista)
    combobox.pack(padx=20, pady=20)
    tamanho_lista = ["Pequeno", "Médio", "Grande"]
    tamanho = tk.CTkComboBox(master=nova_janela, values=tamanho_lista)
    tamanho.pack(padx=20, pady=20)
    botao = tk.CTkButton(master=nova_janela, text="Adicionar Pedido", command=lambda: adicionar_pedido_ao_banco(
        nome_cliente.get(), combobox.get(), tamanho.get(), nova_janela, ))
    botao.pack(pady=10, padx=10)


def adicionar_pedido_ao_banco(nome, escolha, tamanho, janela):
    CustomMessageBox(janela, title="Pedido adicionado",
                     message="Pedido foi adicionado com sucesso")
    janela.withdraw()
    precos = {
        "Pequeno": 16,
        "Médio": 19,
        "Grande": 26
    }
    preco = precos.get(tamanho, 0)
    db.criar_pedido_acai(nome, escolha, tamanho, preco)


janela = tk.CTk()
janela.title("Gerenciador da casa do açaí")
janela.geometry("1280x720")

botao = tk.CTkButton(janela, text="Criar conta", command=registro)
botao.pack(padx=10, pady=10)

botao = tk.CTkButton(janela, text="Fazer login", command=login)
botao.pack(padx=10, pady=10)

if __name__ == "__main__":
    janela.mainloop()
