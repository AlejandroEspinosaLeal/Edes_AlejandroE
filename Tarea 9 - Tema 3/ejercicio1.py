class CuerpoEspacial:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def avanzar_un_paso_de_tiempo(self):
        self.x += self.vx
        self.y += self.vy

class SistemaPropulsion:
    def __init__(self, tipo_combustible, cantidad_combustible, empuje_maximo):
        self.tipo_combustible = tipo_combustible
        self.cantidad_combustible = cantidad_combustible
        self.empuje_maximo = empuje_maximo

    def consumir_combustible(self, cantidad):
        if self.cantidad_combustible >= cantidad:
            self.cantidad_combustible -= cantidad
            return True
        else:
            print("Combustible insuficiente.")
            return False

    def queda_combustible(self):
        return self.cantidad_combustible > 0

    def __str__(self):
        return f"Propulsión ({self.tipo_combustible}): {self.cantidad_combustible:.1f} restantes."

class SistemaComunicaciones:
    def __init__(self, potencia_maxima, frecuencias_soportadas):
        self.potencia_maxima = potencia_maxima
        self.frecuencias_soportadas = frecuencias_soportadas
        self.operativo = True

    def enviar_mensaje(self, mensaje):
        if self.operativo:
            print(f"[COMMS] Enviando: '{mensaje}'")
        else:
            print("[COMMS] Error: Sistema averiado.")

class CuerpoCelesteNatural(CuerpoEspacial):
    def __init__(self, nombre, tipo, sistema_nombre, masa, x, y, vx, vy):
        super().__init__(x, y, vx, vy)
        self.nombre = nombre
        self.tipo_cuerpo = tipo
        self.nombre_sistema_estelar = sistema_nombre
        self.masa_aproximada = masa

    def __str__(self):
        return f"[{self.tipo_cuerpo}] {self.nombre} | Pos: ({self.x}, {self.y})"

class Planeta(CuerpoCelesteNatural):
    def __init__(self, nombre, sistema_nombre, masa, x, y, vx, vy, radio, max_sat, atm_densa):
        super().__init__(nombre, "Planeta", sistema_nombre, masa, x, y, vx, vy)
        self.radio_medio = radio
        self.max_satelites = max_sat
        self.atmosfera_densa = atm_densa

class SateliteNatural(CuerpoCelesteNatural):
    def __init__(self, nombre, sistema_nombre, masa, x, y, vx, vy, orbita_a, dist_media):
        super().__init__(nombre, "Satélite Natural", sistema_nombre, masa, x, y, vx, vy)
        self.nombre_cuerpo_orbita = orbita_a
        self.distancia_media = dist_media

class Cometa(CuerpoCelesteNatural):
    def __init__(self, nombre, sistema_nombre, masa, x, y, vx, vy, periodo, cola_visible):
        super().__init__(nombre, "Cometa", sistema_nombre, masa, x, y, vx, vy)
        self.periodo_orbital = periodo
        self.cola_visible = cola_visible

class EstructuraEspacial(CuerpoEspacial):
    def __init__(self, nombre_mision, agencia, pais, x, y, vx, vy, estado):
        super().__init__(x, y, vx, vy)
        self.nombre_mision = nombre_mision
        self.agencia = agencia
        self.pais_principal = pais
        self.estado_operativo = estado
        self.centro_control_asociado = None

    def asignar_centro(self, centro):
        self.centro_control_asociado = centro

    def __str__(self):
        cc = self.centro_control_asociado.nombre if self.centro_control_asociado else "Sin asignar"
        return f"[Misión] {self.nombre_mision} ({self.estado_operativo}) | CC: {cc} | Pos: ({self.x}, {self.y})"

class SateliteArtificial(EstructuraEspacial):
    def __init__(self, nombre, agencia, pais, x, y, vx, vy, estado, orbita_a, altura, funcion):
        super().__init__(nombre, agencia, pais, x, y, vx, vy, estado)
        self.nombre_cuerpo_orbita = orbita_a
        self.altura_orbita = altura
        self.funcion_principal = funcion
        self.propulsion = SistemaPropulsion("Iones", 50, 10)
        self.comunicaciones = SistemaComunicaciones(200, ["UHF", "VHF"])

class Cohete(EstructuraEspacial):
    def __init__(self, nombre, agencia, pais, x, y, vx, vy, estado, empuje, carga, n_lanz):
        super().__init__(nombre, agencia, pais, x, y, vx, vy, estado)
        self.empuje_total = empuje
        self.capacidad_carga = carga
        self.contador_lanzamientos = n_lanz
        self.propulsion = SistemaPropulsion("Líquido", 5000, empuje)
        self.comunicaciones = SistemaComunicaciones(500, ["Banda-X"])

class SistemaPlanetario:
    def __init__(self, nombre, estrella_principal):
        self.nombre = nombre
        self.nombre_cuerpo_principal = estrella_principal
        self.cuerpos_celestes = []

    def agregar_cuerpo(self, cuerpo):
        self.cuerpos_celestes.append(cuerpo)

class Constelacion:
    def __init__(self, nombre, tipo_orbita):
        self.nombre_constelacion = nombre
        self.tipo_orbita = tipo_orbita
        self.estructuras = []

    def agregar_estructura(self, estructura):
        self.estructuras.append(estructura)

class CentroControl:
    def __init__(self, nombre, pais, num_operadores):
        self.nombre = nombre
        self.pais = pais
        self.numero_operadores = num_operadores

    def enviar_orden(self, estructura, orden):
        print(f"CC {self.nombre} ordena a {estructura.nombre_mision}: {orden}")

    def consultar_estado(self, estructura):
        print(f"CC {self.nombre} consulta estado de {estructura.nombre_mision}: {estructura.estado_operativo}")

if __name__ == "__main__":
    print("=== INICIO SIMULACIÓN CONSOLA ===")

    sis_solar = SistemaPlanetario("Sistema Solar", "Sol")
    tierra = Planeta("Tierra", "Planeta", "Sistema Solar", 5.9e24, 0, 0, 0, 0, 6371, 1, True)
    luna = SateliteNatural("Luna", "Satélite", "Sistema Solar", 7.3e22, 10, 0, 0, 1, "Tierra", 384400)
    
    sis_solar.agregar_cuerpo(tierra)
    sis_solar.agregar_cuerpo(luna)

    cc_houston = CentroControl("Houston", "USA", 20)

    const_gps = Constelacion("GPS", "MEO")
    sat_gps1 = SateliteArtificial("GPS-IIR", "NASA", "USA", 20, 20, 1, 1, "En órbita", "Tierra", 20200, "Navegación")
    sat_gps1.asignar_centro(cc_houston)
    const_gps.agregar_estructura(sat_gps1)

    cohete_sls = Cohete("Artemis I", "NASA", "USA", 0, 0, 0, 5, "En lanzamiento", 8800, 95000, 1)
    cohete_sls.asignar_centro(cc_houston)

    print("\n--- ESTADO INICIAL ---")
    print(tierra)
    print(luna)
    print(sat_gps1)
    print(f"   > {sat_gps1.propulsion}")
    print(cohete_sls)
    print(f"   > {cohete_sls.propulsion}")

    print("\n--- EJECUTANDO ACCIONES ---")
    tierra.avanzar_un_paso_de_tiempo() 
    luna.avanzar_un_paso_de_tiempo()
    cohete_sls.avanzar_un_paso_de_tiempo()
    
    print("Cohete consumiendo combustible...")
    cohete_sls.propulsion.consumir_combustible(1000)

    print("Cambiando estado de satélite...")
    sat_gps1.estado_operativo = "Fuera de servicio"
    
    cc_houston.consultar_estado(sat_gps1)

    print("\n--- ESTADO FINAL ---")
    print(tierra)
    print(luna)
    print(sat_gps1)
    print(cohete_sls)
    print(f"   > {cohete_sls.propulsion}")
