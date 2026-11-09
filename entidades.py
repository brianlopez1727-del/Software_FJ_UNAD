"""
Programa para gestionar las entidades generales del sistema Software FJ.

Contiene la clase abstracta Entidad, encargada de establecer
la estructura y los comportamientos generales de las entidades
que forman parte del sistema de clientes, servicios y reservas.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Entidad(ABC):

    def __init__(self, identificador, nombre):

        # VALIDAR IDENTIFICADOR

        if identificador is None:
            raise ValueError("El identificador es obligatorio.")

        if isinstance(identificador, bool):
            raise ValueError("El identificador no puede ser booleano.")

        if isinstance(identificador, str) and not identificador.strip():
            raise ValueError("El identificador no puede estar vacio.")

        if not isinstance(identificador, (int, str)):
            raise ValueError("El identificador debe ser texto o un entero.")

        if isinstance(identificador, int) and identificador <= 0:
            raise ValueError("El identificador debe ser mayor que cero.")

        # VALIDAR NOMBRE

        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")

        # ATRIBUTOS ENCAPSULADOS

        self._identificador = identificador
        self._nombre = nombre.strip()
        self._fecha_creacion = datetime.now()

    # PROPIEDADES

    @property
    def identificador(self):
        return self._identificador

    @property
    def nombre(self):
        return self._nombre

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # METODO ABSTRACTO

    @abstractmethod
    def mostrar_informacion(self):
        pass

    @abstractmethod
    def validar_datos(self):
        pass

    # REPRESENTACION DEL OBJETO

    def __str__(self):

        return (
            f"Identificador: {self._identificador} | "
            f"Nombre: {self._nombre} | "
            f"Fecha de creacion: "
            f"{self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )
