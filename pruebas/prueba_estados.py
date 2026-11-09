from clientes import Cliente
from servicios import ReservaSala
from sistema import SistemaFJ
from excepciones import OperacionNoPermitidaError

# CREA EL SISTEMA
sistema = SistemaFJ()

# REGISTRA UN CLIENTE
cliente = Cliente(1, "Brian", "Lopez", "12345678", "3001234567", "brian@gmail.com")

sistema.registrar_cliente(cliente)

# REGISTRA UN SERVICIO
servicio = ReservaSala(101, "Sala Ejecutiva", "Sala empresarial", 50000, 10)

sistema.registrar_servicio(servicio)

# CREA UNA RESERVA
reserva = sistema.crear_reserva(201, 1, 101, 2)

# CANCELA LA RESERVA
print("\nPRUEBA 1: CANCELAR RESERVA")
print(reserva.cancelar())
print("Estado:", reserva.estado)

# INTENTA CONFIRMAR UNA RESERVA CANCELADA
print("\nPRUEBA 2: CONFIRMAR RESERVA CANCELADA")

try:
    reserva.confirmar()

except OperacionNoPermitidaError as error:
    print("CONFIRMACION BLOQUEADA:", error)

# INTENTA CANCELARLA NUEVAMENTE
print("\nPRUEBA 3: CANCELAR DOS VECES")

try:
    reserva.cancelar()

except OperacionNoPermitidaError as error:
    print("SEGUNDA CANCELACION BLOQUEADA:", error)

print("\nPRUEBAS FINALIZADAS.")
