import tkinter as tk
from tkinter import messagebox, scrolledtext

class AplicacionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Entornos de Desarrollo - Ejercicio Python")
        self.root.geometry("500x450")
        self.root.config(bg="#f0f0f0")

        # Título
        lbl_titulo = tk.Label(root, text="Seleccione una Herramienta", 
                              font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        lbl_titulo.pack(pady=20)

        # Marco para botones
        frame_botones = tk.Frame(root, bg="#f0f0f0")
        frame_botones.pack(pady=10)

        # Botón 1: Temperatura
        btn_temp = tk.Button(frame_botones, text="1. Conversión Temperatura", 
                             font=("Arial", 11), bg="#4CAF50", fg="white", 
                             width=25, command=self.abrir_conversion)
        btn_temp.pack(pady=5)

        # Botón 2: Tabla
        btn_tabla = tk.Button(frame_botones, text="2. Tabla de Multiplicar", 
                              font=("Arial", 11), bg="#2196F3", fg="white", 
                              width=25, command=self.abrir_tabla)
        btn_tabla.pack(pady=5)

        # Botón 3: Salir
        btn_salir = tk.Button(frame_botones, text="3. Salir", 
                              font=("Arial", 11), bg="#f44336", fg="white", 
                              width=25, command=root.quit)
        btn_salir.pack(pady=5)

        # Área de resultados
        self.area_texto = scrolledtext.ScrolledText(root, width=50, height=10, 
                                                    font=("Consolas", 10))
        self.area_texto.pack(pady=20, padx=10)
        self.log("Bienvenido. Seleccione una opción arriba.")

    def log(self, mensaje):
        """Escribe en el área de texto inferior."""
        self.area_texto.delete(1.0, tk.END)  # Limpiar anterior
        self.area_texto.insert(tk.END, mensaje)

    def abrir_conversion(self):
        # Ventana emergente personalizada (Toplevel) para input
        self.crear_input_window("Conversión Celsius a Fahrenheit", 
                                "Ingrese grados Celsius:", self.calcular_temp)

    def abrir_tabla(self):
        self.crear_input_window("Tabla de Multiplicar", 
                                "Ingrese un número entero:", self.calcular_tabla)

    def crear_input_window(self, titulo, label_text, callback):
        ven = tk.Toplevel(self.root)
        ven.title(titulo)
        ven.geometry("300x150")
        
        tk.Label(ven, text=label_text, font=("Arial", 10)).pack(pady=10)
        entry = tk.Entry(ven)
        entry.pack(pady=5)
        entry.focus()

        def procesar():
            valor = entry.get()
            ven.destroy()
            callback(valor)

        tk.Button(ven, text="Aceptar", command=procesar).pack(pady=10)
        # Permitir pulsar Enter
        ven.bind('<Return>', lambda event: procesar())

    def calcular_temp(self, valor):
        try:
            c = float(valor)
            f = (c * 9/5) + 32
            self.log(f"RESULTADO CONVERSIÓN:\n\n{c}° Celsius = {f:.2f}° Fahrenheit")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor decimal válido.")

    def calcular_tabla(self, valor):
        try:
            n = int(valor)
            resultado = f"TABLA DEL {n}:\n\n"
            for i in range(1, 11):
                resultado += f"{n} x {i} = {n*i}\n"
            self.log(resultado)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número entero válido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGUI(root)
    root.mainloop()
