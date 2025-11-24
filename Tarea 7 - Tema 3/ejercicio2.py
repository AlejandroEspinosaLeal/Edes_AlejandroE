import tkinter as tk
from tkinter import messagebox, ttk
# (Aquí irían las clases Capitan, Sistema, Plataforma, etc. definidas arriba)
# Asumiremos que están disponibles en el mismo archivo o importadas.

class BatallaNavalGUI:
    def __init__(self, root, flota):
        self.root = root
        self.flota = flota
        self.root.title("Simulador Naval - Ejercicio 2")
        self.root.geometry("600x400")

        # Panel izquierdo: Lista de Plataformas
        self.frame_lista = tk.Frame(root, width=200)
        self.frame_lista.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(self.frame_lista, text="Plataformas en Flota").pack()
        self.listbox = tk.Listbox(self.frame_lista)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.seleccionar_plataforma)

        # Panel derecho: Controles y Detalles
        self.frame_detalle = tk.Frame(root)
        self.frame_detalle.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_nombre = tk.Label(self.frame_detalle, text="Seleccione una unidad", font=("Arial", 14, "bold"))
        self.lbl_nombre.pack(pady=5)

        self.lbl_estado = tk.Label(self.frame_detalle, text="")
        self.lbl_estado.pack()

        # Controles de acción
        self.btn_frame = tk.Frame(self.frame_detalle)
        self.btn_frame.pack(pady=20)

        tk.Button(self.btn_frame, text="Navegar (90, 20)", command=self.accion_navegar).grid(row=0, column=0, padx=5)
        tk.Button(self.btn_frame, text="Recibir Daño (20)", command=self.accion_dano).grid(row=0, column=1, padx=5)
        tk.Button(self.btn_frame, text="Sumergirse/Helicóptero", command=self.accion_especial).grid(row=1, column=0, columnspan=2, pady=5)

        self.plataforma_actual = None
        self.actualizar_lista()

    def actualizar_lista(self):
        self.listbox.delete(0, tk.END)
        for p in self.flota.plataformas:
            self.listbox.insert(tk.END, p.nombre)

    def seleccionar_plataforma(self, event):
        seleccion = self.listbox.curselection()
        if seleccion:
            index = seleccion[0]
            self.plataforma_actual = self.flota.plataformas[index]
            self.actualizar_info()

    def actualizar_info(self):
        if self.plataforma_actual:
            p = self.plataforma_actual
            txt = f"Tipo: {p.__class__.__name__}\nIntegridad: {p.integridad}%\nRumbo: {p.rumbo} | Vel: {p.velocidad}"
            if hasattr(p, 'profundidad'):
                txt += f"\nProfundidad: {p.profundidad}m"
            if hasattr(p, 'helicoptero_desplegado'):
                txt += f"\nHelicóptero: {'En aire' if p.helicoptero_desplegado else 'En cubierta'}"
            
            self.lbl_nombre.config(text=p.nombre)
            self.lbl_estado.config(text=txt)

    def accion_navegar(self):
        if self.plataforma_actual:
            self.plataforma_actual.navegar(90, 20)
            self.actualizar_info()

    def accion_dano(self):
        if self.plataforma_actual:
            self.plataforma_actual.recibir_danio(20)
            self.actualizar_info()

    def accion_especial(self):
        if self.plataforma_actual:
            if isinstance(self.plataforma_actual, Submarino):
                self.plataforma_actual.sumergirse(150)
            elif isinstance(self.plataforma_actual, Fragata):
                self.plataforma_actual.despegar_helicoptero()
            else:
                messagebox.showinfo("Info", "Esta plataforma no tiene acción especial.")
            self.actualizar_info()

if __name__ == "__main__":
    # Recreación rápida de datos para la GUI
    c1 = Capitan("Ramius", "CN", "Vet")
    f1 = Fragata("F-100")
    f1.asignar_capitan(c1)
    s1 = Submarino("S-80")
    
    mi_flota = Flota("Flota GUI")
    mi_flota.agregar_plataforma(f1)
    mi_flota.agregar_plataforma(s1)

    root = tk.Tk()
    app = BatallaNavalGUI(root, mi_flota)
    root.mainloop()
