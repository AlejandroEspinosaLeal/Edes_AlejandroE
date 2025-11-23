# ej6_1.py

class Caja:
    def __init__(self, codigo, peso_kg, descripcion_carga, largo, ancho, altura):
        self.codigo = codigo
        self.peso_kg = float(peso_kg)
        self.descripcion_carga = descripcion_carga
        self.largo = float(largo)
        self.ancho = float(ancho)
        self.altura = float(altura)

    def __str__(self):
        return (f"  [CAJA {self.codigo}] Desc: {self.descripcion_carga} | "
                f"Peso: {self.peso_kg}kg | Dim: {self.largo}x{self.ancho}x{self.altura}")

class Camion:
    def __init__(self, matricula, conductor, capacidad_kg, descripcion_carga, rumbo, velocidad):
        self.matricula = matricula
        self.conductor = conductor
        self.capacidad_kg = float(capacidad_kg)
        self.descripcion_carga_camion = descripcion_carga
        # Validación básica de rumbo (1-359)
        self.rumbo = max(1, min(int(rumbo), 359))
        self.velocidad = int(velocidad)
        self.cajas = [] # Lista de objetos Caja

    def peso_total(self):
        total = sum(caja.peso_kg for caja in self.cajas)
        return total

    def add_caja(self, caja):
        peso_actual = self.peso_total()
        if peso_actual + caja.peso_kg <= self.capacidad_kg:
            self.cajas.append(caja)
            print(f"-> Caja {caja.codigo} añadida al camión {self.matricula}.")
            return True
        else:
            print(f"XX Error: La caja {caja.codigo} excede la capacidad del camión {self.matricula}.")
            return False

    def setVelocidad(self, nueva_velocidad):
        self.velocidad = int(nueva_velocidad)

    def setRumbo(self, nuevo_rumbo):
        self.rumbo = max(1, min(int(nuevo_rumbo), 359))

    def claxon(self):
        print("piiiiiii")

    def __str__(self):
        info = (f"=== CAMIÓN {self.matricula} ===\n"
                f"Conductor: {self.conductor} | Capacidad Máx: {self.capacidad_kg}kg\n"
                f"Carga Tipo: {self.descripcion_carga_camion}\n"
                f"Velocidad: {self.velocidad} km/h | Rumbo: {self.rumbo}º\n"
                f"Cajas cargadas: {len(self.cajas)} | Peso Actual Total: {self.peso_total()} kg\n"
                f"Detalle de Cajas:")
        
        for c in self.cajas:
            info += f"\n{c}"
        info += "\n=============================="
        return info

# --- Bloque de ejecución (Script principal) ---
if __name__ == "__main__":
    print("--- CREACIÓN DE OBJETOS ---")
    # 1. Crear 2 objetos Camión
    c1 = Camion("1234-BBB", "Manolo", 1000, "Electronica", 45, 80)
    c2 = Camion("9876-ZZZ", "Ana", 2000, "Fruta", 180, 90)

    # 2. Añadir 3 cajas a cada uno
    # Cajas para camión 1
    c1.add_caja(Caja("C01", 100, "Televisores", 1, 0.5, 0.5))
    c1.add_caja(Caja("C02", 200, "Lavadoras", 0.8, 0.8, 1))
    c1.add_caja(Caja("C03", 50, "Microondas", 0.4, 0.3, 0.3))

    # Cajas para camión 2
    c2.add_caja(Caja("C04", 500, "Manzanas", 2, 2, 2))
    c2.add_caja(Caja("C05", 300, "Peras", 1.5, 1.5, 1.5))
    c2.add_caja(Caja("C06", 400, "Plátanos", 1.5, 1.5, 1.5))

    print("\n--- INFORMACIÓN INICIAL ---")
    print(c1)
    print(c2)

    print("\n--- MODIFICACIONES ---")
    # 3. Añadir 2 cajas al primero y 3 al segundo
    c1.add_caja(Caja("C07", 150, "Ordenadores", 1, 1, 0.5))
    c1.add_caja(Caja("C08", 20, "Ratones", 0.2, 0.2, 0.1))

    c2.add_caja(Caja("C09", 100, "Melones", 1, 1, 1))
    c2.add_caja(Caja("C10", 100, "Sandías", 1, 1, 1))
    c2.add_caja(Caja("C11", 50, "Kiwis", 0.5, 0.5, 0.5))

    # 4. Variar velocidades y rumbos
    c1.setVelocidad(100)
    c1.setRumbo(90)
    
    c2.setVelocidad(60)
    c2.setRumbo(270)

    # 5. El segundo camión toca el claxon
    print("\nAcción Camión 2:")
    c2.claxon()

    print("\n--- INFORMACIÓN FINAL ---")
    print(c1)
    print(c2)
