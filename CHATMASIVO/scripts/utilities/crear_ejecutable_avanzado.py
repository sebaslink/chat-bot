#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para crear un ejecutable avanzado con interfaz gráfica
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import webbrowser
import time
import os
import sys

class ChatMasivoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Masivo WhatsApp - Launcher")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Variables
        self.servidor_proceso = None
        self.servidor_activo = False
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        titulo = ttk.Label(main_frame, text="🚀 CHAT MASIVO WHATSAPP", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Estado del servidor
        self.estado_label = ttk.Label(main_frame, text="Estado: Detenido", 
                                     font=("Arial", 12))
        self.estado_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Botones
        self.btn_iniciar = ttk.Button(main_frame, text="▶️ Iniciar Servidor", 
                                     command=self.iniciar_servidor)
        self.btn_iniciar.grid(row=2, column=0, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        
        self.btn_abrir = ttk.Button(main_frame, text="🌐 Abrir en Navegador", 
                                   command=self.abrir_navegador, state="disabled")
        self.btn_abrir.grid(row=2, column=1, padx=(10, 0), pady=5, sticky=(tk.W, tk.E))
        
        self.btn_detener = ttk.Button(main_frame, text="⏹️ Detener Servidor", 
                                     command=self.detener_servidor, state="disabled")
        self.btn_detener.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=4, column=0, columnspan=2, pady=20, sticky=(tk.W, tk.E))
        
        info_text = """
• URL: http://localhost:5000
• Puerto: 5000
• Modo: Producción (Twilio configurado)
• Base de datos: SQLite
        """
        
        ttk.Label(info_frame, text=info_text, justify="left").grid(row=0, column=0)
        
        # Log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=8, width=50)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configurar grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def log(self, mensaje):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {mensaje}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def iniciar_servidor(self):
        """Iniciar el servidor"""
        try:
            self.log("Iniciando servidor...")
            
            # Verificar si el archivo existe
            if not os.path.exists("codchat_simple.py"):
                messagebox.showerror("Error", "No se encuentra codchat_simple.py")
                return
            
            # Iniciar servidor en hilo separado
            thread = threading.Thread(target=self._iniciar_servidor_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"Error al iniciar servidor: {e}")
    
    def _iniciar_servidor_thread(self):
        """Hilo para iniciar el servidor"""
        try:
            self.servidor_proceso = subprocess.Popen(
                [sys.executable, "codchat_simple.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.servidor_activo = True
            self.root.after(0, self._actualizar_estado_iniciado)
            
            # Leer salida del servidor
            while self.servidor_activo and self.servidor_proceso.poll() is None:
                output = self.servidor_proceso.stdout.readline()
                if output:
                    self.root.after(0, lambda: self.log(output.strip()))
                    
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error en servidor: {e}"))
    
    def _actualizar_estado_iniciado(self):
        """Actualizar interfaz cuando el servidor se inicia"""
        self.estado_label.config(text="Estado: Iniciando...")
        self.btn_iniciar.config(state="disabled")
        self.btn_abrir.config(state="normal")
        self.btn_detener.config(state="normal")
        
        # Esperar un poco y abrir navegador
        self.root.after(3000, self._abrir_navegador_auto)
    
    def _abrir_navegador_auto(self):
        """Abrir navegador automáticamente"""
        self.estado_label.config(text="Estado: Activo")
        self.log("Servidor iniciado correctamente")
        self.log("Abriendo navegador...")
        webbrowser.open("http://localhost:5000")
    
    def abrir_navegador(self):
        """Abrir navegador manualmente"""
        if self.servidor_activo:
            webbrowser.open("http://localhost:5000")
            self.log("Navegador abierto")
        else:
            messagebox.showwarning("Advertencia", "El servidor no está activo")
    
    def detener_servidor(self):
        """Detener el servidor"""
        try:
            if self.servidor_proceso:
                self.servidor_proceso.terminate()
                self.servidor_proceso = None
            
            self.servidor_activo = False
            self.estado_label.config(text="Estado: Detenido")
            self.btn_iniciar.config(state="normal")
            self.btn_abrir.config(state="disabled")
            self.btn_detener.config(state="disabled")
            
            self.log("Servidor detenido")
            
        except Exception as e:
            self.log(f"Error al detener servidor: {e}")
    
    def on_closing(self):
        """Manejar cierre de la aplicación"""
        if self.servidor_activo:
            self.detener_servidor()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ChatMasivoApp(root)
    
    # Manejar cierre
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
