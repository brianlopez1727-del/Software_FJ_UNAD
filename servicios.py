"""
MODULO DE SERVICIOS DE SOFTWARE FJ.

Permite registrar y administrar los servicios de la empresa.

Incluye:
- Clase abstracta Servicio.
- Reserva de salas.
- Alquiler de equipos.
- Asesorias especializadas.
- Polimorfismo.
- Calculo de costos.
- Descuentos e IVA del 19%.
- Validaciones de datos.
"""

import math
import logging

from abc import ABC, abstractmethod

# =====================================================
# CLASE ABSTRACTA SERVICIO
# =====================================================


class Servicio(ABC):

    IVA = 19

    def __init__(
        self, identificador, nombre, descripcion, precio_base, disponible=True
    ):

        # VALIDAR IDENTIFICADOR

        if (
            isinstance(identificador, bool)
            or not isinstance(identificador, int)
            or identificador <= 0
        ):
            raise ValueError("El identificador debe ser un entero mayor que cero.")

        # VALIDAR NOMBRE

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre es obligatorio.")

        # VALIDAR DESCRIPCION

        if not isinstance(descripcion, str) or not descripcion.strip():
            raise ValueError("La descripcion es obligatoria.")

        # VALIDAR PRECIO

        if (
            isinstance(precio_base, bool)
            or not isinstance(precio_base, (int, float))
            or not math.isfinite(precio_base)
            or precio_base <= 0
        ):
            raise ValueError("El precio debe ser un numero mayor que cero.")

        # VALIDAR DISPONIBILIDAD

        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser verdadera o falsa.")

        self.identificador = identificador
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.precio_base = precio_base
        self.disponible = disponible

        logging.info("Servicio creado: %s", self.nombre)

    # =================================================
    # METODO ABSTRACTO
    # =================================================

    @abstractmethod
    def calcular_costo(self, duracion):
        pass

    # =================================================
    # VALIDAR DURACION
    # =================================================

    @staticmethod
    def validar_duracion(duracion):

        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not math.isfinite(duracion)
            or duracion <= 0
        ):
            raise ValueError("La duracion debe ser un numero finito mayor que cero.")

        return True

    # =================================================
    # VALIDAR PORCENTAJES
    # =================================================

    @staticmethod
    def validar_porcentaje(valor, nombre):

        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not math.isfinite(valor)
            or not 0 <= valor <= 100
        ):
            raise ValueError(f"El porcentaje de {nombre} debe estar entre 0 y 100.")

        return True

    # =================================================
    # CALCULAR DETALLE DEL PAGO
    # =================================================

    def calcular_detalle_pago(self, costo_base, descuento=0, impuesto=None):

        if (
            isinstance(costo_base, bool)
            or not isinstance(costo_base, (int, float))
            or not math.isfinite(costo_base)
            or costo_base < 0
        ):
            raise ValueError("El costo base no es valido.")

        if impuesto is None:
            impuesto = self.IVA

        self.validar_porcentaje(descuento, "descuento")
        self.validar_porcentaje(impuesto, "impuesto")

        # CALCULAR DESCUENTO

        valor_descuento = costo_base * descuento / 100

        # CALCULAR SUBTOTAL

        subtotal = costo_base - valor_descuento

        # CALCULAR IVA

        valor_impuesto = subtotal * impuesto / 100

        # CALCULAR TOTAL

        total = subtotal + valor_impuesto

        logging.info(
            "Pago calculado para servicio %s. Total: %.2f", self.identificador, total
        )

        return {
            "costo_base": costo_base,
            "descuento_porcentaje": descuento,
            "valor_descuento": valor_descuento,
            "subtotal": subtotal,
            "impuesto_porcentaje": impuesto,
            "valor_impuesto": valor_impuesto,
            "total": total,
            "total_pagar": total,
        }

    # =================================================
    # MOSTRAR INFORMACION
    # =================================================

    def mostrar_informacion(self):

        return (
            f"ID: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripcion: {self.descripcion}\n"
            f"Precio base: ${self.precio_base:,.2f}\n"
            f"IVA: {self.IVA}%\n"
            f"Disponible: {self.disponible}"
        )


# =====================================================
# RESERVA DE SALAS
# =====================================================


class ReservaSala(Servicio):

    def __init__(self, identificador, nombre, descripcion, precio_base, capacidad):

        super().__init__(identificador, nombre, descripcion, precio_base)

        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, int)
            or capacidad <= 0
        ):
            raise ValueError("La capacidad debe ser un entero mayor que cero.")

        self.capacidad = capacidad

    # CALCULAR COSTO

    def calcular_costo(self, duracion, descuento=0, impuesto=None):

        self.validar_duracion(duracion)

        costo_base = self.precio_base * duracion

        detalle = self.calcular_detalle_pago(costo_base, descuento, impuesto)

        return detalle["total_pagar"]

    # MOSTRAR INFORMACION

    def mostrar_informacion(self):

        return super().mostrar_informacion() + f"\nCapacidad: {self.capacidad} personas"


# =====================================================
# ALQUILER DE EQUIPOS
# =====================================================


class AlquilerEquipo(Servicio):

    def __init__(
        self, identificador, nombre, descripcion, precio_base, cantidad_disponible
    ):

        super().__init__(identificador, nombre, descripcion, precio_base)

        if (
            isinstance(cantidad_disponible, bool)
            or not isinstance(cantidad_disponible, int)
            or cantidad_disponible < 0
        ):
            raise ValueError("La cantidad disponible debe ser un entero no negativo.")

        self.cantidad_disponible = cantidad_disponible

    # CALCULAR COSTO

    def calcular_costo(self, duracion, descuento=0, impuesto=None, cantidad=1):

        self.validar_duracion(duracion)

        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero mayor que cero.")

        if cantidad > self.cantidad_disponible:
            raise ValueError("No hay suficientes equipos disponibles.")

        costo_base = self.precio_base * duracion * cantidad

        detalle = self.calcular_detalle_pago(costo_base, descuento, impuesto)

        return detalle["total_pagar"]

    # MOSTRAR INFORMACION

    def mostrar_informacion(self):

        return (
            super().mostrar_informacion()
            + f"\nCantidad disponible: {self.cantidad_disponible}"
        )


# =====================================================
# ASESORIAS ESPECIALIZADAS
# =====================================================


class Asesoria(Servicio):

    def __init__(self, identificador, nombre, descripcion, precio_base, especialidad):

        super().__init__(identificador, nombre, descripcion, precio_base)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValueError("La especialidad es obligatoria.")

        self.especialidad = especialidad.strip()

    # CALCULAR COSTO

    def calcular_costo(self, duracion, descuento=0, impuesto=None):

        self.validar_duracion(duracion)

        costo_base = self.precio_base * duracion

        detalle = self.calcular_detalle_pago(costo_base, descuento, impuesto)

        return detalle["total_pagar"]

    # MOSTRAR INFORMACION

    def mostrar_informacion(self):

        return super().mostrar_informacion() + f"\nEspecialidad: {self.especialidad}"
