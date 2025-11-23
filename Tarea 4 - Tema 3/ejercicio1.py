class Barco:
    def __init__(self, nombre, posicionX, posicionY, velocidad, rumbo, numeroMunicion):
        self.nombre = nombre
        self.posicionX = posicionX
        self.posicionY = posicionY
        # [cite_start]Validación velocidad (0-20 km/h) [cite: 11]
        self.velocidad = max(0, min(velocidad, 20))
        # [cite_start]Validación rumbo (1-359 grados) [cite: 12]
        self.rumbo = max(1, min(rumbo, 359))
        self.numeroMunicion = numeroMunicion

    def __str__(self):
        # [cite_start]Método especial __str__ [cite: 16]
        return (f"--- {self.nombre} ---\n"
                f"Posición: ({self.posicionX:.2f}, {self.posicionY:.2f})\n"
                f"Velocidad: {self.velocidad} km/h\n"
                f"Rumbo: {self.rumbo}º\n"
                f"Munición: {self.numeroMunicion}\n")

    def disparar(self):
        # [cite_start]Método disparar [cite: 17]
        if self.numeroMunicion > 0:
            self.numeroMunicion -= 1
            print("El barco ha disparado")
            return True
        else:
            print("No hay munición")
            return False

    def setVelocidad(self, nueva_velocidad):
        # [cite_start]Método setVelocidad [cite: 18]
        self.velocidad = max(0, min(nueva_velocidad, 20))

    def setRumbo(self, nuevo_rumbo):
        # [cite_start]Método setRumbo [cite: 19]
        self.rumbo = max(1, min(nuevo_rumbo, 359))

# --- Bloque de pruebas del Ejercicio 1 ---
if __name__ == "__main__":
    # [cite_start]Crear 3 objetos Barco [cite: 20]
    barco1 = Barco("Titanic", 0, 0, 10, 45, 5)
    barco2 = Barco("Perla Negra", 100, 50, 20, 90, 10)
    barco3 = Barco("Nautilus", 50, 50, 5, 180, 2)

    barcos = [barco1, barco2, barco3]

    for b in barcos:
        print(f"ESTADO INICIAL:\n{b}")
        
        # Probar métodos
        b.setVelocidad(b.velocidad + 2)
        b.setRumbo(b.rumbo + 10)
        b.disparar()
        
        print(f"ESTADO FINAL:\n{b}")
        print("-" * 20)
