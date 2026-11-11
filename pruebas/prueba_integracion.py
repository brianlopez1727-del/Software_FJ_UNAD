"""
PRUEBAS DE INTEGRACION DEL SISTEMA SOFTWARE FJ.

Verifica la comunicacion entre los modulos de clientes,
servicios, reservas y sistema.

Incluye pruebas de operaciones exitosas, errores controlados,
validaciones, cambios de estado y continuidad del sistema.

Se realizan diez operaciones para verificar el funcionamiento
integral de la aplicacion.
"""

# =====================================================
# IMPORTAR MODULOS
# =====================================================

from clientes import Cliente
from servicios import ReservaSala
from sistema import SistemaFJ

from excepciones import (
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)

# =====================================================
# FUNCION PARA MOSTRAR RESULTADOS
# =====================================================


def mostrar_resultado(numero, descripcion, resultado):

    print("\n" + "=" * 55)
    print(f"PRUEBA {numero}: {descripcion}")
    print("=" * 55)

    print(resultado)


# =====================================================
# INICIAR PRUEBAS DE INTEGRACION
# =====================================================

print("\n")
print("*" * 55)
print("       PRUEBAS DE INTEGRACION - SOFTWARE FJ")
print("*" * 55)

# Crear instancia del sistema.

sistema = SistemaFJ()


# =====================================================
# PRUEBA 1: REGISTRO DE CLIENTE
# =====================================================

print("\nPRUEBA 1: REGISTRO DE CLIENTE")

cliente = Cliente(901, "Brian", "Lopez", "12345678", "3001234567", "brian@gmail.com")

resultado = sistema.registrar_cliente(cliente)

print(resultado)


# =====================================================
# PRUEBA 2: REGISTRO DE SERVICIO
# =====================================================

print("\nPRUEBA 2: REGISTRO DE SERVICIO")

sala = ReservaSala(
    901, "Sala Ejecutiva", "Sala para reuniones empresariales", 50000, 10
)

resultado = sistema.registrar_servicio(sala)

print(resultado)


# =====================================================
# PRUEBA 3: CREACION DE RESERVA
# =====================================================

print("\nPRUEBA 3: CREACION DE RESERVA")

reserva = sistema.crear_reserva(901, 901, 901, 2)

print(reserva.mostrar_informacion())

print("Estado inicial:", reserva.estado)


# =====================================================
# PRUEBA 4: CONFIRMACION DE RESERVA
# =====================================================

print("\nPRUEBA 4: CONFIRMACION DE RESERVA")

resultado = sistema.confirmar_reserva(901)

print(resultado)

print("Estado actual:", reserva.estado)


# =====================================================
# PRUEBA 5: CONTROL DE CLIENTE INEXISTENTE
# =====================================================

print("\nPRUEBA 5: CLIENTE INEXISTENTE")

try:

    sistema.crear_reserva(902, 999, 901, 2)

except ClienteNoEncontradoError as error:

    print("CORRECTO: Cliente inexistente controlado.")
    print("Detalle:", error)


# =====================================================
# PRUEBA 6: CONTROL DE SERVICIO INEXISTENTE
# =====================================================

print("\nPRUEBA 6: SERVICIO INEXISTENTE")

try:

    sistema.crear_reserva(903, 901, 999, 2)

except ServicioNoDisponibleError as error:

    print("CORRECTO: Servicio inexistente controlado.")
    print("Detalle:", error)


# =====================================================
# PRUEBA 7: CONTROL DE RESERVA DUPLICADA
# =====================================================

print("\nPRUEBA 7: RESERVA DUPLICADA")

try:

    sistema.crear_reserva(901, 901, 901, 2)

except OperacionNoPermitidaError as error:

    print("CORRECTO: Reserva duplicada controlada.")
    print("Detalle:", error)


# =====================================================
# PRUEBA 8: CONSULTA DEL RESUMEN GENERAL
# =====================================================

print("\nPRUEBA 8: RESUMEN GENERAL DEL SISTEMA")

print(sistema.mostrar_resumen())


# =====================================================
# PRUEBA 9: CANCELACION DE RESERVA
# =====================================================

print("\nPRUEBA 9: CANCELACION DE RESERVA")

resultado = sistema.cancelar_reserva(901)

print(resultado)

reserva_cancelada = sistema.buscar_reserva(901)

if reserva_cancelada.estado == "Cancelada":

    print("CORRECTO: La reserva fue cancelada.")
    print("Estado actual:", reserva_cancelada.estado)

else:

    print("ERROR: No se pudo cancelar correctamente la reserva.")


# =====================================================
# PRUEBA 10: CONFIRMACION DE RESERVA CANCELADA
# =====================================================

print("\nPRUEBA 10: CONFIRMACION DE RESERVA CANCELADA")

try:

    sistema.confirmar_reserva(901)

except OperacionNoPermitidaError as error:

    print("CORRECTO: Se controlo la operacion no permitida.")
    print("Detalle:", error)

else:

    print("ERROR: Se permitio confirmar una reserva cancelada.")


# =====================================================
# VERIFICACION DE CONTINUIDAD DEL SISTEMA
# =====================================================

print("\nVERIFICACION DE CONTINUIDAD DEL SISTEMA")

print("Sistema activo:", sistema.activo)

print("\nRESUMEN FINAL:")

print(sistema.mostrar_resumen())


# =====================================================
# FINALIZAR PRUEBAS
# =====================================================

print("\n")
print("*" * 55)
print("     PRUEBAS DE INTEGRACION FINALIZADAS")
print("*" * 55)

print(sistema.cerrar_sistema())

print("\nEstado final del sistema:", sistema.activo)
