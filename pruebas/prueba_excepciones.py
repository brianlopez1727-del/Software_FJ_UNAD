"""
Pruebas de excepciones personalizadas del sistema Software FJ.

Verifica el funcionamiento de las excepciones,
el encadenamiento de errores y su captura controlada.
"""

# IMPORTA LAS EXCEPCIONES PERSONALIZADAS

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
)

# IMPORTA LAS CLASES PRINCIPALES

from clientes import Cliente
from servicios import ReservaSala
from sistema import SistemaFJ

print("\n========================================")
print(" PRUEBAS DE EXCEPCIONES - SOFTWARE FJ")
print("========================================")

# PRUEBA 1: DATOS INVALIDOS

print("\nPRUEBA 1: DATOS INVALIDOS")

try:

    ReservaSala(501, "Sala", "Sala empresarial", -1000, 10)

except DatosInvalidosError as error:

    print("CORRECTO: DatosInvalidosError:", error)


# PRUEBA 2: CLIENTE INEXISTENTE

print("\nPRUEBA 2: CLIENTE INEXISTENTE")

sistema = SistemaFJ()

try:

    sistema.buscar_cliente(999)

except ClienteNoEncontradoError as error:

    print("CORRECTO: ClienteNoEncontradoError:", error)


# PRUEBA 3: SERVICIO INEXISTENTE

print("\nPRUEBA 3: SERVICIO INEXISTENTE")

try:

    sistema.buscar_servicio(999)

except ServicioNoDisponibleError as error:

    print("CORRECTO: ServicioNoDisponibleError:", error)


# PRUEBA 4: PARAMETRO FALTANTE

print("\nPRUEBA 4: PARAMETRO FALTANTE")

try:

    from reservas import Reserva

    Reserva(None, None, None, 2)

except ParametroFaltanteError as error:

    print("CORRECTO: ParametroFaltanteError:", error)


# PRUEBA 5: RESERVA INEXISTENTE

print("\nPRUEBA 5: RESERVA INEXISTENTE")

try:

    sistema.buscar_reserva(999)

except ReservaInvalidaError as error:

    print("CORRECTO: ReservaInvalidaError:", error)


# PRUEBA 6: OPERACION NO PERMITIDA

print("\nPRUEBA 6: OPERACION NO PERMITIDA")

cliente = Cliente(501, "Brian", "Lopez", "12345678", "3001234567", "brian@gmail.com")

sala = ReservaSala(502, "Sala Ejecutiva", "Sala empresarial", 50000, 10)

sistema.registrar_cliente(cliente)
sistema.registrar_servicio(sala)

reserva = sistema.crear_reserva(503, 501, 502, 2)

reserva.cancelar()

try:

    reserva.confirmar()

except OperacionNoPermitidaError as error:

    print("CORRECTO: OperacionNoPermitidaError:", error)


# PRUEBA 7: ENCADENAMIENTO DE EXCEPCIONES

print("\nPRUEBA 7: ENCADENAMIENTO DE EXCEPCIONES")

try:

    try:

        int("Software FJ")

    except ValueError as error:

        raise DatosInvalidosError("No se pudo convertir el dato ingresado.") from error

except DatosInvalidosError as error:

    print("CORRECTO: Excepcion personalizada:", error)
    print("Excepcion original:", type(error.__cause__).__name__)


# FINALIZA LAS PRUEBAS

print("\n========================================")
print("PRUEBAS DE EXCEPCIONES FINALIZADAS")
print("========================================")

print(sistema.cerrar_sistema())
