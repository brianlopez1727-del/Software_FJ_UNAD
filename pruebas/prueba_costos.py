from servicios import ReservaSala, AlquilerEquipo, Asesoria

# CREA LOS SERVICIOS

sala = ReservaSala(101, "Sala Ejecutiva", "Sala empresarial", 50000, 10)

equipo = AlquilerEquipo(
    102, "Alquiler de portatil", "Equipo tecnologico", 30000, "Portatil", 2
)

asesoria = Asesoria(
    103,
    "Asesoria tecnologica",
    "Consultoria especializada",
    80000,
    "Desarrollo de software",
)

# PRUEBA 1: COSTO DE RESERVA DE SALA

print("\nPRUEBA 1: RESERVA DE SALA")
print("Costo esperado: $100000.00")
print("Costo obtenido:", sala.calcular_costo(2))

# PRUEBA 2: COSTO DE ALQUILER DE EQUIPOS

print("\nPRUEBA 2: ALQUILER DE EQUIPOS")
print("Costo esperado: $120000.00")
print("Costo obtenido:", equipo.calcular_costo(2))

# PRUEBA 3: COSTO DE ASESORIA

print("\nPRUEBA 3: ASESORIA")
print("Costo esperado: $160000.00")
print("Costo obtenido:", asesoria.calcular_costo(2))

# PRUEBA 4: DESCUENTO DEL 10%

print("\nPRUEBA 4: DESCUENTO DEL 10%")
print("Costo esperado: $90000.00")
print("Costo obtenido:", sala.calcular_costo(2, descuento=10))

# PRUEBA 5: IMPUESTO DEL 19%

print("\nPRUEBA 5: IMPUESTO DEL 19%")
print("Costo esperado: $119000.00")
print("Costo obtenido:", sala.calcular_costo(2, impuesto=19))

# PRUEBA 6: DESCUENTO E IMPUESTO

print("\nPRUEBA 6: DESCUENTO E IMPUESTO")
print("Costo esperado: $107100.00")
print("Costo obtenido:", sala.calcular_costo(2, descuento=10, impuesto=19))

print("\nPRUEBAS DE COSTOS FINALIZADAS.")
