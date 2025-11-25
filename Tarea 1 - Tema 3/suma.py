# suma.py
try:
    num1 = float(input("Introduce el primer número: "))
    num2 = float(input("Introduce el segundo número: "))
    resultado = num1 + num2
    print(f"La suma es: {resultado}")
except ValueError:
    print("Error: Por favor introduce solo números.")
