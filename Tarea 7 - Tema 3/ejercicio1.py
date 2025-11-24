import random

# --- Clases del Modelo (Ejercicio 1) ---

class Capitan:
    def __init__(self, nombre, rango, experiencia):
        self.nombre = nombre
        self.rango = rango
        self.experiencia = experiencia

    def __str__(self):
        return f"{self.rango} {self.nombre} (Exp: {self.experiencia})"

class Sistema:
    def __init__(self, nombre, tipo, potencia_o_rango):
        self.nombre = nombre
        self.tipo = tipo  # "Arma" o "Sensor"
        self.potencia_o_rango = potencia_o_rango

    def __str__(self):
        return f"{self.tipo}: {self.nombre} (Nivel: {self.potencia_o_rango})"

class Plataforma:
    def __init__(self, nombre, sistemas=None):
        self.nombre = nombre
        self.sistemas = sistemas if sistemas else []
        self.capitan = None
        self.integridad = 100  # Salud de la nave
        self.operativa = True
        self.rumbo = 0
        self.velocidad = 0

    def asignar_capitan(self, capitan):
        self.capitan = capitan
        print(f"-> Capitán {capitan.nombre} asume el mando del {self.nombre}.")

    def navegar(self, rumbo, velocidad):
        if self.esta_operativa():
            self.rumbo = rumbo
            self.velocidad = velocidad
            print(f"-> {self.nombre} navegando: Rumbo {self.rumbo}, Velocidad {self.velocidad} nudos.")
        else:
            print(f"-> {self.nombre} no puede navegar (Inoperativa).")

    def recibir_danio(self, cantidad):
        self.integridad -= cantidad
        if self.integridad <= 0:
            self.integridad = 0
            self.operativa = False
            print(f"-> ¡ALERTA! {self.nombre} ha sido destruido.")
        else:
            print(f"-> {self.nombre} recibió daño. Integridad al {self.integridad}%.")

    def esta_operativa(self):
        return self.operativa

    def __str__(self):
        cap_info = self.capitan if self.capitan else "Sin Capitán"
        sys_info = ", ".join([s.nombre for s in self.sistemas])
        estado = "Operativa" if self.operativa else "DESTRUIDA"
        return f"[{self.__class__.__name__}] {self.nombre} | {estado} | Hull: {self.integridad}% | Cap: {cap_info} | Sys: {sys_info}"

class Fragata(Plataforma):
    def __init__(self, nombre, sistemas=None):
        super().__init__(nombre, sistemas)
        self.helicoptero_desplegado = False

    def despegar_helicoptero(self):
        if self.esta_operativa():
            self.helicoptero_desplegado = True
            print(f"-> {self.nombre}: Helicóptero despegando para reconocimiento.")

class Corbeta(Plataforma):
    def __init__(self, nombre, sistemas=None):
        super().__init__(nombre, sistemas)
        # Atributo específico: Alta maniobrabilidad
        self.maniobrabilidad = "Alta"

class Submarino(Plataforma):
    def __init__(self, nombre, sistemas=None):
        super().__init__(nombre, sistemas)
        self.profundidad = 0

    def sumergirse(self, profundidad):
        if self.esta_operativa():
            self.profundidad = profundidad
            print(f"-> {self.nombre}: Sumergiéndose a {self.profundidad} metros.")

class Flota:
    def __init__(self, nombre):
        self.nombre = nombre
        self.plataformas = []

    def agregar_plataforma(self, plataforma):
        self.plataformas.append(plataforma)

    def ordenar_ataque(self):
        print(f"\n[{self.nombre.upper()}] ¡ORDEN GENERAL: TODAS LAS UNIDADES ATACAR!")
        for p in self.plataformas:
            if p.esta_operativa():
                print(f"   - {p.nombre} iniciando secuencia de fuego.")

    def mostrar_informacion(self):
        print(f"\n=== Estado de la {self.nombre} ===")
        for p in self.plataformas:
            print(p)
            # Mostrar detalle de sistemas
            for s in p.sistemas:
                print(f"      * {s}")

# --- Ejecución del Programa Principal (Simulación) ---
if __name__ == "__main__":
    print("=== INICIO DE SIMULACIÓN NAVAL ===")

    # 1. Crear varios capitanes (mínimo 3) [cite: 6, 7]
    c1 = Capitan("Ramius", "Capitán de Navío", "Veterano")
    c2 = Capitan("Aubrey", "Comandante", "Experto")
    c3 = Capitan("Sparrow", "Teniente", "Novato")

    # 2. Crear sistemas de armas y sensores [cite: 11]
    cañon = Sistema("Cañón 76mm", "Arma", 50)
    misil = Sistema("Harpoon", "Arma", 120)
    sonar = Sistema("Sonar Activo", "Sensor", 100)
    radar = Sistema("Radar Aéreo", "Sensor", 200)
    torpedo = Sistema("Torpedo Mk48", "Arma", 300)

    # 3. Crear Fragata, Corbeta y Submarino asignando sistemas en constructores [cite: 8, 12]
    fragata = Fragata("F-100 Álvaro de Bazán", sistemas=[misil, radar])
    corbeta = Corbeta("C-30 Descubierta", sistemas=[cañon])
    submarino = Submarino("S-80 Isaac Peral", sistemas=[torpedo, sonar])

    # 4. Asignar a cada plataforma su capitán [cite: 10]
    fragata.asignar_capitan(c1)
    corbeta.asignar_capitan(c2)
    submarino.asignar_capitan(c3)

    # 5. Crear una Flota y agregar plataformas [cite: 13, 15]
    flota = Flota("Flota del Atlántico")
    flota.agregar_plataforma(fragata)
    flota.agregar_plataforma(corbeta)
    flota.agregar_plataforma(submarino)

    # 6. Mostrar información inicial [cite: 16]
    flota.mostrar_informacion()

    # 7. Ejecutar simulación [cite: 20]
    print("\n--- EJECUTANDO ACCIONES ---")
    
    # La flota ordena un ataque [cite: 21]
    flota.ordenar_ataque()
    
    # Una plataforma navega en un rumbo (90, 20) [cite: 22]
    fragata.navegar(90, 20)
    
    # Otra recibe daño [cite: 23]
    corbeta.recibir_danio(45)
    
    # Un submarino se sumerge (200) [cite: 25]
    submarino.sumergirse(200)
    
    # Una fragata despega un helicóptero [cite: 26]
    fragata.despegar_helicoptero()
    
    # Mostrar si cada plataforma sigue operativa [cite: 27]
    print(f"\n¿{fragata.nombre} operativa? {fragata.esta_operativa()}")
    print(f"¿{corbeta.nombre} operativa? {corbeta.esta_operativa()}")

    # 8. Finalmente se mostrará toda la información de la flota [cite: 28]
    flota.mostrar_informacion()
