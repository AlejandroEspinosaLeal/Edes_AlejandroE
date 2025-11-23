# ej6_2.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import pygame
import os
import random
from ej6_1 import Camion, Caja  # Importamos las clases del ejercicio anterior

class AppTransporte:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Flota - Camiones y Cajas")
        self.root.geometry("1100x700")

        # Inicializar Pygame Mixer
        pygame.mixer.init()
        self.sonido_claxon = None
        self.cargar_sonido()

        # Datos
        self.flota = [] # Lista de diccionarios {'obj': Camion, 'x': float, 'y': float, 'color': str}
        self.camion_activo_idx = -1

        # Interfaz
        self.crear_interfaz()
        
        # Bucle de animación
        self.animar()

    def cargar_sonido(self):
        try:
            if os.path.exists("claxon.wav"):
                self.sonido_claxon = pygame.mixer.Sound("claxon.wav")
            else:
                print("Aviso: 'claxon.wav' no encontrado. Se usará solo texto.")
        except Exception as e:
            print(f"Error audio: {e}")

    def crear_interfaz(self):
        # --- Panel Izquierdo: Mapa ---
        self.canvas = tk.Canvas(self.root, bg="#333333", width=750, height=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Evento clic en mapa para seleccionar (aproximado)
        self.canvas.bind("<Button-1>", self.seleccionar_por_clic)
        # Evento clic derecho para claxon
        self.canvas.bind("<Button-3>", lambda e: self.tocar_claxon())

        # --- Panel Derecho: Controles ---
        panel = tk.Frame(self.root, width=350, bg="#f0f0f0", padx=10, pady=10)
        panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Título
        tk.Label(panel, text="PANEL DE CONTROL", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        # Selector de Camión
        tk.Label(panel, text="Seleccionar Camión Activo:", bg="#f0f0f0").pack(anchor="w")
        self.combo_camiones = ttk.Combobox(panel, state="readonly")
        self.combo_camiones.pack(fill=tk.X, pady=5)
        self.combo_camiones.bind("<<ComboboxSelected>>", self.seleccionar_camion_combo)

        # Datos del Camión Activo
        frame_datos = tk.LabelFrame(panel, text="Datos en tiempo real", bg="#f0f0f0")
        frame_datos.pack(fill=tk.X, pady=10)

        self.lbl_info = tk.Label(frame_datos, text="Seleccione un camión...", justify=tk.LEFT, bg="#f0f0f0")
        self.lbl_info.pack(fill=tk.X, padx=5, pady=5)

        # Controles de Movimiento
        frame_mov = tk.LabelFrame(panel, text="Movimiento", bg="#f0f0f0")
        frame_mov.pack(fill=tk.X, pady=5)

        tk.Label(frame_mov, text="Velocidad:", bg="#f0f0f0").pack()
        self.scale_vel = tk.Scale(frame_mov, from_=0, to=150, orient=tk.HORIZONTAL, command=self.actualizar_velocidad)
        self.scale_vel.pack(fill=tk.X)

        tk.Label(frame_mov, text="Rumbo (Grados):", bg="#f0f0f0").pack()
        self.scale_rumbo = tk.Scale(frame_mov, from_=1, to=359, orient=tk.HORIZONTAL, command=self.actualizar_rumbo)
        self.scale_rumbo.pack(fill=tk.X)

        # Gestión de Carga
        frame_carga = tk.LabelFrame(panel, text="Gestión de Carga", bg="#f0f0f0")
        frame_carga.pack(fill=tk.X, pady=5)
        
        tk.Button(frame_carga, text="Añadir Caja (Standard)", command=self.btn_add_caja, bg="#dddddd").pack(fill=tk.X, pady=2)
        tk.Button(frame_carga, text="Ver Carga Detallada", command=self.ver_carga, bg="#dddddd").pack(fill=tk.X, pady=2)

        # Acciones Varias
        tk.Button(panel, text="🔊 TOCAR CLAXON", command=self.tocar_claxon, bg="orange", fg="white", font=("bold")).pack(fill=tk.X, pady=10)
        
        tk.Frame(panel, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # Crear Nuevo Camión
        tk.Label(panel, text="NUEVO CAMIÓN", font=("Arial", 10, "bold"), bg="#f0f0f0").pack()
        tk.Label(panel, text="Matrícula:", bg="#f0f0f0").pack()
        self.entry_mat = tk.Entry(panel)
        self.entry_mat.pack(fill=tk.X)
        
        tk.Button(panel, text="Crear Camión", command=self.crear_camion, bg="green", fg="white").pack(fill=tk.X, pady=5)

    def crear_camion(self):
        mat = self.entry_mat.get()
        if not mat:
            messagebox.showerror("Error", "Introduce una matrícula")
            return

        # Creamos camión con valores por defecto para agilizar
        # (matricula, conductor, capacidad, descripcion, rumbo, velocidad)
        nuevo_camion = Camion(mat, "Conductor X", 2000, "General", random.randint(1, 359), random.randint(20, 80))
        
        # Añadir a la flota con posición aleatoria
        datos_camion = {
            'obj': nuevo_camion,
            'x': random.randint(50, 700),
            'y': random.randint(50, 650),
            'color': f"#{random.randint(0, 0xFFFFFF):06x}" # Color aleatorio hex
        }
        self.flota.append(datos_camion)
        
        self.actualizar_lista_combo()
        self.entry_mat.delete(0, tk.END)

    def actualizar_lista_combo(self):
        vals = [f"{d['obj'].matricula}" for d in self.flota]
        self.combo_camiones['values'] = vals
        if self.flota:
            self.combo_camiones.current(len(self.flota)-1)
            self.seleccionar_camion_combo(None)

    def seleccionar_camion_combo(self, event):
        idx = self.combo_camiones.current()
        if idx >= 0:
            self.camion_activo_idx = idx
            c = self.flota[idx]['obj']
            # Actualizar sliders sin disparar eventos
            self.scale_vel.set(c.velocidad)
            self.scale_rumbo.set(c.rumbo)
            self.actualizar_label_info()

    def seleccionar_por_clic(self, event):
        # Buscar si el clic cae cerca de algún camión
        for i, data in enumerate(self.flota):
            dist = math.hypot(event.x - data['x'], event.y - data['y'])
            if dist < 30: # Radio de clic
                self.combo_camiones.current(i)
                self.seleccionar_camion_combo(None)
                break

    def actualizar_velocidad(self, val):
        if self.camion_activo_idx >= 0:
            self.flota[self.camion_activo_idx]['obj'].setVelocidad(int(val))
            self.actualizar_label_info()

    def actualizar_rumbo(self, val):
        if self.camion_activo_idx >= 0:
            self.flota[self.camion_activo_idx]['obj'].setRumbo(int(val))
            self.actualizar_label_info()

    def btn_add_caja(self):
        if self.camion_activo_idx < 0: return
        
        # Añadir una caja genérica para probar
        peso = random.randint(50, 500)
        caja = Caja(f"A-{random.randint(100,999)}", peso, "Generico", 1, 1, 1)
        
        exito = self.flota[self.camion_activo_idx]['obj'].add_caja(caja)
        if not exito:
            messagebox.showwarning("Carga", "¡Capacidad excedida!")
        self.actualizar_label_info()

    def ver_carga(self):
        if self.camion_activo_idx < 0: return
        c = self.flota[self.camion_activo_idx]['obj']
        txt = ""
        for caja in c.cajas:
            txt += str(caja) + "\n"
        if not txt: txt = "Camión vacío."
        messagebox.showinfo(f"Carga de {c.matricula}", txt)

    def tocar_claxon(self):
        if self.camion_activo_idx >= 0:
            # Lógica
            self.flota[self.camion_activo_idx]['obj'].claxon()
            # Audio
            if self.sonido_claxon:
                self.sonido_claxon.play()
            
            # Efecto visual breve (cambio color texto)
            self.lbl_info.config(fg="red")
            self.root.after(200, lambda: self.lbl_info.config(fg="black"))

    def actualizar_label_info(self):
        if self.camion_activo_idx >= 0:
            c = self.flota[self.camion_activo_idx]['obj']
            txt = (f"Matrícula: {c.matricula}\n"
                   f"Cond: {c.conductor}\n"
                   f"Vel: {c.velocidad} | Rumbo: {c.rumbo}\n"
                   f"Cajas: {len(c.cajas)} | Peso: {c.peso_total()}/{c.capacidad_kg}")
            self.lbl_info.config(text=txt)

    def animar(self):
        self.canvas.delete("all")
        
        for i, data in enumerate(self.flota):
            camion = data['obj']
            
            # Cálculo de movimiento
            # Convertir rumbo geográfico (0=Norte, sentido horario) a trigonométrico
            rad = math.radians(camion.rumbo - 90)
            
            # Reducimos velocidad para que quepa en pantalla
            factor_v = 0.05
            dx = camion.velocidad * factor_v * math.cos(rad)
            dy = camion.velocidad * factor_v * math.sin(rad)
            
            data['x'] += dx
            data['y'] += dy
            
            # Rebote simple en bordes
            w, h = 750, 700
            if data['x'] < 0: data['x'] = 0; camion.setRumbo((camion.rumbo + 180) % 360)
            if data['x'] > w: data['x'] = w; camion.setRumbo((camion.rumbo + 180) % 360)
            if data['y'] < 0: data['y'] = 0; camion.setRumbo((camion.rumbo + 180) % 360)
            if data['y'] > h: data['y'] = h; camion.setRumbo((camion.rumbo + 180) % 360)

            # Dibujar
            # Si es el activo, borde blanco grueso
            width_outline = 3 if i == self.camion_activo_idx else 1
            color_outline = "white" if i == self.camion_activo_idx else "black"
            
            # Representación simple (Rectángulo rotado es complejo en Canvas básico, usaremos circulo + linea dirección)
            r = 20
            self.canvas.create_oval(data['x']-r, data['y']-r, data['x']+r, data['y']+r, 
                                    fill=data['color'], outline=color_outline, width=width_outline)
            
            # Linea de dirección
            end_x = data['x'] + (r+10) * math.cos(rad)
            end_y = data['y'] + (r+10) * math.sin(rad)
            self.canvas.create_line(data['x'], data['y'], end_x, end_y, fill="white", width=2)
            
            # Texto Matrícula
            self.canvas.create_text(data['x'], data['y']-r-10, text=camion.matricula, fill="white", font=("Arial", 8))

        if self.camion_activo_idx >= 0:
            self.actualizar_label_info()

        self.root.after(50, self.animar)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTransporte(root)
    root.mainloop()