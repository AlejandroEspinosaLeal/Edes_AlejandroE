import tkinter as tk
from tkinter import messagebox, ttk
import math
import pygame
import os
from ejercicio1 import Barco  # Importamos la clase creada anteriormente

class BatallaNavalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval - Control de Flota")
        self.root.geometry("1000x700")

        # [cite_start]Inicializar Pygame para audio [cite: 27]
        pygame.mixer.init()
        self.cargar_audios()

        # Lista de barcos y variables
        self.barcos = []
        self.barco_seleccionado = None
        self.iconos_barcos = [] # Referencias para evitar garbage collection

        # Interfaz principal
        self.crear_interfaz()
        
        # Iniciar bucle de animación (movimiento)
        self.actualizar_movimiento()

    def cargar_audios(self):
        # [cite_start]Cargar sonido de fondo y disparo [cite: 26]
        try:
            if os.path.exists("fondo.mp3"):
                pygame.mixer.music.load("fondo.mp3")
                pygame.mixer.music.play(-1) # Loop infinito
            if os.path.exists("disparo.wav"):
                self.sonido_disparo = pygame.mixer.Sound("disparo.wav")
            else:
                self.sonido_disparo = None
        except Exception as e:
            print(f"Error cargando audio: {e}")
            self.sonido_disparo = None

    def crear_interfaz(self):
        # --- Panel Izquierdo: Mapa (Canvas) ---
        self.canvas = tk.Canvas(self.root, bg="navy", width=700, height=700)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # --- Panel Derecho: Controles ---
        panel_control = tk.Frame(self.root, width=300, bg="lightgray", padx=10, pady=10)
        panel_control.pack(side=tk.RIGHT, fill=tk.Y)

        # [cite_start]Sección 1: Crear Nuevo Barco [cite: 24]
        tk.Label(panel_control, text="CREAR NUEVO BARCO", font=("Arial", 12, "bold"), bg="lightgray").pack(pady=5)
        
        tk.Label(panel_control, text="Nombre:", bg="lightgray").pack()
        self.entry_nombre = tk.Entry(panel_control)
        self.entry_nombre.pack()

        tk.Label(panel_control, text="Pos X (0-700):", bg="lightgray").pack()
        self.entry_x = tk.Entry(panel_control)
        self.entry_x.pack()
        
        tk.Label(panel_control, text="Pos Y (0-700):", bg="lightgray").pack()
        self.entry_y = tk.Entry(panel_control)
        self.entry_y.pack()

        tk.Button(panel_control, text="Crear Barco", command=self.crear_barco, bg="green", fg="white").pack(pady=10)

        tk.Frame(panel_control, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=10)

        # [cite_start]Sección 2: Selector de Barco Activo [cite: 25]
        tk.Label(panel_control, text="BARCO ACTIVO", font=("Arial", 12, "bold"), bg="lightgray").pack(pady=5)
        
        self.combo_barcos = ttk.Combobox(panel_control, state="readonly")
        self.combo_barcos.pack(fill=tk.X)
        self.combo_barcos.bind("<<ComboboxSelected>>", self.seleccionar_barco)

        # [cite_start]Sección 3: Controles del Barco Activo [cite: 25]
        tk.Label(panel_control, text="Modificar Rumbo (1-359):", bg="lightgray").pack(pady=(10,0))
        self.scale_rumbo = tk.Scale(panel_control, from_=1, to=359, orient=tk.HORIZONTAL)
        self.scale_rumbo.pack(fill=tk.X)
        tk.Button(panel_control, text="Aplicar Rumbo", command=self.actualizar_rumbo).pack()

        tk.Label(panel_control, text="Modificar Velocidad (0-20):", bg="lightgray").pack(pady=(10,0))
        self.scale_velocidad = tk.Scale(panel_control, from_=0, to=20, orient=tk.HORIZONTAL)
        self.scale_velocidad.pack(fill=tk.X)
        tk.Button(panel_control, text="Aplicar Velocidad", command=self.actualizar_velocidad).pack()

        tk.Label(panel_control, text="Acciones:", bg="lightgray").pack(pady=(15,5))
        # [cite_start]Botón Disparar [cite: 17, 26]
        tk.Button(panel_control, text="🔥 DISPARAR 🔥", command=self.accion_disparar, bg="red", fg="white", font=("Arial", 10, "bold")).pack(fill=tk.X, pady=5)
        
        # Monitor de estado
        self.lbl_estado = tk.Label(panel_control, text="Info: Seleccione un barco", bg="white", relief=tk.SUNKEN, height=4)
        self.lbl_estado.pack(fill=tk.X, pady=10)

    def crear_barco(self):
        try:
            nom = self.entry_nombre.get()
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            # Valores por defecto para velocidad, rumbo y munición
            v = 0
            r = 90
            m = 10 
            
            nuevo_barco = Barco(nom, x, y, v, r, m)
            self.barcos.append(nuevo_barco)
            
            # Actualizar lista desplegable
            lista_nombres = [b.nombre for b in self.barcos]
            self.combo_barcos['values'] = lista_nombres
            self.combo_barcos.current(len(self.barcos)-1)
            self.seleccionar_barco(None)
            
            # Limpiar entradas
            self.entry_nombre.delete(0, tk.END)
            self.entry_x.delete(0, tk.END)
            self.entry_y.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor introduce coordenadas numéricas válidas.")

    def seleccionar_barco(self, event):
        idx = self.combo_barcos.current()
        if idx >= 0:
            self.barco_seleccionado = self.barcos[idx]
            # Actualizar controles con valores actuales
            self.scale_rumbo.set(self.barco_seleccionado.rumbo)
            self.scale_velocidad.set(self.barco_seleccionado.velocidad)
            self.actualizar_info_label()

    def actualizar_rumbo(self):
        if self.barco_seleccionado:
            self.barco_seleccionado.setRumbo(self.scale_rumbo.get())
            self.actualizar_info_label()

    def actualizar_velocidad(self):
        if self.barco_seleccionado:
            self.barco_seleccionado.setVelocidad(self.scale_velocidad.get())
            self.actualizar_info_label()

    def accion_disparar(self):
        if self.barco_seleccionado:
            disparo_exitoso = self.barco_seleccionado.disparar() # Imprime en consola y decrementa
            self.actualizar_info_label()
            
            if disparo_exitoso and self.sonido_disparo:
                self.sonido_disparo.play()

    def actualizar_info_label(self):
        if self.barco_seleccionado:
            txt = (f"{self.barco_seleccionado.nombre}\n"
                   f"Vel: {self.barco_seleccionado.velocidad} km/h | Rumbo: {self.barco_seleccionado.rumbo}\n"
                   f"Munición: {self.barco_seleccionado.numeroMunicion}\n"
                   f"Pos: ({int(self.barco_seleccionado.posicionX)}, {int(self.barco_seleccionado.posicionY)})")
            self.lbl_estado.config(text=txt)

    def dibujar_barco(self, barco):
        # [cite_start]Intentar cargar imagen, si no, dibujar triángulo [cite: 23]
        x, y = barco.posicionX, barco.posicionY
        
        if os.path.exists("barco.png"):
            try:
                # Nota: Tkinter nativo no rota imágenes fácilmente sin PIL. 
                # Se muestra el icono en la posición X, Y.
                img = tk.PhotoImage(file="barco.png")
                self.iconos_barcos.append(img) # Guardar referencia
                self.canvas.create_image(x, y, image=img, tags="movil")
                self.canvas.create_text(x, y-20, text=barco.nombre, fill="white", tags="movil")
            except:
                self._dibujar_triangulo(x, y, barco)
        else:
            self._dibujar_triangulo(x, y, barco)

    def _dibujar_triangulo(self, x, y, barco):
        # Dibuja un triángulo orientado según el rumbo si no hay imagen
        # Rumbo 0 = Norte (arriba), 90 = Este (derecha)
        rad = math.radians(barco.rumbo - 90) # Ajuste trigonométrico
        size = 15
        
        # Puntas del triángulo
        x1 = x + size * math.cos(rad)
        y1 = y + size * math.sin(rad)
        
        x2 = x + size * math.cos(rad + 2.5)
        y2 = y + size * math.sin(rad + 2.5)
        
        x3 = x + size * math.cos(rad - 2.5)
        y3 = y + size * math.sin(rad - 2.5)
        
        color = "yellow" if barco == self.barco_seleccionado else "white"
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, tags="movil")
        self.canvas.create_text(x, y-20, text=barco.nombre, fill="white", tags="movil")

    def actualizar_movimiento(self):
        # Limpiar canvas
        self.canvas.delete("movil")
        self.iconos_barcos = []

        for barco in self.barcos:
            # [cite_start]Calcular nueva posición basada en velocidad y rumbo [cite: 23]
            # Velocidad muy alta sale de pantalla rápido, dividimos por un factor para la demo visual
            factor_velocidad = 0.1 
            
            # Trigonometría: Rumbo 0 es Norte (Y disminuye), Rumbo 90 es Este (X aumenta)
            # Convertir rumbo geográfico a matemático
            angulo_rad = math.radians(barco.rumbo - 90)
            
            dx = (barco.velocidad * factor_velocidad) * math.cos(angulo_rad)
            dy = (barco.velocidad * factor_velocidad) * math.sin(angulo_rad)
            
            barco.posicionX += dx
            barco.posicionY += dy
            
            # Rebote simple si toca bordes (opcional, para no perder barcos)
            if barco.posicionX < 0 or barco.posicionX > 700: barco.posicionX -= dx*2
            if barco.posicionY < 0 or barco.posicionY > 700: barco.posicionY -= dy*2

            self.dibujar_barco(barco)

        if self.barco_seleccionado:
            self.actualizar_info_label()

        # Llamar a esta función de nuevo en 50ms
        self.root.after(50, self.actualizar_movimiento)

if __name__ == "__main__":
    root = tk.Tk()
    app = BatallaNavalGUI(root)
    root.mainloop()