import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from utils.cryptography import encrypt_hybrid, decrypt_hybrid_qvault
from utils.qvaults import QVaultFormat
from utils.logging import log_message

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class QuantumVaultGUI:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("QuantumVault 🔐")
        self.app.geometry("600x500")
        self.app.resizable(True, True)
        self.app.minsize(500, 400)
        
        self.selected_file_path = ""
        self.mode = "encrypt"  # encrypt ou decrypt
        self.build_layout()

    def build_layout(self):
        # Main container
        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="QuantumVault", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#90caf9"
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Post-Quantum Cryptography Tool",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack()

        # Mode selector
        mode_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        mode_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(mode_frame, text="Mode:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        
        mode_buttons_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        mode_buttons_frame.pack(fill="x", pady=(5, 0))
        
        self.encrypt_btn = ctk.CTkButton(
            mode_buttons_frame,
            text="🔒 Encrypt",
            command=lambda: self.set_mode("encrypt"),
            width=120,
            height=35
        )
        self.encrypt_btn.pack(side="left", padx=(0, 10))
        
        self.decrypt_btn = ctk.CTkButton(
            mode_buttons_frame,
            text="🔓 Decrypt",
            command=lambda: self.set_mode("decrypt"),
            width=120,
            height=35,
            fg_color="transparent",
            text_color="#90caf9",
            border_width=1
        )
        self.decrypt_btn.pack(side="left")

        # File selection
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(file_frame, text="File Selection", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        
        file_content_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_content_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.file_label = ctk.CTkLabel(
            file_content_frame, 
            text="No file selected", 
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.file_label.pack(anchor="w", pady=(0, 10))
        
        select_btn = ctk.CTkButton(
            file_content_frame,
            text="📁 Select File",
            command=self.select_file,
            width=140,
            height=32
        )
        select_btn.pack(anchor="w")

        # Action button
        self.action_btn = ctk.CTkButton(
            main_frame,
            text="🔒 Encrypt File",
            command=self.action,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2e7d32",
            hover_color="#1b5e20"
        )
        self.action_btn.pack(fill="x", pady=(0, 15))

        # Progress section
        self.progress_frame = ctk.CTkFrame(main_frame)
        self.progress_frame.pack(fill="x", pady=(0, 15))
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="#90caf9"
        )
        self.progress_label.pack(pady=(10, 5))
        
        self.progressbar = ctk.CTkProgressBar(self.progress_frame)
        self.progressbar.set(0)
        self.progressbar.pack(fill="x", padx=15, pady=(0, 10))
        
        # Status section
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="x")
        
        ctk.CTkLabel(status_frame, text="Status", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to encrypt/decrypt files",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack(anchor="w", padx=15, pady=(0, 15))

    def set_mode(self, mode):
        self.mode = mode
        if mode == "encrypt":
            self.encrypt_btn.configure(fg_color="#2e7d32", hover_color="#1b5e20")
            self.decrypt_btn.configure(fg_color="transparent", text_color="#90caf9", border_width=1)
            self.action_btn.configure(text="🔒 Encrypt File", fg_color="#2e7d32", hover_color="#1b5e20")
        else:
            self.decrypt_btn.configure(fg_color="#d32f2f", hover_color="#b71c1c")
            self.encrypt_btn.configure(fg_color="transparent", text_color="#90caf9", border_width=1)
            self.action_btn.configure(text="🔓 Decrypt File", fg_color="#d32f2f", hover_color="#b71c1c")
        
        self.reset_ui()

    def select_file(self):
        if self.mode == "encrypt":
            filetypes = [("All files", "*.*")]
            title = "Select file to encrypt"
        else:
            filetypes = [("QuantumVault files", "*.qvault"), ("All files", "*.*")]
            title = "Select .qvault file to decrypt"
        
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if file_path:
            self.selected_file_path = file_path
            filename = os.path.basename(file_path)
            self.file_label.configure(text=filename, text_color="white")
            
            if self.mode == "decrypt" and not file_path.endswith('.qvault'):
                self.status_label.configure(
                    text="⚠️ Warning: Selected file is not a .qvault file",
                    text_color="#ff9800"
                )
                # Show warning message
                messagebox.showwarning(
                    "Warning",
                    f"The selected file '{filename}' is not a .qvault file.\n\nThis may cause errors during decryption."
                )
                log_message(f"Warning: Non-.qvault file selected for decryption: {filename}", "GUI", "WARNING")
            else:
                self.status_label.configure(
                    text=f"File selected: {filename}",
                    text_color="#4caf50"
                )
                log_message(f"File selected: {filename}", "GUI", "INFO")

    def action(self):
        if not self.selected_file_path:
            messagebox.showerror("Error", "Please select a file first.")
            log_message("No file selected for operation", "GUI", "ERROR")
            return
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.process_file)
        thread.daemon = True
        thread.start()

    def process_file(self):
        try:
            self.update_progress("Processing...", 0.2)
            self.action_btn.configure(state="disabled")
            
            if self.mode == "encrypt":
                self.encrypt_file()
            else:
                self.decrypt_file()
                
        except Exception as e:
            self.update_progress("Error occurred", 0)
            self.status_label.configure(text=f"Error: {str(e)}", text_color="#f44336")
            log_message(f"GUI Error: {str(e)}", "GUI", "ERROR")
            
            # Show error message box with more details
            error_details = self.get_error_details(str(e))
            messagebox.showerror(
                "Error",
                f"An error occurred:\n\n{str(e)}\n\n{error_details}\n\nPlease check the logs for more details."
            )
        finally:
            self.action_btn.configure(state="normal")

    def encrypt_file(self):
        try:
            self.update_progress("Encrypting file...", 0.4)
            
            # Generate output filename
            base_name = os.path.splitext(self.selected_file_path)[0]
            output_file = f"{base_name}.qvault"
            
            # Encrypt the file
            encrypt_hybrid(self.selected_file_path, output_file)
            
            self.update_progress("Encryption completed!", 1.0)
            self.status_label.configure(
                text=f"✅ File encrypted successfully!\nCreated: {os.path.basename(output_file)} and {os.path.basename(output_file.replace('.qvault', '.key'))}",
                text_color="#4caf50"
            )
            
            messagebox.showinfo(
                "Success", 
                f"File encrypted successfully!\n\nEncrypted file: {os.path.basename(output_file)}\nKey file: {os.path.basename(output_file.replace('.qvault', '.key'))}\n\n⚠️ Important: Keep the key file safe! Without it, you cannot decrypt the file."
            )
            
        except Exception as e:
            log_message(f"Encryption error in GUI: {str(e)}", "GUI ENCRYPTION", "ERROR")
            raise Exception(f"Encryption failed: {str(e)}")

    def decrypt_file(self):
        try:
            self.update_progress("Checking file...", 0.3)
            
            # Check if it's a valid .qvault file
            if not self.selected_file_path.endswith('.qvault'):
                raise Exception("Selected file is not a .qvault file")
            
            # Check if key file exists
            key_file = self.selected_file_path.replace('.qvault', '.key')
            if not os.path.exists(key_file):
                error_msg = f"Key file not found: {os.path.basename(key_file)}\n\nPlease make sure the .key file is in the same directory as the .qvault file."
                raise Exception(error_msg)
            
            self.update_progress("Decrypting file...", 0.6)
            
            # Generate output filename
            base_name = os.path.splitext(self.selected_file_path)[0]
            output_file = f"{base_name}_decrypted"
            
            # Decrypt the file
            decrypt_hybrid_qvault(self.selected_file_path, output_file, key_file)
            
            self.update_progress("Decryption completed!", 1.0)
            self.status_label.configure(
                text=f"✅ File decrypted successfully!\nSaved as: {os.path.basename(output_file)}",
                text_color="#4caf50"
            )
            
            messagebox.showinfo(
                "Success", 
                f"File decrypted successfully!\n\nDecrypted file: {os.path.basename(output_file)}\n\n✅ The original file extension has been automatically restored."
            )
            
        except Exception as e:
            log_message(f"Decryption error in GUI: {str(e)}", "GUI DECRYPTION", "ERROR")
            raise Exception(f"Decryption failed: {str(e)}")

    def update_progress(self, text, value):
        self.app.after(0, lambda: self.progress_label.configure(text=text))
        self.app.after(0, lambda: self.progressbar.set(value))

    def get_error_details(self, error_msg):
        """Get helpful details for common errors"""
        error_lower = error_msg.lower()
        
        if "file not found" in error_lower:
            return "💡 Tip: Make sure the file exists and you have permission to access it."
        elif "key file not found" in error_lower:
            return "💡 Tip: The .key file must be in the same directory as the .qvault file."
        elif "not a .qvault file" in error_lower:
            return "💡 Tip: Only .qvault files can be decrypted. Make sure you selected the correct file."
        elif "permission" in error_lower:
            return "💡 Tip: Check if you have write permissions in the target directory."
        elif "disk full" in error_lower or "no space" in error_lower:
            return "💡 Tip: Check if you have enough disk space available."
        else:
            return "💡 Tip: Check the logs folder for detailed error information."

    def reset_ui(self):
        self.selected_file_path = ""
        self.file_label.configure(text="No file selected", text_color="gray")
        self.progress_label.configure(text="Ready")
        self.progressbar.set(0)
        self.status_label.configure(text="Ready to encrypt/decrypt files", text_color="gray")

    def run(self):
        self.app.mainloop()

def initGui():
    app = QuantumVaultGUI()
    app.run()

if __name__ == "__main__":
    initGui()