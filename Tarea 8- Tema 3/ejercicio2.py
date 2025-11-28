import tkinter as tk
from tkinter import messagebox
import random

class BatallaNavalGUI:
    def __init__(self, root, flota):
        self.root = root
        self.flota = flota
        self.root.title("Simulador Naval - Ejercicio 2")
        self.root.geometry("800x600")

        self.panel_control = tk.Frame(root, width=200, bg="#f0f0f0")
        self.panel_control.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.panel_control, text="Selector de Plataforma", font=("Arial", 12, "bold")).pack(pady=10)

        self.lista_naves = tk.Listbox(self.panel_control, height=10)
        self.lista_naves.pack(padx=10, fill=tk.X)
        self.lista_naves.bind('<<ListboxSelect>>', self.seleccionar_nave)

        tk.Label(self.panel_control, text="Acciones", font=("Arial", 10, "bold")).pack(pady=10)
        
        self.btn_navegar = tk.Button(self.panel_control, text="Navegar (Mover)", command=self.accion_navegar)
        self.btn_navegar.pack(fill=tk.X, padx=5, pady=2)

        self.btn_atacar = tk.Button(self.panel_control, text="Atacar", command=self.accion_atacar)
        self.btn_atacar.pack(fill=tk.X, padx=5, pady=2)
        
        self.btn_especial = tk.Button(self.panel_control, text="Acción Especial", command=self.accion_especial)
        self.btn_especial.pack(fill=tk.X, padx=5, pady=2)

        self.btn_info = tk.Button(self.panel_control, text="Ver Estado", command=self.ver_info)
        self.btn_info.pack(fill=tk.X, padx=5, pady=10)

        self.lbl_status = tk.Label(self.panel_control, text="Info: Seleccione nave", wraplength=180, justify="left")
        self.lbl_status.pack(pady=20)

        self.canvas = tk.Canvas(root, bg="#006994")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.iconos = {}
        self.nave_seleccionada = None
        
        self.inicializar_flota()
        self.actualizar_lista()

    def inicializar_flota(self):
        colores = {Fragata: "gray", Corbeta: "black", Submarino: "darkblue"}
        
        for i, nave in enumerate(self.flota.plataformas):
            x = random.randint(50, 500)
            y = random.randint(50, 500)
            
            tipo = type(nave)
            color = colores.get(tipo, "white")
            
            ship_id = self.canvas.create_oval(x, y, x+40, y+20, fill=color, outline="white", width=2)
            text_id = self.canvas.create_text(x+20, y-10, text=nave.nombre, fill="white", font=("Arial", 8))
            
            self.iconos[nave.nombre] = {"ship_id": ship_id, "text_id": text_id, "obj": nave}

    def actualizar_lista(self):
        self.lista_naves.delete(0, tk.END)
        for nave in self.flota.plataformas:
            self.lista_naves.insert(tk.END, nave.nombre)

    def seleccionar_nave(self, event):
        selection = self.lista_naves.curselection()
        if selection:
            nombre = self.lista_naves.get(selection[0])
            self.nave_seleccionada = next((n for n in self.flota.plataformas if n.nombre == nombre), None)
            
            tipo = type(self.nave_seleccionada).__name__
            self.lbl_status.config(text=f"Seleccionada:\n{nombre}\nTipo: {tipo}\nHP: {self.nave_seleccionada.hp}")

    def accion_navegar(self):
        if not self.nave_seleccionada: return
        
        dx = random.randint(-50, 50)
        dy = random.randint(-50, 50)
        
        ids = self.iconos[self.nave_seleccionada.nombre]
        self.canvas.move(ids["ship_id"], dx, dy)
        self.canvas.move(ids["text_id"], dx, dy)
        
        self.nave_seleccionada.navegar(90, 20) 
        self.lbl_status.config(text=f"{self.nave_seleccionada.nombre} moviéndose...")

    def accion_atacar(self):
        if not self.nave_seleccionada: return
        self.nave_seleccionada.atacar()
        
        ids = self.iconos[self.nave_seleccionada.nombre]
        self.canvas.itemconfig(ids["ship_id"], fill="red")
        self.root.after(200, lambda: self.restaurar_color(self.nave_seleccionada))
        
        messagebox.showinfo("Ataque", f"{self.nave_seleccionada.nombre} disparó sus armas.")

    def restaurar_color(self, nave):
        colores = {Fragata: "gray", Corbeta: "black", Submarino: "darkblue"}
        ids = self.iconos[nave.nombre]
        color = colores.get(type(nave), "white")
        self.canvas.itemconfig(ids["ship_id"], fill=color)

    def accion_especial(self):
        if not self.nave_seleccionada: return
        
        if isinstance(self.nave_seleccionada, Submarino):
            self.nave_seleccionada.sumergirse(200)
            messagebox.showinfo("Acción", "Submarino sumergido.")
            ids = self.iconos[self.nave_seleccionada.nombre]
            self.canvas.itemconfig(ids["ship_id"], fill="cyan")
            
        elif isinstance(self.nave_seleccionada, Fragata):
            self.nave_seleccionada.despegar_helicoptero()
            messagebox.showinfo("Acción", "Helicóptero en aire.")
        else:
            messagebox.showinfo("Info", "Esta nave no tiene acción especial definida.")

    def ver_info(self):
        if self.nave_seleccionada:
            messagebox.showinfo("Estado", str(self.nave_seleccionada))

if __name__ == "__main__":
    cap1 = Capitan("Jack Aubrey", "CN")
    cap2 = Capitan("James Norrington", "Comodoro")
    cap3 = Capitan("Marko Ramius", "Cmdt")
    
    f1 = Fragata("F-100 Álvaro de Bazán")
    c1 = Corbeta("P-41 Meteoro")
    s1 = Submarino("S-81 Isaac Peral")
    
    f1.asumir_mando(cap1)
    c1.asumir_mando(cap2)
    s1.asumir_mando(cap3)
    
    flota_atlantico = Flota("Flota del Atlántico")
    flota_atlantico.agregar_plataforma(f1)
    flota_atlantico.agregar_plataforma(c1)
    flota_atlantico.agregar_plataforma(s1)

    root = tk.Tk()
    app = BatallaNavalGUI(root, flota_atlantico)
    root.mainloop()
