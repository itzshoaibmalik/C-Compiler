import tkinter as tk
from tkinter import scrolledtext, messagebox
import customtkinter as ctk
import subprocess
import os
import tempfile

class CCompilerGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Simple C Compiler")
        self.window.geometry("1000x800")
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Create buttons frame
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Create buttons
        self.compile_button = ctk.CTkButton(
            self.button_frame,
            text="Compile & Run",
            command=self.compile_and_run
        )
        self.compile_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self.clear_all
        )
        self.clear_button.pack(side="left", padx=5)
        
        # Create editor frame
        self.editor_frame = ctk.CTkFrame(self.main_frame)
        self.editor_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(0, weight=1)
        
        # Create code editor
        self.code_editor = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            bg="#2b2b2b",
            fg="#ffffff"
        )
        self.code_editor.grid(row=0, column=0, sticky="nsew")
        
        # Create output frame
        self.output_frame = ctk.CTkFrame(self.main_frame)
        self.output_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(0, weight=1)
        
        # Create output text
        self.output_text = scrolledtext.ScrolledText(
            self.output_frame,
            wrap=tk.WORD,
            height=10,
            font=("Consolas", 12),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        # Insert default C program
        default_code = """#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    return 0;
}"""
        self.code_editor.insert("1.0", default_code)
        
    def compile_and_run(self):
        # Get the code from editor
        code = self.code_editor.get("1.0", tk.END)
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as source_file:
            source_file.write(code.encode())
            source_path = source_file.name
        
        exe_path = source_path[:-2]  # Remove .c extension
        
        try:
            # Compile the code
            compile_process = subprocess.run(
                ["gcc", source_path, "-o", exe_path],
                capture_output=True,
                text=True
            )
            
            if compile_process.returncode != 0:
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert("1.0", "Compilation Error:\n" + compile_process.stderr)
                return
            
            # Run the compiled program
            run_process = subprocess.run(
                [exe_path],
                capture_output=True,
                text=True
            )
            
            # Display output
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", "Program Output:\n" + run_process.stdout)
            
            if run_process.stderr:
                self.output_text.insert(tk.END, "\nErrors:\n" + run_process.stderr)
                
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", f"Error: {str(e)}")
            
        finally:
            # Clean up temporary files
            try:
                os.remove(source_path)
                os.remove(exe_path)
            except:
                pass
    
    def clear_all(self):
        self.code_editor.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = CCompilerGUI()
    app.run() 