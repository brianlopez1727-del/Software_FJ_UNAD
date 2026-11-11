"""
Pruebas de validaciones del sistema Software FJ.

Verifica el rechazo de datos incorrectos
en servicios, costos y parámetros.
"""

from servicios import ReservaSala, AlquilerEquipo, Asesoria


def probar_validacion(nombre, operacion):

    try:
        operacion()

        print(f"ERROR: {nombre} - Se aceptaron datos incorrectos.")

    except (ValueError, TypeError) as error:

        print(f"CORRECTO: {nombre} - {error}")


print("\n========================================")
print(" PRUEBAS DE VALIDACIONES - SOFTWARE FJ")
print("========================================")

# PRUEBA 1: PRECIO NEGATIVO

probar_validacion(
    "Precio negativo", lambda: ReservaSala(301, "Sala", "Sala empresarial", -50000, 10)
)

# PRUEBA 2: CAPACIDAD CERO

probar_validacion(
    "Capacidad cero", lambda: ReservaSala(302, "Sala", "Sala empresarial", 50000, 0)
)

# PRUEBA 3: CANTIDAD NEGATIVA DE EQUIPOS

probar_validacion(
    "Cantidad negativa",
    lambda: AlquilerEquipo(303, "Portatiles", "Alquiler de equipos", 30000, -2),
)

# PRUEBA 4: ESPECIALIDAD VACIA

probar_validacion(
    "Especialidad vacia", lambda: Asesoria(304, "Asesoria", "Consultoria", 80000, "")
)

# PRUEBA 5: DURACION CERO

sala = ReservaSala(305, "Sala", "Sala empresarial", 50000, 10)

probar_validacion("Duracion cero", lambda: sala.calcular_costo(0))

# PRUEBA 6: DESCUENTO SUPERIOR AL 100%

probar_validacion("Descuento superior al 100%", lambda: sala.calcular_costo(2, 150))

# PRUEBA 7: IMPUESTO SUPERIOR AL 100%

probar_validacion("Impuesto superior al 100%", lambda: sala.calcular_costo(2, 0, 150))

# PRUEBA 8: DURACION NEGATIVA

probar_validacion("Duracion negativa", lambda: sala.calcular_costo(-3))

print("\n========================================")
print("PRUEBAS DE VALIDACIONES FINALIZADAS")
print("========================================")
