"""
Programa para gestionar las entidades generales del sistema Software FJ.

Contiene la clase abstracta Entidad, encargada de establecer
la estructura y los comportamientos generales de las entidades
que forman parte del sistema de clientes, servicios y reservas.
"""

# IMPORTA LAS HERRAMIENTAS PARA CREAR CLASES ABSTRACTAS

from abc import ABC, abstractmethod

# IMPORTA LA FECHA Y HORA ACTUAL DEL SISTEMA

from datetime import datetime

# CLASE ABSTRACTA QUE REPRESENTA LAS ENTIDADES GENERALES DEL SISTEMA


class Entidad(ABC):

    # CONSTRUCTOR DE LA CLASE ENTIDAD
    def __init__(self, identificador, nombre):

        # VALIDACION DEL IDENTIFICADOR
        if not identificador:
            raise ValueError("El identificador es obligatorio.")

        # VALIDACION DEL NOMBRE
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacio.")

        # ATRIBUTOS ENCAPSULADOS DE LA ENTIDAD
        self._identificador = identificador
        self._nombre = nombre.strip()
        self._fecha_creacion = datetime.now()

    # CONSULTA EL IDENTIFICADOR DE LA ENTIDAD
    @property
    def identificador(self):
        return self._identificador

    # CONSULTA EL NOMBRE DE LA ENTIDAD
    @property
    def nombre(self):
        return self._nombre

    # CONSULTA LA FECHA DE CREACION DE LA ENTIDAD
    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # METODO ABSTRACTO PARA MOSTRAR LA INFORMACION DE LA ENTIDAD
    @abstractmethod
    def mostrar_informacion(self):
        pass

    # METODO ABSTRACTO PARA VALIDAR LOS DATOS DE LA ENTIDAD
    @abstractmethod
    def validar_datos(self):
        pass

    # REPRESENTACION GENERAL DE LA ENTIDAD
    def __str__(self):
        return (
            f"Identificador: {self._identificador} | "
            f"Nombre: {self._nombre} | "
            f"Fecha de creacion: "
            f"{self._fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )
