import customtkinter as tk
import db

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
    subjanela = tk.CTkToplevel(janela)
    subjanela.title("Registro")
    subjanela.geometry("1000x800")
    subjanela.grab_set()
    
    label_email = tk.CTkLabel(subjanela, text="Usuário:")
    label_email.pack()

    entry_email = tk.CTkEntry(subjanela)
    entry_email.pack()

    label_senha = tk.CTkLabel(subjanela, text="Senha:")
    label_senha.pack()

    entry_senha = tk.CTkEntry(subjanela, show="*")
    entry_senha.pack()

    botao_login = tk.CTkButton(subjanela, text="Registrar",command=lambda: verificar_registro(entry_email.get(),entry_senha.get(), subjanela))
    botao_login.pack()
    
    
    
def verificar_registro(email, senha, subjanela):
    email_db = db.pegar_email(email)
    if email == email_db[0]:
        CustomMessageBox(subjanela)
        
    else:
        db.criar_conta(email,senha)
        subjanela.destroy()
        

    
    

janela = tk.CTk()
janela.title("Gerenciador da casa do açaí")
janela.geometry("1000x800")

botao = tk.CTkButton(janela, text="Criar conta", command=registro)
botao.pack(padx=10, pady=10)

botao = tk.CTkButton(janela, text="Entrar")
botao.pack(padx=10, pady=10)















if __name__ == "__main__":
    janela.mainloop()


