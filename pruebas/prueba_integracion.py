"""
Pruebas de integracion del Sistema Software FJ.

Verifica la comunicacion entre clientes, servicios
y reservas, incluyendo el control de errores.
"""

# IMPORTA LAS CLASES PRINCIPALES

from clientes import Cliente
from servicios import ReservaSala
from sistema import SistemaFJ

# IMPORTA LAS EXCEPCIONES PERSONALIZADAS

from excepciones import (
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)

print("\n========================================")
print(" PRUEBAS DE INTEGRACION - SOFTWARE FJ")
print("========================================")

# CREA UNA INSTANCIA DEL SISTEMA

sistema = SistemaFJ()

# PRUEBA 1: REGISTRO DE CLIENTE

print("\nPRUEBA 1: REGISTRO DE CLIENTE")

cliente = Cliente(901, "Brian", "Lopez", "12345678", "3001234567", "brian@gmail.com")

print(sistema.registrar_cliente(cliente))

# PRUEBA 2: REGISTRO DE SERVICIO

print("\nPRUEBA 2: REGISTRO DE SERVICIO")

sala = ReservaSala(
    901, "Sala Ejecutiva", "Sala para reuniones empresariales", 50000, 10
)

print(sistema.registrar_servicio(sala))

# PRUEBA 3: CREACION DE RESERVA

print("\nPRUEBA 3: CREACION DE RESERVA")

reserva = sistema.crear_reserva(901, 901, 901, 2)

print(reserva.mostrar_informacion())

# PRUEBA 4: CONFIRMACION DE RESERVA

print("\nPRUEBA 4: CONFIRMACION DE RESERVA")

print(sistema.confirmar_reserva(901))

# PRUEBA 5: CONTROL DE CLIENTE INEXISTENTE

print("\nPRUEBA 5: CLIENTE INEXISTENTE")

try:

    sistema.crear_reserva(902, 999, 901, 2)

except ClienteNoEncontradoError as error:

    print("CORRECTO: Cliente inexistente controlado:", error)

# PRUEBA 6: CONTROL DE SERVICIO INEXISTENTE

print("\nPRUEBA 6: SERVICIO INEXISTENTE")

try:

    sistema.crear_reserva(903, 901, 999, 2)

except ServicioNoDisponibleError as error:

    print("CORRECTO: Servicio inexistente controlado:", error)

# PRUEBA 7: CONTROL DE RESERVA DUPLICADA

print("\nPRUEBA 7: RESERVA DUPLICADA")

try:

    sistema.crear_reserva(901, 901, 901, 2)

except OperacionNoPermitidaError as error:

    print("CORRECTO: Reserva duplicada controlada:", error)

# PRUEBA 8: CONSULTA DEL RESUMEN GENERAL

print("\nPRUEBA 8: RESUMEN DEL SISTEMA")

print(sistema.mostrar_resumen())

# FINALIZA LAS PRUEBAS

print("\n========================================")
print("PRUEBAS DE INTEGRACION FINALIZADAS")
print("========================================")

print(sistema.cerrar_sistema())
