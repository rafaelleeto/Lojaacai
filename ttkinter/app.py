import customtkinter as tk
import db
from werkzeug.security import check_password_hash, generate_password_hash

tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")

ACAI_PURPLE_DARK = "#5D356A"
ACAI_PURPLE_HOVER = "#8A4C9B"
ACAI_PINK = "#C25776"
ACAI_PINK_HOVER = "#D96C8E"
DARK_BG = "#1F1A2A"
SECONDARY_BG = "#2C2538"
LIGHT_TEXT = "#F9F7F3"


class CustomMessageBox(tk.CTkToplevel):
    def __init__(self, master, title="Mensagem", message="Texto da mensagem"):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()

        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - 150
        y = master.winfo_y() + (master.winfo_height() // 2) - 75
        self.geometry(f"+{x}+{y}")

        frame = tk.CTkFrame(self, fg_color=SECONDARY_BG, corner_radius=10)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.label = tk.CTkLabel(
            frame, text=message, wraplength=260, font=("Roboto", 14), text_color=LIGHT_TEXT)
        self.label.pack(pady=(20, 10), padx=20)

        self.button = tk.CTkButton(
            frame,
            text="OK",
            command=self.close,
            width=100,
            fg_color=ACAI_PURPLE_DARK,
            hover_color=ACAI_PURPLE_HOVER
        )
        self.button.pack(pady=(0, 20))

    def close(self):
        self.destroy()


def registro():
    janela.withdraw()
    subjanela = tk.CTkToplevel(janela)
    subjanela.title("Registro")
    subjanela.geometry("500x500")
    subjanela.grab_set()
    subjanela.configure(fg_color=DARK_BG)

    frame_registro = tk.CTkFrame(
        subjanela, width=350, height=300, corner_radius=15, fg_color=SECONDARY_BG)
    frame_registro.pack(expand=True)
    frame_registro.grid_columnconfigure(0, weight=1)

    label_titulo = tk.CTkLabel(
        frame_registro, text="Criar Nova Conta", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.grid(row=0, column=0, pady=(20, 10))

    label_email = tk.CTkLabel(
        frame_registro, text="Usuário:", text_color=LIGHT_TEXT)
    label_email.grid(row=1, column=0, pady=(10, 0))

    entry_email = tk.CTkEntry(
        frame_registro, placeholder_text="Digite seu usuário", width=250)
    entry_email.grid(row=2, column=0, pady=5)

    label_senha = tk.CTkLabel(
        frame_registro, text="Senha:", text_color=LIGHT_TEXT)
    label_senha.grid(row=3, column=0, pady=(10, 0))

    entry_senha = tk.CTkEntry(frame_registro, show="*",
                              placeholder_text="Digite sua senha", width=250)
    entry_senha.grid(row=4, column=0, pady=5)

    botao_login = tk.CTkButton(
        frame_registro,
        text="Registrar",
        command=lambda: verificar_registro(
            entry_email.get(), entry_senha.get(), subjanela),
        width=200,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao_login.grid(row=5, column=0, pady=20)


def verificar_registro(email, senha, subjanela):
    if len(senha) < 6:
        CustomMessageBox(subjanela, "Senha Fraca",
                         "Senha Fraca, Escolha outra.")
        return

    if not email or not senha:
        CustomMessageBox(subjanela, "Campos Vazios",
                         "Por favor, preencha todos os campos.")
        return

    if db.pegar_email(email):
        CustomMessageBox(subjanela, "Email em uso",
                         "Esse email já foi cadastrado.")
        return
    else:
        db.criar_conta(email, generate_password_hash(senha))
        subjanela.withdraw()
        login()
        CustomMessageBox(janela, "Conta criada",
                         "A conta foi criada com sucesso.")


def login():
    janela.withdraw()
    nova_janela = tk.CTkToplevel(janela)
    nova_janela.title("Login")
    nova_janela.geometry("550x500")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    frame_login = tk.CTkFrame(nova_janela, width=350,
                              height=250, corner_radius=15, fg_color=SECONDARY_BG)
    frame_login.pack(expand=True)
    frame_login.grid_columnconfigure(0, weight=1)

    label_titulo = tk.CTkLabel(
        frame_login, text="Fazer Login", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.grid(row=0, column=0, pady=(20, 10))

    label_email = tk.CTkLabel(
        frame_login, text="Usuário:", text_color=LIGHT_TEXT)
    label_email.grid(row=1, column=0, pady=(10, 0))

    entry_email = tk.CTkEntry(
        frame_login, placeholder_text="Digite seu usuário", width=250)
    entry_email.grid(row=2, column=0, pady=5)

    label_senha = tk.CTkLabel(
        frame_login, text="Senha:", text_color=LIGHT_TEXT)
    label_senha.grid(row=3, column=0, pady=(10, 0))

    entry_senha = tk.CTkEntry(frame_login, show="*",
                              placeholder_text="Digite sua senha", width=250)
    entry_senha.grid(row=4, column=0, pady=5)

    botao_login = tk.CTkButton(
        frame_login,
        text="Efetuar Login",
        command=lambda: verificar_login(
            entry_email.get(), entry_senha.get(), nova_janela),
        width=200,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao_login.grid(row=5, column=0, pady=20)


def logout(janela_menu):
    janela_menu.destroy()
    janela.deiconify()


def verificar_login(email, senha, janela_login):
    if not email or not senha:
        CustomMessageBox(janela_login, "Campos Vazios",
                         "Por favor, preencha todos os campos.")
        return

    senha_criptografada = db.pegar_senha(email)
    if senha_criptografada and check_password_hash(senha_criptografada[0], senha):
        global usuario
        usuario = db.pegar_email(email)
        janela_login.destroy()
        pagina_principal()
    else:
        CustomMessageBox(janela_login, "Acesso Negado",
                         "Usuário ou Senha incorretos.")


def pagina_principal():
    nova_janela = tk.CTkToplevel(janela)
    nova_janela.title("Menu Principal")
    nova_janela.geometry("600x600")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)
    botao_logout = tk.CTkButton(
        nova_janela,
        text="Logout",
        command=lambda: logout(nova_janela),
        width=100,
        height=30,
        corner_radius=8,
        fg_color=ACAI_PINK,
        hover_color=ACAI_PINK_HOVER
    )

    botao_logout.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Menu Principal", font=("Roboto", 30, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 30))

    frame_botoes = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_botoes.pack(pady=10)

    if usuario and usuario[0] == "rafael@gmail.com":
        botao_criar_acai = tk.CTkButton(
            frame_botoes,
            text="Criar Açaí",
            command=criar_acai,
            width=250,
            height=40,
            corner_radius=10,
            fg_color=ACAI_PURPLE_DARK,
            hover_color=ACAI_PURPLE_HOVER
        )
        botao_criar_acai.pack(pady=10, padx=20)

        # O novo botão que substitui o "Alterar"
        botao_gerenciar_acais = tk.CTkButton(
            frame_botoes,
            text="Gerenciar Açaís",
            command=gerenciar_acais,
            width=250,
            height=40,
            corner_radius=10,
            fg_color=ACAI_PURPLE_DARK,
            hover_color=ACAI_PURPLE_HOVER
        )
        botao_gerenciar_acais.pack(pady=10, padx=20)

    botoes_menu = [
        ("Criar Pedido", criar_pedido),
        ("Visualizar Pedidos", visualizar_todos_pedidos),
        ("Deletar Pedido", deletar_pedido),
        ("Editar Pedido", atualizar_pedido),
        ("Confirmar Entrega", confirmar_entrega),
        ("Ver Lucros", ver_lucros)
    ]

    for texto, comando in botoes_menu:
        fg_color = ACAI_PINK if "Deletar" in texto else ACAI_PURPLE_DARK
        hover_color = ACAI_PINK_HOVER if "Deletar" in texto else ACAI_PURPLE_HOVER

        botao = tk.CTkButton(
            frame_botoes,
            text=texto,
            command=comando,
            width=250,
            height=40,
            corner_radius=10,
            fg_color=fg_color,
            hover_color=hover_color
        )
        botao.pack(pady=10, padx=20)


def confirmar_entrega():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Confirmar Entrega")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Pedidos Não Entregues", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    itens = db.pegar_pedidos_nao_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=500, height=300, corner_radius=10, fg_color=SECONDARY_BG)
    frame_lista.pack(pady=20, padx=20)

    if not itens:
        tk.CTkLabel(frame_lista, text="Nenhum pedido pendente.",
                    font=("Roboto", 14), text_color=LIGHT_TEXT).pack(pady=10)
    else:
        for item in itens:
            label = tk.CTkLabel(
                master=frame_lista, text=f"ID: {item['id']} | Cliente: {item['nome']} | Pedido: {item['nome_acai']}", font=("Roboto", 14), text_color=LIGHT_TEXT)
            label.pack(pady=5, padx=10)

    id_entry = tk.CTkEntry(
        nova_janela, placeholder_text="Digite o ID do pedido para confirmar", width=250)
    id_entry.pack(pady=10)

    botao_enviar = tk.CTkButton(
        nova_janela,
        text="Confirmar",
        command=lambda: entrega(id_entry.get(), nova_janela),
        width=150,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao_enviar.pack()


def entrega(id_pedido, subjanela):
    if not id_pedido:
        CustomMessageBox(subjanela, "ID inválido", "Por favor, digite um ID.")
        return
    db.atualizar_entrega(id_pedido)
    CustomMessageBox(master=subjanela, title="Sucesso",
                     message="Entrega do pedido confirmada!")
    subjanela.destroy()


def deletar_pedido():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Deletar Pedidos")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Pedidos Pendentes", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    itens = db.pegar_pedidos_nao_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=500, height=300, corner_radius=10, fg_color=SECONDARY_BG)
    frame_lista.pack(pady=20, padx=20)

    if not itens:
        tk.CTkLabel(frame_lista, text="Nenhum pedido pendente.",
                    font=("Roboto", 14), text_color=LIGHT_TEXT).pack(pady=10)
    else:
        for item in itens:
            label = tk.CTkLabel(
                master=frame_lista, text=f"ID: {item['id']} | Cliente: {item['nome']}", font=("Roboto", 14), text_color=LIGHT_TEXT)
            label.pack(pady=5, padx=10)

    id_entry = tk.CTkEntry(
        nova_janela, placeholder_text="Digite o ID para excluir o pedido", width=250)
    id_entry.pack(pady=10)

    botao_enviar = tk.CTkButton(
        nova_janela,
        text="Excluir Pedido",
        command=lambda: excluir_pedido_db(id_entry.get(), nova_janela),
        width=150,
        corner_radius=8,
        fg_color=ACAI_PINK,
        hover_color=ACAI_PINK_HOVER
    )
    botao_enviar.pack()


def excluir_pedido_db(id_pedido, subjanela):
    if not id_pedido:
        CustomMessageBox(subjanela, "ID inválido", "Por favor, digite um ID.")
        return
    db.excluir_pedido(id_pedido)
    CustomMessageBox(master=subjanela, title="Sucesso!",
                     message="Pedido deletado com sucesso!")
    subjanela.destroy()


def ver_lucros():
    lucro = 0
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Lucros Totais")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Lucros de Pedidos Entregues", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    itens = db.pegar_pedidos_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=500, height=400, corner_radius=10, fg_color=SECONDARY_BG)
    frame_lista.pack(pady=20, padx=20)

    if not itens:
        tk.CTkLabel(frame_lista, text="Nenhum pedido entregue ainda.",
                    font=("Roboto", 14), text_color=LIGHT_TEXT).pack(pady=10)
    else:
        for item in itens:
            lucro += item["preco"]
            label = tk.CTkLabel(
                master=frame_lista, text=f"ID: {item['id']} | Cliente: {item['nome']} | Preço: R${item['preco']:.2f}", font=("Roboto", 14), text_color=LIGHT_TEXT)
            label.pack(pady=5, padx=10)

    label_lucro_total = tk.CTkLabel(
        master=nova_janela, text=f"O lucro total foi de R${lucro:.2f}", font=("Roboto", 20, "bold"), text_color=LIGHT_TEXT)
    label_lucro_total.pack(pady=(10, 20))


def atualizar_pedido():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Alterar Pedido")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Pedidos para Alterar", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    itens = db.pegar_pedidos_nao_entregues()
    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=500, height=250, corner_radius=10, fg_color=SECONDARY_BG)
    frame_lista.pack(pady=20, padx=20)

    if not itens:
        tk.CTkLabel(frame_lista, text="Nenhum pedido pendente.",
                    font=("Roboto", 14), text_color=LIGHT_TEXT).pack(pady=10)
    else:
        for item in itens:
            label = tk.CTkLabel(
                master=frame_lista, text=f"ID: {item['id']} | Cliente: {item['nome']}", font=("Roboto", 14), text_color=LIGHT_TEXT)
            label.pack(pady=5, padx=10)

    frame_form = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_form.pack(pady=10)
    frame_form.grid_columnconfigure(0, weight=1)

    opcoes = db.pegar_tipos_acai()

    label_id = tk.CTkLabel(
        frame_form, text="Digite o ID do pedido que deseja alterar:", text_color=LIGHT_TEXT)
    label_id.grid(row=0, column=0)
    id_cliente = tk.CTkEntry(
        frame_form, placeholder_text="ID do pedido", width=250)
    id_cliente.grid(row=1, column=0, pady=5, padx=5)

    label_nome = tk.CTkLabel(
        frame_form, text="Digite o novo nome do cliente:", text_color=LIGHT_TEXT)
    label_nome.grid(row=2, column=0)
    nome_cliente = tk.CTkEntry(
        frame_form, placeholder_text="Nome do cliente", width=250)
    nome_cliente.grid(row=3, column=0, pady=5, padx=5)

    nova_lista = [opcao["nome"] for opcao in opcoes]
    label_tipo = tk.CTkLabel(
        frame_form, text="Escolha o novo açaí:", text_color=LIGHT_TEXT)
    label_tipo.grid(row=4, column=0)
    combobox = tk.CTkComboBox(frame_form, values=nova_lista, width=250)
    combobox.grid(row=5, column=0, padx=5, pady=5)

    tamanho_lista = ["Pequeno", "Médio", "Grande"]
    tamanho_label = tk.CTkLabel(
        frame_form, text="Escolha o novo tamanho:", text_color=LIGHT_TEXT)
    tamanho_label.grid(row=6, column=0)
    tamanho = tk.CTkComboBox(frame_form, values=tamanho_lista, width=250)
    tamanho.grid(row=7, column=0, padx=5, pady=5)

    botao_enviar = tk.CTkButton(
        nova_janela,
        text="Alterar Pedido",
        command=lambda: alterar_pedido_db(nome_cliente.get(), combobox.get(
        ), tamanho.get(), nova_janela, id_cliente.get()),
        width=200,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao_enviar.pack(pady=20)


def alterar_pedido_db(nome, combobox, tamanho, novajanela, id_pedido):
    if not id_pedido or not nome or not combobox or not tamanho:
        CustomMessageBox(novajanela, "Campos Vazios",
                         "Por favor, preencha todos os campos.")
        return

    precos = {"Pequeno": 16, "Médio": 19, "Grande": 26}
    preco = precos.get(tamanho, 0)
    db.atualizar_pedido(nome, combobox, tamanho, preco, id_pedido)
    CustomMessageBox(master=novajanela, title="Sucesso!",
                     message="Pedido alterado com sucesso!")
    novajanela.destroy()


def criar_acai():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Criar Açaí")
    nova_janela.geometry("700x700")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Criar Novo Açaí", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    frame_acai = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_acai.pack(pady=10)
    frame_acai.grid_columnconfigure(0, weight=1)

    nome = tk.CTkEntry(frame_acai, placeholder_text="Nome do açaí", width=250)
    nome.grid(row=0, column=0, pady=10)

    label_ingredientes = tk.CTkLabel(
        frame_acai, text="Ingredientes:", font=("Roboto", 16), text_color=LIGHT_TEXT)
    label_ingredientes.grid(row=1, column=0, pady=(10, 5))

    ingredientes = ["Leite Ninho", "Nutella", "Paçoca", "Uva",
                    "Cacau", "Granola", "Morango", "Leite Condensado"]
    checkboxes = []
    for i, ingrediente in enumerate(ingredientes):
        cb = tk.CTkCheckBox(frame_acai, text=ingrediente,
                            fg_color=ACAI_PURPLE_DARK, hover_color=ACAI_PURPLE_HOVER, text_color=LIGHT_TEXT)
        cb.grid(row=2+i, column=0, pady=5)
        checkboxes.append(cb)

    botao_criar = tk.CTkButton(
        nova_janela,
        text="Criar Açaí",
        command=lambda: adicionar_acai_ao_banco(
            nome.get(), checkboxes, nova_janela),
        width=200,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao_criar.pack(pady=20)


def adicionar_acai_ao_banco(nome, checkboxes, nova_janela):
    if not nome:
        CustomMessageBox(nova_janela, "Nome Inválido",
                         "Por favor, digite um nome para o açaí.")
        return

    ingredientes_marcados = [cb.get() for cb in checkboxes]
    db.adicionar_tipo_acai(nome, *ingredientes_marcados)
    CustomMessageBox(nova_janela, title="Açaí Criado com Sucesso",
                     message="O açaí foi criado.")
    nova_janela.destroy()


def gerenciar_acais():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Gerenciar Açaís")
    nova_janela.geometry("700x700")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(nova_janela, text="Gerenciar Açaís Existentes", font=(
        "Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    opcoes_acai = db.pegar_tipos_acai()
    lista_nomes_acai = [opcao["nome"] for opcao in opcoes_acai]

    if not lista_nomes_acai:
        tk.CTkLabel(nova_janela, text="Nenhum açaí cadastrado.", font=(
            "Roboto", 14), text_color=LIGHT_TEXT).pack(pady=10)
        return

    label_escolha_acai = tk.CTkLabel(
        nova_janela, text="Escolha o açaí para gerenciar:", text_color=LIGHT_TEXT)
    label_escolha_acai.pack(pady=5)
    combobox_acai = tk.CTkComboBox(
        nova_janela, values=lista_nomes_acai, width=250)
    combobox_acai.pack(pady=5)

    frame_rename = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_rename.pack(pady=10)

    label_novo_nome = tk.CTkLabel(
        frame_rename, text="Novo Nome:", text_color=LIGHT_TEXT)
    label_novo_nome.pack()
    entry_novo_nome = tk.CTkEntry(
        frame_rename, placeholder_text="Digite o novo nome", width=250)
    entry_novo_nome.pack(pady=5)

    frame_ingredientes = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_ingredientes.pack(pady=10)
    frame_ingredientes.grid_columnconfigure(0, weight=1)

    label_ingredientes = tk.CTkLabel(frame_ingredientes, text="Alterar Ingredientes:", font=(
        "Roboto", 16), text_color=LIGHT_TEXT)
    label_ingredientes.grid(row=0, column=0, pady=(10, 5))

    ingredientes_disponiveis = ["Leite Ninho", "Nutella", "Paçoca",
                                "Uva", "Cacau", "Granola", "Morango", "Leite Condensado"]
    checkboxes = []
    for i, ingrediente in enumerate(ingredientes_disponiveis):
        cb = tk.CTkCheckBox(frame_ingredientes, text=ingrediente,
                            fg_color=ACAI_PURPLE_DARK, hover_color=ACAI_PURPLE_HOVER, text_color=LIGHT_TEXT)
        cb.grid(row=1+i, column=0, pady=5)
        checkboxes.append(cb)

    def atualizar_checkboxes(event):
        acai_selecionado = combobox_acai.get()
        if acai_selecionado:
            acai_info = [a for a in opcoes_acai if a['nome']
                         == acai_selecionado][0]
            for i, ingrediente in enumerate(ingredientes_disponiveis):
                if acai_info[ingrediente.replace(" ", "_").lower()]:
                    checkboxes[i].select()
                else:
                    checkboxes[i].deselect()

    combobox_acai.bind("<<ComboboxSelected>>", atualizar_checkboxes)

    def salvar_alteracoes():
        acai_selecionado = combobox_acai.get()
        novo_nome = entry_novo_nome.get()

        if novo_nome and novo_nome != acai_selecionado:
            db.renomear_tipo_acai(acai_selecionado, novo_nome)

        ingredientes_marcados = [cb.get() for cb in checkboxes]
        db.atualizar_tipo_acai(
            novo_nome if novo_nome else acai_selecionado, *ingredientes_marcados)

        CustomMessageBox(nova_janela, title="Açaí Atualizado",
                         message="O açaí foi atualizado com sucesso.")
        nova_janela.destroy()

    def excluir_acai_db():
        acai_selecionado = combobox_acai.get()
        db.excluir_tipo_acai(acai_selecionado)
        CustomMessageBox(nova_janela, title="Açaí Excluído",
                         message=f"O açaí '{acai_selecionado}' foi excluído.")
        nova_janela.destroy()

    frame_botoes = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_botoes.pack(pady=20)

    botao_salvar = tk.CTkButton(
        frame_botoes,
        text="Salvar Alterações",
        command=salvar_alteracoes,
        width=200,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao_salvar.pack(side="left", padx=10)

    botao_excluir = tk.CTkButton(
        frame_botoes,
        text="Excluir Açaí",
        command=excluir_acai_db,
        width=200,
        corner_radius=8,
        fg_color=ACAI_PINK,
        hover_color=ACAI_PINK_HOVER
    )
    botao_excluir.pack(side="left", padx=10)


def visualizar_todos_pedidos():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Todos os Pedidos")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(nova_janela, text="Todos os Pedidos (Pendentes e Entregues)", font=(
        "Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    frame_lista = tk.CTkScrollableFrame(
        master=nova_janela, width=800, height=500, corner_radius=10, fg_color=SECONDARY_BG)
    frame_lista.pack(pady=20, padx=20)

    pedidos = db.pegar_todos_pedidos()

    if not pedidos:
        tk.CTkLabel(frame_lista, text="Nenhum pedido encontrado.", font=(
            "Roboto", 14), text_color=LIGHT_TEXT).pack(pady=10)
    else:
        for pedido in pedidos:
            status = "Entregue" if pedido["entregue"] else "Pendente"
            texto_pedido = (
                f"ID: {pedido['id']} | Cliente: {pedido['nome']} | "
                f"Endereço: {pedido['endereco']} | Açaí: {pedido['nome_acai']} | "
                f"Tamanho: {pedido['tamanho']} | Preço: R${pedido['preco']:.2f} | Status: {status}"
            )
            label = tk.CTkLabel(master=frame_lista, text=texto_pedido, font=(
                "Roboto", 14), text_color=LIGHT_TEXT, anchor="w")
            label.pack(fill="x", padx=10, pady=5)


def criar_pedido():
    nova_janela = tk.CTkToplevel()
    nova_janela.title("Adicionar Pedido")
    nova_janela.geometry("1280x720")
    nova_janela.grab_set()
    nova_janela.configure(fg_color=DARK_BG)

    label_titulo = tk.CTkLabel(
        nova_janela, text="Adicionar Novo Pedido", font=("Roboto", 24, "bold"), text_color=LIGHT_TEXT)
    label_titulo.pack(pady=(20, 10))

    opcoes = db.pegar_tipos_acai()

    frame_form = tk.CTkFrame(nova_janela, fg_color="transparent")
    frame_form.pack(pady=10)
    frame_form.grid_columnconfigure(0, weight=1)

    label_nome = tk.CTkLabel(
        frame_form, text="Nome do cliente:", text_color=LIGHT_TEXT)
    label_nome.grid(row=0, column=0)
    nome_cliente = tk.CTkEntry(
        frame_form, placeholder_text="Digite o nome do cliente", width=250)
    nome_cliente.grid(row=1, column=0, pady=5, padx=10)

    label_endereco = tk.CTkLabel(
        frame_form, text="Endereço do cliente:", text_color=LIGHT_TEXT)
    label_endereco.grid(row=2, column=0)
    entry_endereco = tk.CTkEntry(
        frame_form, placeholder_text="Digite o Endereço do cliente", width=250)
    entry_endereco.grid(row=3, column=0, pady=5, padx=10)

    nova_lista = [opcao["nome"] for opcao in opcoes]
    label_acai = tk.CTkLabel(
        frame_form, text="Escolha o tipo de açaí:", text_color=LIGHT_TEXT)
    label_acai.grid(row=4, column=0)
    combobox = tk.CTkComboBox(frame_form, values=nova_lista, width=250)
    combobox.grid(row=5, column=0, padx=20, pady=5)

    tamanho_lista = ["Pequeno", "Médio", "Grande"]
    label_tamanho = tk.CTkLabel(
        frame_form, text="Escolha o tamanho:", text_color=LIGHT_TEXT)
    label_tamanho.grid(row=6, column=0)
    tamanho = tk.CTkComboBox(frame_form, values=tamanho_lista, width=250)
    tamanho.grid(row=7, column=0, padx=20, pady=5)

    botao = tk.CTkButton(
        nova_janela,
        text="Adicionar Pedido",
        command=lambda: adicionar_pedido_ao_banco(
            nome_cliente.get(), entry_endereco.get(), combobox.get(), tamanho.get(), nova_janela),
        width=200,
        corner_radius=8,
        fg_color=ACAI_PURPLE_DARK,
        hover_color=ACAI_PURPLE_HOVER
    )
    botao.pack(pady=20, padx=10)


def adicionar_pedido_ao_banco(nome, endereco, escolha, tamanho, janela):
    if not nome or not escolha or not tamanho or not endereco:
        CustomMessageBox(janela, "Campos Vazios",
                         "Por favor, preencha todos os campos.")
        return

    precos = {"Pequeno": 16, "Médio": 19, "Grande": 26}
    preco = precos.get(tamanho, 0)
    db.criar_pedido_acai(nome, endereco, escolha, tamanho, preco)
    CustomMessageBox(janela, title="Pedido Adicionado",
                     message="O pedido foi adicionado com sucesso.")
    janela.destroy()


# ---
# Janela Principal
# ---
janela = tk.CTk()
janela.title("Gerenciador da Casa do Açaí")
janela.geometry("550x550")
janela.configure(fg_color=DARK_BG)

label_bem_vindo = tk.CTkLabel(
    janela, text="Bem-vindo(a) Á Casa do Açaí!", font=("Roboto", 36, "bold"), text_color=LIGHT_TEXT)
label_bem_vindo.pack(pady=(90, 100))

botao_criar_conta = tk.CTkButton(
    janela,
    text="Criar conta",
    command=registro,
    width=250,
    height=50,
    corner_radius=10,
    fg_color=ACAI_PURPLE_DARK,
    hover_color=ACAI_PURPLE_HOVER
)
botao_criar_conta.pack(padx=10, pady=(10, 5))

botao_fazer_login = tk.CTkButton(
    janela,
    text="Fazer login",
    command=login,
    width=250,
    height=50,
    corner_radius=10,
    fg_color=ACAI_PURPLE_DARK,
    hover_color=ACAI_PURPLE_HOVER
)
botao_fazer_login.pack(padx=10, pady=(5, 10))


if __name__ == "__main__":
    janela.mainloop()
