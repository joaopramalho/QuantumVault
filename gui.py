import customtkinter
app = customtkinter.CTk()
customtkinter.set_default_color_theme("blue")

import tkinter

# Iniciar GUI
app.title("QuantumVault")
app.geometry("600x300")

# Button Functions

def btf_cryptograph():
    print("Cryptograph button pressed.")

def btf_decryptograph():
    print("Decryptograph button pressed.")

# Cryptograph Button
bt_cryptograph = customtkinter.CTkButton(master=app, text="Cryptograph into a .qvault file", command=btf_cryptograph)
bt_cryptograph.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Decryptograph Button
bt_decryptograph = customtkinter.CTkButton(master=app, text="Decryptograph a .qvault file", command=btf_decryptograph)
bt_decryptograph.place(relx=0.5, rely=0.61, anchor=tkinter.CENTER)


app.mainloop()