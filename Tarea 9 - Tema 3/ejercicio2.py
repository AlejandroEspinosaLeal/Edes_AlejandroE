import tkinter as tk
from ejercicio1 import Planeta, SateliteNatural, SateliteArtificial, Cohete

ANCHO = 800
ALTO = 600

class SimuladorVisual:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Espacial - Ejercicio 3")

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#111122")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.panel = tk.Frame(root, width=250, bg="lightgray")
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.panel.pack_propagate(False)

        tk.Label(self.panel, text="PANEL DE CONTROL", bg="lightgray", font=("Arial", 12, "bold")).pack(pady=10)
        self.lbl_info = tk.Label(self.panel, text="Selecciona un objeto...", bg="white", justify=tk.LEFT, relief=tk.SUNKEN)
        self.lbl_info.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.panel, bg="lightgray")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        tk.Button(btn_frame, text="Avanzar un paso de tiempo", command=self.avanzar_tiempo).pack(fill=tk.X, padx=10, pady=5)
        
        self.animando = False
        self.btn_anim = tk.Button(btn_frame, text="Iniciar animación", command=self.toggle_animacion)
        self.btn_anim.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(btn_frame, text="Actualizar datos panel", command=self.actualizar_info_panel).pack(fill=tk.X, padx=10, pady=5)

        self.objetos = []
        self.obj_seleccionado = None
        self.crear_objetos_iniciales()
        self.dibujar_objetos()

    def crear_objetos_iniciales(self):
        p1 = Planeta("Tierra", "Solar", 100, 400, 300, 0, 0, 20, 1, True)
        
        s1 = SateliteNatural("Luna", "Solar", 10, 500, 300, 0, 2, "Tierra", 100)
        
        a1 = SateliteArtificial("Hubble", "NASA", "USA", 350, 350, 1, -1, "Operativo", "Tierra", 500, "Obs")
        
        c1 = Cohete("Falcon 9", "SpaceX", "USA", 400, 500, 0, -3, "Lanzamiento", 9000, 1000, 5)

        self.objetos = [p1, s1, a1, c1]

    def dibujar_objetos(self):
        self.canvas.delete("all")
        self.mapa_tags = {}

        for obj in self.objetos:
            x, y = obj.x, obj.y
            
            if isinstance(obj, Planeta):
                tag = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="blue", outline="white")
            elif isinstance(obj, SateliteNatural):
                tag = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="gray", outline="white")
            elif isinstance(obj, SateliteArtificial):
                tag = self.canvas.create_rectangle(x-5, y-5, x+5, y+5, fill="red", outline="white")
            elif isinstance(obj, Cohete):
                tag = self.canvas.create_polygon(x, y-10, x-5, y+5, x+5, y+5, fill="orange", outline="white")
            else:
                tag = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="white")

            self.canvas.tag_bind(tag, "<Button-1>", lambda event, o=obj: self.seleccionar_objeto(o))
            self.mapa_tags[obj] = tag

    def seleccionar_objeto(self, obj):
        self.obj_seleccionado = obj
        self.actualizar_info_panel()

    def actualizar_info_panel(self):
        if self.obj_seleccionado:
            obj = self.obj_seleccionado
            texto = f"Nombre: {getattr(obj, 'nombre', getattr(obj, 'nombre_mision', '?'))}\n"
            texto += f"Tipo: {type(obj).__name__}\n"
            texto += f"Pos X: {obj.x:.2f}\n"
            texto += f"Pos Y: {obj.y:.2f}\n"
            texto += f"Vel X: {obj.vx:.2f}\n"
            texto += f"Vel Y: {obj.vy:.2f}\n"
            
            if hasattr(obj, 'propulsion'):
                texto += f"Fuel: {obj.propulsion.cantidad_combustible:.1f}"
            
            self.lbl_info.config(text=texto)
        else:
            self.lbl_info.config(text="Ningún objeto seleccionado.\nHaz click en una figura.")

    def avanzar_tiempo(self):
        for obj in self.objetos:
            obj.avanzar_un_paso_de_tiempo()
        
        self.dibujar_objetos()
        
        if self.obj_seleccionado:
            self.actualizar_info_panel()

    def toggle_animacion(self):
        self.animando = not self.animando
        if self.animando:
            self.btn_anim.config(text="Detener animación")
            self.loop_animacion()
        else:
            self.btn_anim.config(text="Iniciar animación")

    def loop_animacion(self):
        if self.animando:
            self.avanzar_tiempo()
            self.root.after(50, self.loop_animacion)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = SimuladorVisual(ventana)
    ventana.mainloop()]w
