"""
Programa para gestionar los clientes de la empresa Software FJ.

Permite registrar clientes, almacenar sus datos personales,
validar la informacion ingresada y consultar sus datos
mediante principios de programacion orientada a objetos.
"""

# IMPORTA LA CLASE ABSTRACTA ENTIDAD

from entidades import Entidad

# IMPORTA LAS EXCEPCIONES PERSONALIZADAS

from excepciones import DatosInvalidosError

# IMPORTA EXPRESIONES REGULARES PARA VALIDAR LOS DATOS

import re

# CLASE QUE REPRESENTA LOS CLIENTES DE SOFTWARE FJ


class Cliente(Entidad):

    # CONSTRUCTOR DE LA CLASE CLIENTE
    def __init__(self, identificador, nombre, apellido, documento, telefono, correo):

        # INICIALIZA LOS ATRIBUTOS DE LA CLASE PADRE
        super().__init__(identificador, nombre)

        # ALMACENA LOS DATOS PERSONALES DEL CLIENTE
        self.__apellido = apellido
        self.__documento = documento
        self.__telefono = telefono
        self.__correo = correo

        # VALIDA LOS DATOS DEL CLIENTE
        self.validar_datos()

    # CONSULTA EL APELLIDO DEL CLIENTE
    @property
    def apellido(self):
        return self.__apellido

    # CONSULTA EL DOCUMENTO DEL CLIENTE
    @property
    def documento(self):
        return self.__documento

    # CONSULTA EL TELEFONO DEL CLIENTE
    @property
    def telefono(self):
        return self.__telefono

    # CONSULTA EL CORREO ELECTRONICO DEL CLIENTE
    @property
    def correo(self):
        return self.__correo

    # VALIDA LOS DATOS PERSONALES DEL CLIENTE
    def validar_datos(self):

        # VALIDA QUE EL APELLIDO NO ESTE VACIO
        if not isinstance(self.__apellido, str) or not self.__apellido.strip():
            raise DatosInvalidosError("El apellido es obligatorio.")

        # VALIDA QUE EL DOCUMENTO CONTENGA ENTRE 6 Y 12 DIGITOS
        if (
            not str(self.__documento).isdigit()
            or not 6 <= len(str(self.__documento)) <= 12
        ):
            raise DatosInvalidosError(
                "El documento debe contener entre 6 y 12 digitos."
            )

        # VALIDA QUE EL TELEFONO CONTENGA ENTRE 7 Y 15 DIGITOS
        if (
            not str(self.__telefono).isdigit()
            or not 7 <= len(str(self.__telefono)) <= 15
        ):
            raise DatosInvalidosError("El telefono debe contener entre 7 y 15 digitos.")

        # VALIDA EL FORMATO DEL CORREO ELECTRONICO
        patron_correo = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not isinstance(self.__correo, str) or not re.match(
            patron_correo, self.__correo
        ):
            raise DatosInvalidosError(
                "El correo electronico no tiene un formato valido."
            )

        # CONFIRMA QUE TODOS LOS DATOS SON CORRECTOS
        return True

    # MUESTRA LA INFORMACION COMPLETA DEL CLIENTE
    def mostrar_informacion(self):

        return (
            f"\nINFORMACION DEL CLIENTE\n"
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self.nombre} {self.__apellido}\n"
            f"Documento: {self.__documento}\n"
            f"Telefono: {self.__telefono}\n"
            f"Correo: {self.__correo}\n"
            f"Fecha de registro: {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    # REPRESENTACION DEL OBJETO CLIENTE
    def __str__(self):
        return self.mostrar_informacion()
