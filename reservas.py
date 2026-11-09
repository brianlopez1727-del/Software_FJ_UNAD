"""
Programa para gestionar las reservas de Software FJ.

Permite crear, confirmar, cancelar y procesar reservas,
aplicando descuentos e IVA del 19%.

Incluye validaciones, encapsulamiento y manejo
de excepciones personalizadas.
"""

import logging
import math

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
)

from clientes import Cliente
from servicios import Servicio


class Reserva:

    IVA = 19

    def __init__(
        self, identificador, cliente, servicio, duracion, descuento=0, impuesto=19
    ):

        # =============================================
        # VALIDAR IDENTIFICADOR
        # =============================================

        if identificador is None or str(identificador).strip() == "":
            raise ParametroFaltanteError(
                "El identificador de la reserva es obligatorio."
            )

        # =============================================
        # VALIDAR CLIENTE
        # =============================================

        if cliente is None:
            raise ClienteNoEncontradoError()

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "El cliente debe ser un objeto de la clase Cliente."
            )

        # =============================================
        # VALIDAR SERVICIO
        # =============================================

        if servicio is None:
            raise ParametroFaltanteError("Debe seleccionar un servicio.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio seleccionado no es valido.")

        # =============================================
        # VALIDAR DURACION
        # =============================================

        self.validar_duracion(duracion)

        # =============================================
        # VALIDAR DESCUENTO E IVA
        # =============================================

        self.validar_porcentaje(descuento, "descuento")
        self.validar_porcentaje(impuesto, "impuesto")

        # =============================================
        # GUARDAR INFORMACION
        # =============================================

        self.__identificador = identificador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion

        self.__descuento = descuento
        self.__impuesto = impuesto

        # =============================================
        # CALCULAR COSTOS
        # =============================================

        try:

            # Calcular el costo base según el servicio.
            # Para alquiler de equipos se utiliza una unidad.

            costo_base = servicio.precio_base * duracion

            self.__detalle_pago = servicio.calcular_detalle_pago(
                costo_base, descuento, impuesto
            )

            self.__costo = self.__detalle_pago["total_pagar"]

        except Exception as error:

            logging.exception(
                "Error al calcular el costo de la reserva %s.", identificador
            )

            raise ReservaInvalidaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

        # =============================================
        # ESTADO INICIAL
        # =============================================

        self.__estado = "Pendiente"

        logging.info("Reserva creada correctamente: %s", identificador)

    # =============================================
    # PROPIEDADES
    # =============================================

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    @property
    def descuento(self):
        return self.__descuento

    @property
    def impuesto(self):
        return self.__impuesto

    @property
    def detalle_pago(self):
        return self.__detalle_pago.copy()

    # =============================================
    # VALIDAR DURACION
    # =============================================

    @staticmethod
    def validar_duracion(duracion):

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):

            raise DatosInvalidosError(
                "La duracion debe ser un numero finito mayor que cero."
            )

        return True

    # =============================================
    # VALIDAR PORCENTAJES
    # =============================================

    @staticmethod
    def validar_porcentaje(valor, nombre):

        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or not 0 <= valor <= 100
        ):

            raise DatosInvalidosError(
                f"El porcentaje de {nombre} debe estar entre 0 y 100."
            )

        return True

    # =============================================
    # CONFIRMAR RESERVA
    # =============================================

    def confirmar(self):

        try:

            if self.__estado != "Pendiente":

                raise OperacionNoPermitidaError(
                    "Solo se pueden confirmar reservas pendientes."
                )

            if not self.__servicio.disponible:

                raise ServicioNoDisponibleError("El servicio no esta disponible.")

            self.__estado = "Confirmada"

        except Exception:

            logging.exception("Error al confirmar la reserva %s.", self.__identificador)

            raise

        else:

            logging.info("Reserva confirmada: %s", self.__identificador)

            return f"Reserva {self.__identificador} " "confirmada correctamente."

        finally:

            logging.info(
                "Finalizo la confirmacion de la reserva %s.", self.__identificador
            )

    # =============================================
    # CANCELAR RESERVA
    # =============================================

    def cancelar(self):

        try:

            if self.__estado not in ("Pendiente", "Confirmada"):

                raise OperacionNoPermitidaError(
                    "La reserva no puede cancelarse en su estado actual."
                )

            self.__estado = "Cancelada"

        except Exception:

            logging.exception("Error al cancelar la reserva %s.", self.__identificador)

            raise

        else:

            logging.info("Reserva cancelada: %s", self.__identificador)

            return f"Reserva {self.__identificador} " "cancelada correctamente."

        finally:

            logging.info(
                "Finalizo la cancelacion de la reserva %s.", self.__identificador
            )

    # =============================================
    # PROCESAR RESERVA
    # =============================================

    def procesar(self):

        try:

            resultado = self.confirmar()

        except ServicioNoDisponibleError as error:

            logging.exception(
                "Servicio no disponible al procesar reserva %s.", self.__identificador
            )

            raise ReservaInvalidaError("No fue posible procesar la reserva.") from error

        except OperacionNoPermitidaError:

            logging.exception(
                "Operacion no permitida al procesar reserva %s.", self.__identificador
            )

            raise

        else:

            logging.info("Procesamiento exitoso: %s", self.__identificador)

            return resultado

        finally:

            logging.info("Procesamiento finalizado: %s", self.__identificador)

    # =============================================
    # MOSTRAR INFORMACION COMPLETA
    # =============================================

    def mostrar_informacion(self):

        detalle = self.__detalle_pago

        return (
            f"\n====================================\n"
            f"       INFORMACION DE RESERVA\n"
            f"====================================\n"
            f"Identificador: {self.__identificador}\n"
            f"Cliente: {self.__cliente.nombre} "
            f"{self.__cliente.apellido}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duracion: {self.__duracion} horas\n"
            f"------------------------------------\n"
            f"Costo base: ${detalle['costo_base']:,.2f}\n"
            f"Descuento: {detalle['descuento_porcentaje']}%\n"
            f"Valor descuento: ${detalle['valor_descuento']:,.2f}\n"
            f"Subtotal: ${detalle['subtotal']:,.2f}\n"
            f"IVA: {detalle['impuesto_porcentaje']}%\n"
            f"Valor IVA: ${detalle['valor_impuesto']:,.2f}\n"
            f"------------------------------------\n"
            f"TOTAL A PAGAR: ${detalle['total_pagar']:,.2f}\n"
            f"Estado: {self.__estado}\n"
            f"===================================="
        )

    # =============================================
    # REPRESENTACION DEL OBJETO
    # =============================================

    def __str__(self):

        return self.mostrar_informacion()


"""
Programa para gestionar las reservas de Software FJ.

Permite crear, confirmar, cancelar y procesar reservas,
aplicando descuentos e IVA del 19%.

Incluye validaciones, encapsulamiento y manejo
de excepciones personalizadas.
"""

import logging
import math

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
)

from clientes import Cliente
from servicios import Servicio, AlquilerEquipo


class Reserva:

    IVA = 19

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion,
        descuento=0,
        impuesto=19,
        cantidad=1,
    ):

        # =============================================
        # VALIDAR IDENTIFICADOR
        # =============================================

        if identificador is None or str(identificador).strip() == "":
            raise ParametroFaltanteError(
                "El identificador de la reserva es obligatorio."
            )

        # =============================================
        # VALIDAR CLIENTE
        # =============================================

        if cliente is None:
            raise ClienteNoEncontradoError()

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError(
                "El cliente debe ser un objeto de la clase Cliente."
            )

        # =============================================
        # VALIDAR SERVICIO
        # =============================================

        if servicio is None:
            raise ParametroFaltanteError("Debe seleccionar un servicio.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio seleccionado no es valido.")

        # =============================================
        # VALIDAR DURACION
        # =============================================

        self.validar_duracion(duracion)

        # =============================================
        # VALIDAR DESCUENTO E IVA
        # =============================================

        self.validar_porcentaje(descuento, "descuento")
        self.validar_porcentaje(impuesto, "impuesto")

        # =============================================
        # VALIDAR CANTIDAD
        # =============================================

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatosInvalidosError(
                "La cantidad debe ser un numero entero mayor que cero."
            )

        if isinstance(servicio, AlquilerEquipo):

            if cantidad > servicio.cantidad_disponible:
                raise ServicioNoDisponibleError(
                    "No hay suficientes equipos disponibles."
                )

        # =============================================
        # GUARDAR INFORMACION
        # =============================================

        self.__identificador = identificador
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion

        self.__descuento = descuento
        self.__impuesto = impuesto
        self.__cantidad = cantidad

        # =============================================
        # CALCULAR COSTOS
        # =============================================

        try:

            costo_base = servicio.precio_base * duracion

            # Si es alquiler de equipos, multiplicar
            # por la cantidad solicitada.

            if isinstance(servicio, AlquilerEquipo):
                costo_base *= cantidad

            self.__detalle_pago = servicio.calcular_detalle_pago(
                costo_base, descuento, impuesto
            )

            self.__costo = self.__detalle_pago["total"]

        except Exception as error:

            logging.exception(
                "Error al calcular el costo de la reserva %s.", identificador
            )

            raise ReservaInvalidaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

        # =============================================
        # ESTADO INICIAL
        # =============================================

        self.__estado = "Pendiente"

        logging.info("Reserva creada correctamente: %s", identificador)

    # =============================================
    # PROPIEDADES
    # =============================================

    @property
    def identificador(self):
        return self.__identificador

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    @property
    def descuento(self):
        return self.__descuento

    @property
    def impuesto(self):
        return self.__impuesto

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def detalle_pago(self):
        return self.__detalle_pago.copy()

    # =============================================
    # VALIDAR DURACION
    # =============================================

    @staticmethod
    def validar_duracion(duracion):

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):

            raise DatosInvalidosError(
                "La duracion debe ser un numero finito mayor que cero."
            )

        return True

    # =============================================
    # VALIDAR PORCENTAJES
    # =============================================

    @staticmethod
    def validar_porcentaje(valor, nombre):

        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or not 0 <= valor <= 100
        ):

            raise DatosInvalidosError(
                f"El porcentaje de {nombre} debe estar entre 0 y 100."
            )

        return True

    # =============================================
    # CONFIRMAR RESERVA
    # =============================================

    def confirmar(self):

        try:

            if self.__estado != "Pendiente":

                raise OperacionNoPermitidaError(
                    "Solo se pueden confirmar reservas pendientes."
                )

            if not self.__servicio.disponible:

                raise ServicioNoDisponibleError("El servicio no esta disponible.")

            self.__estado = "Confirmada"

        except Exception:

            logging.exception("Error al confirmar la reserva %s.", self.__identificador)

            raise

        else:

            logging.info("Reserva confirmada: %s", self.__identificador)

            return f"Reserva {self.__identificador} " "confirmada correctamente."

        finally:

            logging.info(
                "Finalizo la confirmacion de la reserva %s.", self.__identificador
            )

    # =============================================
    # CANCELAR RESERVA
    # =============================================

    def cancelar(self):

        try:

            if self.__estado not in ("Pendiente", "Confirmada"):

                raise OperacionNoPermitidaError(
                    "La reserva no puede cancelarse en su estado actual."
                )

            self.__estado = "Cancelada"

        except Exception:

            logging.exception("Error al cancelar la reserva %s.", self.__identificador)

            raise

        else:

            logging.info("Reserva cancelada: %s", self.__identificador)

            return f"Reserva {self.__identificador} " "cancelada correctamente."

        finally:

            logging.info(
                "Finalizo la cancelacion de la reserva %s.", self.__identificador
            )

    # =============================================
    # PROCESAR RESERVA
    # =============================================

    def procesar(self):

        try:

            resultado = self.confirmar()

        except ServicioNoDisponibleError as error:

            logging.exception(
                "Servicio no disponible al procesar reserva %s.", self.__identificador
            )

            raise ReservaInvalidaError("No fue posible procesar la reserva.") from error

        except OperacionNoPermitidaError:

            logging.exception(
                "Operacion no permitida al procesar reserva %s.", self.__identificador
            )

            raise

        else:

            logging.info("Procesamiento exitoso: %s", self.__identificador)

            return resultado

        finally:

            logging.info("Procesamiento finalizado: %s", self.__identificador)

    # =============================================
    # MOSTRAR INFORMACION COMPLETA
    # =============================================

    def mostrar_informacion(self):

        detalle = self.__detalle_pago

        informacion = (
            f"\n====================================\n"
            f"       INFORMACION DE RESERVA\n"
            f"====================================\n"
            f"Identificador: {self.__identificador}\n"
            f"Cliente: {self.__cliente.nombre} "
            f"{self.__cliente.apellido}\n"
            f"Servicio: {self.__servicio.nombre}\n"
            f"Duracion: {self.__duracion} horas\n"
        )

        if isinstance(self.__servicio, AlquilerEquipo):

            informacion += f"Cantidad de equipos: {self.__cantidad}\n"

        informacion += (
            f"------------------------------------\n"
            f"Costo base: ${detalle['costo_base']:,.2f}\n"
            f"Descuento: {self.__descuento}%\n"
            f"Valor descuento: "
            f"${detalle['valor_descuento']:,.2f}\n"
            f"Subtotal: ${detalle['subtotal']:,.2f}\n"
            f"IVA: {self.__impuesto}%\n"
            f"Valor IVA: ${detalle['valor_impuesto']:,.2f}\n"
            f"------------------------------------\n"
            f"TOTAL A PAGAR: ${detalle['total']:,.2f}\n"
            f"Estado: {self.__estado}\n"
            f"===================================="
        )

        return informacion

    # =============================================
    # REPRESENTACION DEL OBJETO
    # =============================================

    def __str__(self):

        return self.mostrar_informacion()
