import sys

def celsius_a_fahrenheit(celsius):
    """Convierte grados Celsius a Fahrenheit."""
    return (celsius * 9/5) + 32

def mostrar_tabla_multiplicar(numero):
    """Imprime la tabla de multiplicar del 1 al 10."""
    print(f"\n--- Tabla del {numero} ---")
    for i in range(1, 11):
        print(f"{numero} x {i} = {numero * i}")
    print("----------------------\n")

def menu_principal():
    while True:
        print("MENÚ PRINCIPAL")
        print("1) Conversión de temperatura (Celsius -> Fahrenheit)")
        print("2) Tabla de multiplicar")
        print("3) Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                entrada = float(input("Introduzca los grados Celsius: "))
                resultado = celsius_a_fahrenheit(entrada)
                print(f"\nResultado: {entrada}°C son {resultado:.2f}°F\n")
            except ValueError:
                print("\nError: Por favor, introduzca un número decimal válido.\n")

        elif opcion == '2':
            try:
                entrada = int(input("Introduzca un número entero: "))
                mostrar_tabla_multiplicar(entrada)
            except ValueError:
                print("\nError: Por favor, introduzca un número entero válido.\n")

        elif opcion == '3':
            print("Saliendo del programa...")
            break

        else:
            print("\nOpción no válida. Intente de nuevo.\n")

if __name__ == "__main__":
    menu_principal()
