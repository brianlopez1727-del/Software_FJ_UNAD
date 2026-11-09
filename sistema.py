"""
MODULO PRINCIPAL DE GESTION DE SOFTWARE FJ.

Administra clientes, servicios y reservas.

Incluye:
- Programacion orientada a objetos.
- Encapsulamiento.
- Validaciones.
- Excepciones personalizadas.
- Gestion de reservas.
- Control de disponibilidad.
- Registro de operaciones.
"""

import logging

from clientes import Cliente
from servicios import Servicio, AlquilerEquipo
from reservas import Reserva

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
)


class SistemaFJ:

    def __init__(self):

        self.__clientes = {}
        self.__servicios = {}
        self.__reservas = {}

        self.__activo = True

        logging.info("Sistema Software FJ iniciado correctamente.")

    # =============================================
    # VALIDAR ESTADO DEL SISTEMA
    # =============================================

    def validar_sistema(self):

        if not self.__activo:
            raise OperacionNoPermitidaError("El sistema se encuentra cerrado.")

        return True

    # =============================================
    # REGISTRAR CLIENTE
    # =============================================

    def registrar_cliente(self, cliente):

        self.validar_sistema()

        if cliente is None:
            raise ParametroFaltanteError("Debe proporcionar un cliente.")

        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El objeto debe pertenecer a la clase Cliente.")

        identificador = cliente.identificador

        if identificador in self.__clientes:
            raise OperacionNoPermitidaError(
                "Ya existe un cliente con ese identificador."
            )

        self.__clientes[identificador] = cliente

        logging.info("Cliente registrado: %s", identificador)

        return f"Cliente {cliente.nombre} registrado correctamente."

    # =============================================
    # BUSCAR CLIENTE
    # =============================================

    def buscar_cliente(self, identificador):

        self.validar_sistema()

        cliente = self.__clientes.get(identificador)

        if cliente is None:
            raise ClienteNoEncontradoError(
                "No existe un cliente con ese identificador."
            )

        return cliente

    # =============================================
    # REGISTRAR SERVICIO
    # =============================================

    def registrar_servicio(self, servicio):

        self.validar_sistema()

        if servicio is None:
            raise ParametroFaltanteError("Debe proporcionar un servicio.")

        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El objeto debe pertenecer a la clase Servicio.")

        identificador = servicio.identificador

        if identificador in self.__servicios:
            raise OperacionNoPermitidaError(
                "Ya existe un servicio con ese identificador."
            )

        self.__servicios[identificador] = servicio

        logging.info("Servicio registrado: %s", identificador)

        return f"Servicio {servicio.nombre} registrado correctamente."

    # =============================================
    # BUSCAR SERVICIO
    # =============================================

    def buscar_servicio(self, identificador):

        self.validar_sistema()

        servicio = self.__servicios.get(identificador)

        if servicio is None:
            raise ServicioNoDisponibleError("No se encontro el servicio solicitado.")

        return servicio

    # =============================================
    # CREAR RESERVA
    # =============================================

    def crear_reserva(
        self,
        identificador,
        id_cliente,
        id_servicio,
        duracion,
        descuento=0,
        impuesto=19,
        cantidad=1,
    ):

        self.validar_sistema()

        if identificador is None:
            raise ParametroFaltanteError(
                "El identificador de la reserva es obligatorio."
            )

        if identificador in self.__reservas:
            raise OperacionNoPermitidaError(
                "Ya existe una reserva con ese identificador."
            )

        cliente = self.buscar_cliente(id_cliente)

        servicio = self.buscar_servicio(id_servicio)

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no esta disponible."
            )

        reserva = Reserva(
            identificador, cliente, servicio, duracion, descuento, impuesto, cantidad
        )

        self.__reservas[identificador] = reserva

        logging.info("Reserva creada: %s", identificador)

        return reserva

    # =============================================
    # BUSCAR RESERVA
    # =============================================

    def buscar_reserva(self, identificador):

        self.validar_sistema()

        reserva = self.__reservas.get(identificador)

        if reserva is None:
            raise ReservaInvalidaError("No existe una reserva con ese identificador.")

        return reserva

    # =============================================
    # CONFIRMAR RESERVA
    # =============================================

    def confirmar_reserva(self, identificador):

        self.validar_sistema()

        reserva = self.buscar_reserva(identificador)

        resultado = reserva.confirmar()

        logging.info("Reserva confirmada: %s", identificador)

        return resultado

    # =============================================
    # CANCELAR RESERVA
    # =============================================

    def cancelar_reserva(self, identificador):

        self.validar_sistema()

        reserva = self.buscar_reserva(identificador)

        resultado = reserva.cancelar()

        logging.info("Reserva cancelada: %s", identificador)

        return resultado

    # =============================================
    # PROCESAR RESERVA
    # =============================================

    def procesar_reserva(self, identificador):

        self.validar_sistema()

        reserva = self.buscar_reserva(identificador)

        resultado = reserva.procesar()

        logging.info("Reserva procesada: %s", identificador)

        return resultado

    # =============================================
    # LISTAR CLIENTES
    # =============================================

    def listar_clientes(self):

        self.validar_sistema()

        return tuple(self.__clientes.values())

    # =============================================
    # LISTAR SERVICIOS
    # =============================================

    def listar_servicios(self):

        self.validar_sistema()

        return tuple(self.__servicios.values())

    # =============================================
    # LISTAR RESERVAS
    # =============================================

    def listar_reservas(self):

        self.validar_sistema()

        return tuple(self.__reservas.values())

    # =============================================
    # MOSTRAR RESUMEN
    # =============================================

    def mostrar_resumen(self):

        self.validar_sistema()

        total_clientes = len(self.__clientes)
        total_servicios = len(self.__servicios)
        total_reservas = len(self.__reservas)

        pendientes = sum(
            reserva.estado == "Pendiente" for reserva in self.__reservas.values()
        )

        confirmadas = sum(
            reserva.estado == "Confirmada" for reserva in self.__reservas.values()
        )

        canceladas = sum(
            reserva.estado == "Cancelada" for reserva in self.__reservas.values()
        )

        ingresos = sum(
            reserva.costo
            for reserva in self.__reservas.values()
            if reserva.estado == "Confirmada"
        )

        return (
            "\n========================================\n"
            "       RESUMEN GENERAL SOFTWARE FJ\n"
            "========================================\n"
            f"Clientes registrados: {total_clientes}\n"
            f"Servicios registrados: {total_servicios}\n"
            f"Total de reservas: {total_reservas}\n"
            "----------------------------------------\n"
            f"Reservas pendientes: {pendientes}\n"
            f"Reservas confirmadas: {confirmadas}\n"
            f"Reservas canceladas: {canceladas}\n"
            "----------------------------------------\n"
            f"Ingresos confirmados: ${ingresos:,.2f}\n"
            "========================================"
        )

    # =============================================
    # CERRAR SISTEMA
    # =============================================

    def cerrar_sistema(self):

        if not self.__activo:
            return "El sistema ya se encuentra cerrado."

        self.__activo = False

        logging.info("Sistema Software FJ cerrado correctamente.")

        return "Sistema Software FJ finalizado correctamente."

    # =============================================
    # PROPIEDAD ESTADO DEL SISTEMA
    # =============================================

    @property
    def activo(self):

        return self.__activo
