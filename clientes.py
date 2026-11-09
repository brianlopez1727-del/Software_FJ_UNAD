"""
Programa para gestionar los clientes de la empresa Software FJ.

Permite registrar clientes, almacenar sus datos personales,
validar la informacion ingresada y consultar sus datos
mediante principios de programacion orientada a objetos.
"""

import re

from entidades import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):

    def __init__(self, identificador, nombre, apellido, documento, telefono, correo):

        # INICIALIZAR CLASE PADRE

        super().__init__(identificador, nombre)

        # GUARDAR DATOS PERSONALES

        self.__apellido = apellido.strip() if isinstance(apellido, str) else apellido
        self.__documento = str(documento).strip() if documento is not None else ""
        self.__telefono = str(telefono).strip() if telefono is not None else ""
        self.__correo = correo.strip().lower() if isinstance(correo, str) else correo

        # VALIDAR DATOS

        self.validar_datos()

    # PROPIEDADES

    @property
    def apellido(self):
        return self.__apellido

    @property
    def documento(self):
        return self.__documento

    @property
    def telefono(self):
        return self.__telefono

    @property
    def correo(self):
        return self.__correo

    # VALIDAR INFORMACION DEL CLIENTE

    def validar_datos(self):

        # VALIDAR NOMBRE

        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")

        # VALIDAR APELLIDO

        if not isinstance(self.__apellido, str) or not self.__apellido.strip():
            raise DatosInvalidosError("El apellido es obligatorio.")

        # VALIDAR DOCUMENTO

        if not self.__documento.isdigit() or not 6 <= len(self.__documento) <= 12:
            raise DatosInvalidosError(
                "El documento debe contener entre 6 y 12 digitos."
            )

        # VALIDAR TELEFONO

        if not self.__telefono.isdigit() or not 7 <= len(self.__telefono) <= 15:
            raise DatosInvalidosError("El telefono debe contener entre 7 y 15 digitos.")

        # VALIDAR CORREO

        patron_correo = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"

        if not isinstance(self.__correo, str) or not re.fullmatch(
            patron_correo, self.__correo
        ):
            raise DatosInvalidosError(
                "El correo electronico no tiene un formato valido."
            )

        return True

    # MOSTRAR INFORMACION

    def mostrar_informacion(self):

        return (
            f"\nINFORMACION DEL CLIENTE\n"
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self.nombre} {self.__apellido}\n"
            f"Documento: {self.__documento}\n"
            f"Telefono: {self.__telefono}\n"
            f"Correo: {self.__correo}\n"
            f"Fecha de registro: "
            f"{self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    # REPRESENTACION DEL OBJETO

    def __str__(self):

        return self.mostrar_informacion()
