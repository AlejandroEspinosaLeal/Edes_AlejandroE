import time

class Capitan:
    def __init__(self, nombre, rango):
        self.nombre = nombre
        self.rango = rango

    def __str__(self):
        return f"{self.rango} {self.nombre}"

class Sistema:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def __repr__(self):
        return f"{self.tipo}: {self.nombre}"

class Plataforma:
    def __init__(self, nombre, sistemas=None):
        self.nombre = nombre
        self.sistemas = sistemas if sistemas else []
        self.capitan = None
        self.hp = 100
        self.rumbo = 0
        self.velocidad = 0

    def asumir_mando(self, capitan):
        self.capitan = capitan

    def navegar(self, rumbo, velocidad):
        self.rumbo = rumbo
        self.velocidad = velocidad
        print(f"[{self.nombre}] Navegando a rumbo {rumbo}° a {velocidad} nudos.")

    def recibir_danio(self, cantidad):
        self.hp -= cantidad
        if self.hp < 0: self.hp = 0
        print(f"¡ALERTA! [{self.nombre}] ha recibido {cantidad} de daño. Integridad: {self.hp}%")

    def esta_operativa(self):
        return self.hp > 0

    def atacar(self):
        print(f"[{self.nombre}] Disparando sistemas de armas...")

    def __str__(self):
        cap = self.capitan if self.capitan else "Sin Capitán"
        estado = "OPERATIVA" if self.esta_operativa() else "HUNDIDA"
        return f"NAVE: {self.nombre} ({estado}) | CAPITÁN: {cap} | SISTEMAS: {self.sistemas}"

class Fragata(Plataforma):
    def __init__(self, nombre, sistemas=None):
        super().__init__(nombre, sistemas)
        self.tiene_helicoptero = True

    def despegar_helicoptero(self):
        if self.tiene_helicoptero and self.esta_operativa():
            print(f"[{self.nombre}] Helicóptero despegando para reconocimiento.")
        else:
            print(f"[{self.nombre}] No se puede desplegar helicóptero.")

class Corbeta(Plataforma):
    def __init__(self, nombre, sistemas=None):
        super().__init__(nombre, sistemas)
        self.agilidad = "Alta"

class Submarino(Plataforma):
    def __init__(self, nombre, sistemas=None):
        super().__init__(nombre, sistemas)
        self.profundidad = 0

    def sumergirse(self, profundidad):
        self.profundidad = profundidad
        print(f"[{self.nombre}] Inmersión a {profundidad} metros.")

class Flota:
    def __init__(self, nombre):
        self.nombre = nombre
        self.plataformas = []

    def agregar_plataforma(self, plataforma):
        self.plataformas.append(plataforma)

    def ordenar_ataque(self):
        print(f"\n--- COMANDO DE FLOTA {self.nombre.upper()}: ¡ORDEN DE ATAQUE GENERAL! ---")
        for p in self.plataformas:
            if p.esta_operativa():
                p.atacar()

    def mostrar_info(self):
        print(f"\n--- REPORTE DE ESTADO: {self.nombre.upper()} ---")
        for p in self.plataformas:
            print(p)

if __name__ == "__main__":
    print("=== INICIO SIMULACIÓN EJERCICIO 1 ===\n")

    cap1 = Capitan("Jack Aubrey", "Capitán de Navío")
    cap2 = Capitan("James Norrington", "Comodoro")
    cap3 = Capitan("Marko Ramius", "Comandante")

    radar = Sistema("Radar Aéreo", "Sensor")
    sonar = Sistema("Sonar Activo", "Sensor")
    misiles = Sistema("Harpoon", "Arma")
    torpedos = Sistema("Mk48", "Arma")
    canion = Sistema("76mm", "Arma")

    f1 = Fragata("F-100 Álvaro de Bazán", sistemas=[radar, misiles])
    c1 = Corbeta("P-41 Meteoro", sistemas=[radar, canion])
    s1 = Submarino("S-81 Isaac Peral", sistemas=[sonar, torpedos])

    f1.asumir_mando(cap1)
    c1.asumir_mando(cap2)
    s1.asumir_mando(cap3)

    flota = Flota("Flota del Atlántico")

    flota.agregar_plataforma(f1)
    flota.agregar_plataforma(c1)
    flota.agregar_plataforma(s1)

    flota.mostrar_info()

    flota.ordenar_ataque()

    c1.navegar(90, 20)

    f1.recibir_danio(30)

    s1.sumergirse(200)

    f1.despegar_helicoptero()

    print("\n--- Verificando estado operativo ---")
    for p in flota.plataformas:
        print(f"{p.nombre}: Operativa = {p.esta_operativa()}")

    flota.mostrar_info()
