import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class QuantumVaultGUI:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("QuantumVault")
        self.app.geometry("500x320")
        self.app.resizable(False, False)
        self.selected_file_path = ""
        self.mode = "encrypt"  # encrypt ou decrypt
        self.build_layout()

    def build_layout(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        self.frame = ctk.CTkFrame(self.app)
        self.frame.pack(expand=True, fill="both", padx=30, pady=24)

        ctk.CTkLabel(self.frame, text="QuantumVault", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 12))

        row = ctk.CTkFrame(self.frame)
        row.pack(fill="x", pady=(0, 18))

        # FS
        file_col = ctk.CTkFrame(row, fg_color="transparent")
        file_col.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.file_label = ctk.CTkLabel(file_col, text="Nenhum arquivo", text_color="gray", anchor="w")
        self.file_label.pack(anchor="w", pady=(0, 4))
        ctk.CTkButton(file_col, text="Selecionar Arquivo", command=self.select_file, width=140).pack(fill="x")

        pass_col = ctk.CTkFrame(row, fg_color="transparent")
        pass_col.pack(side="left", expand=True, fill="x", padx=(10, 0))
        ctk.CTkLabel(pass_col, text="Senha", anchor="w").pack(anchor="w", pady=(0, 4))
        self.password_entry = ctk.CTkEntry(pass_col, show="*", placeholder_text="Digite a senha")
        self.password_entry.pack(fill="x")

        # Barra de progressao
        self.progress_text = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=13), text_color="#90caf9")
        self.progressbar = ctk.CTkProgressBar(self.frame, width=320)
        self.progressbar.set(0)
        self.progress_text.pack_forget()
        self.progressbar.pack_forget()

        self.action_btn = ctk.CTkButton(self.frame, text="Criptografar", command=self.action, height=40, font=ctk.CTkFont(size=15, weight="bold"))
        self.action_btn.pack(pady=(10, 8), fill="x")

        self.toggle_btn = ctk.CTkButton(self.frame, text="Alternar para Descriptografar", command=self.toggle_mode, fg_color="transparent", text_color="#90caf9", border_width=1)
        self.toggle_btn.pack(pady=(0, 0))

    def select_file(self):
        if self.mode == "encrypt":
            filetypes = [("Any file", "*.*")]
        else:
            filetypes = [("QuantumVault files", "*.qvault"), ("Any file", "*.*")]
        file_path = filedialog.askopenfilename(title="Selecionar arquivo", filetypes=filetypes)
        if file_path:
            self.selected_file_path = file_path
            self.file_label.configure(text=os.path.basename(file_path), text_color="white")

    def action(self):
        if not self.selected_file_path:
            messagebox.showerror("Erro", "Selecione um arquivo.")
            return
        if not self.password_entry.get():
            messagebox.showerror("Erro", "Digite a senha.")
            return
        # Exibir barra de progresso
        self.progress_text.configure(text="Processando...", text_color="#90caf9")
        self.progress_text.pack(pady=(0, 2))
        self.progressbar.set(0)
        self.progressbar.pack(pady=(0, 12))
        self.action_btn.configure(state="disabled")
        self.toggle_btn.configure(state="disabled")


    def finish_action(self):
        if self.mode == "encrypt":
            messagebox.showinfo("Sucesso", f"Arquivo criptografado com sucesso!\nArquivo: {os.path.basename(self.selected_file_path)}")
        else:
            messagebox.showinfo("Sucesso", f"Arquivo descriptografado com sucesso!\nArquivo: {os.path.basename(self.selected_file_path)}")
        self.progress_text.pack_forget()
        self.progressbar.pack_forget()
        self.action_btn.configure(state="normal")
        self.toggle_btn.configure(state="normal")

    def toggle_mode(self):
        if self.mode == "encrypt":
            self.mode = "decrypt"
            self.action_btn.configure(text="Descriptografar")
            self.toggle_btn.configure(text="Alternar para Criptografar")
        else:
            self.mode = "encrypt"
            self.action_btn.configure(text="Criptografar")
            self.toggle_btn.configure(text="Alternar para Descriptografar")
        self.password_entry.delete(0, tk.END)
        self.file_label.configure(text="Nenhum arquivo", text_color="gray")
        self.selected_file_path = ""
        self.progress_text.pack_forget()
        self.progressbar.pack_forget()

    def run(self):
        self.app.mainloop()

# Init GUI
def initGui():
    app = QuantumVaultGUI()
    app.run()

if __name__ == "__main__":
    main()