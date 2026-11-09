"""
PROGRAMA PRINCIPAL SOFTWARE FJ.

Permite ejecutar el sistema desde la terminal
o iniciar la interfaz grafica con CustomTkinter.

Incluye:
- Configuracion de logs.
- Registro de clientes.
- Registro de servicios.
- Creacion de reservas.
- Confirmacion y cancelacion.
- Pruebas de excepciones.
- Manejo de errores.
"""

import sys
import logging

from pathlib import Path

# =============================================
# CONFIGURACION GENERAL
# =============================================

BASE_DIR = Path(__file__).resolve().parent

CARPETA_LOGS = BASE_DIR / "logs"

CARPETA_LOGS.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=CARPETA_LOGS / "software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

# =============================================
# IMPORTACIONES
# =============================================

from clientes import Cliente

from servicios import ReservaSala, AlquilerEquipo, Asesoria

from sistema import SistemaFJ

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    SoftwareFJError,
)

# =============================================
# REGISTRAR ERRORES
# =============================================


def registrar_error(mensaje, error):

    logging.error("%s: %s", mensaje, error)


# =============================================
# PRUEBAS DE EXCEPCIONES
# =============================================


def probar_excepciones():

    print("\n" + "=" * 55)
    print("PRUEBAS DE EXCEPCIONES")
    print("=" * 55)

    # PRUEBA 1

    print("\nPRUEBA 1: TRY / EXCEPT")

    try:

        int("Software FJ")

    except ValueError as error:

        print("ERROR CONTROLADO:", error)

        registrar_error("Error de conversion", error)

    # PRUEBA 2

    print("\nPRUEBA 2: TRY / EXCEPT / ELSE")

    try:

        numero = int("150")

    except ValueError as error:

        print("ERROR:", error)

    else:

        print("Conversion realizada correctamente:", numero)

    # PRUEBA 3

    print("\nPRUEBA 3: TRY / EXCEPT / FINALLY")

    try:

        resultado = 100 / 0

    except ZeroDivisionError as error:

        print("ERROR CONTROLADO:", error)

        registrar_error("Division entre cero", error)

    finally:

        print("El bloque FINALLY se ejecuto correctamente.")

    # PRUEBA 4

    print("\nPRUEBA 4: ENCADENAMIENTO DE EXCEPCIONES")

    try:

        try:

            int("Dato incorrecto")

        except ValueError as error:

            raise DatosInvalidosError(
                "No fue posible procesar el dato ingresado."
            ) from error

    except DatosInvalidosError as error:

        print("EXCEPCION PERSONALIZADA:", error)

        print("EXCEPCION ORIGINAL:", error.__cause__)

    print("\nPRUEBAS FINALIZADAS.")


# =============================================
# EJECUTAR SISTEMA
# =============================================


def ejecutar_programa():

    sistema = SistemaFJ()

    print("\n" + "=" * 55)
    print(" SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("=" * 55)

    try:

        # =====================================
        # OPERACION 1: REGISTRAR CLIENTE
        # =====================================

        print("\nOPERACION 1: REGISTRO DE CLIENTE")

        cliente = Cliente(
            1, "Brian", "Lopez", "12345678", "3001234567", "brian@gmail.com"
        )

        print(sistema.registrar_cliente(cliente))

        # =====================================
        # OPERACION 2: CLIENTE INVALIDO
        # =====================================

        print("\nOPERACION 2: CLIENTE INVALIDO")

        try:

            Cliente(2, "Carlos", "Perez", "87654321", "3101234567", "correo_incorrecto")

        except (DatosInvalidosError, ValueError) as error:

            print("ERROR CONTROLADO:", error)

            registrar_error("Cliente invalido", error)

        # =====================================
        # OPERACION 3: REGISTRAR SALA
        # =====================================

        print("\nOPERACION 3: REGISTRO DE SALA")

        sala = ReservaSala(
            101, "Sala Ejecutiva", "Sala para reuniones empresariales", 50000, 10
        )

        print(sistema.registrar_servicio(sala))

        # =====================================
        # OPERACION 4: REGISTRAR EQUIPO
        # =====================================

        print("\nOPERACION 4: REGISTRO DE EQUIPO")

        equipo = AlquilerEquipo(
            102, "Alquiler de portatil", "Equipo tecnologico para trabajo", 30000, 2
        )

        print(sistema.registrar_servicio(equipo))

        # =====================================
        # OPERACION 5: REGISTRAR ASESORIA
        # =====================================

        print("\nOPERACION 5: REGISTRO DE ASESORIA")

        asesoria = Asesoria(
            103,
            "Asesoria tecnologica",
            "Consultoria especializada",
            80000,
            "Desarrollo de software",
        )

        print(sistema.registrar_servicio(asesoria))

        # =====================================
        # OPERACION 6: CREAR RESERVA
        # =====================================

        print("\nOPERACION 6: CREACION DE RESERVA")

        reserva = sistema.crear_reserva(201, 1, 101, 2, descuento=10, impuesto=19)

        print(reserva.mostrar_informacion())

        # =====================================
        # OPERACION 7: CLIENTE INEXISTENTE
        # =====================================

        print("\nOPERACION 7: CLIENTE INEXISTENTE")

        try:

            sistema.crear_reserva(202, 999, 101, 2)

        except ClienteNoEncontradoError as error:

            print("ERROR CONTROLADO:", error)

            registrar_error("Cliente inexistente", error)

        # =====================================
        # OPERACION 8: CONFIRMAR RESERVA
        # =====================================

        print("\nOPERACION 8: CONFIRMAR RESERVA")

        print(sistema.confirmar_reserva(201))

        # =====================================
        # OPERACION 9: CANCELAR RESERVA
        # =====================================

        print("\nOPERACION 9: CANCELAR RESERVA")

        print(sistema.cancelar_reserva(201))

        # =====================================
        # OPERACION 10: OPERACION NO PERMITIDA
        # =====================================

        print("\nOPERACION 10: OPERACION NO PERMITIDA")

        try:

            sistema.confirmar_reserva(201)

        except OperacionNoPermitidaError as error:

            print("ERROR CONTROLADO:", error)

            registrar_error("Operacion no permitida", error)

        # =====================================
        # OPERACION 11: EQUIPO NO DISPONIBLE
        # =====================================

        print("\nOPERACION 11: EQUIPO NO DISPONIBLE")

        try:

            sistema.crear_reserva(203, 1, 102, 2, cantidad=5)

        except ServicioNoDisponibleError as error:

            print("ERROR CONTROLADO:", error)

            registrar_error("Equipos insuficientes", error)

        # =====================================
        # OPERACION 12: DURACION INVALIDA
        # =====================================

        print("\nOPERACION 12: DURACION INVALIDA")

        try:

            sala.calcular_costo(0)

        except (DatosInvalidosError, ValueError) as error:

            print("ERROR CONTROLADO:", error)

            registrar_error("Duracion invalida", error)

        # =====================================
        # PRUEBAS AVANZADAS
        # =====================================

        probar_excepciones()

        # =====================================
        # RESUMEN GENERAL
        # =====================================

        print("\n" + "=" * 55)

        print(sistema.mostrar_resumen())

        print("=" * 55)

    except SoftwareFJError as error:

        print("\nERROR CONTROLADO DEL SISTEMA:", error)

        logging.exception("Error personalizado durante la ejecucion.")

    except Exception as error:

        print("\nERROR INESPERADO:", error)

        logging.exception("Error inesperado durante la ejecucion.")

    finally:

        print("\nFINALIZANDO SOFTWARE FJ")

        print(sistema.cerrar_sistema())


# =============================================
# INICIAR INTERFAZ GRAFICA
# =============================================


def iniciar_interfaz():

    try:

        from interfaz.ventana_principal import VentanaPrincipal

        aplicacion = VentanaPrincipal()

        aplicacion.mainloop()

    except ImportError as error:

        logging.exception("No fue posible importar la interfaz grafica.")

        print("No se pudo cargar la interfaz:", error)

    except Exception as error:

        logging.exception("Error al iniciar la interfaz grafica.")

        print("No fue posible iniciar Software FJ:", error)


# =============================================
# PUNTO DE ENTRADA
# =============================================

if __name__ == "__main__":

    if "--pruebas" in sys.argv:

        ejecutar_programa()

    else:

        iniciar_interfaz()
