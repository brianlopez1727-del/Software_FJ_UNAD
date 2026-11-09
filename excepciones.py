"""
Programa para gestionar las excepciones personalizadas
del sistema Software FJ.

Permite controlar errores relacionados con clientes,
servicios, reservas, validaciones y operaciones.
"""

# CLASE BASE DE LAS EXCEPCIONES DEL SISTEMA


class SoftwareFJError(Exception):

    def __init__(self, mensaje="Error general en el sistema Software FJ."):
        super().__init__(mensaje)


# EXCEPCION PARA DATOS INVALIDOS


class DatosInvalidosError(SoftwareFJError):

    def __init__(self, mensaje="Los datos ingresados no son validos."):
        super().__init__(mensaje)


# EXCEPCION PARA CLIENTES NO ENCONTRADOS


class ClienteNoEncontradoError(SoftwareFJError):

    def __init__(self, mensaje="No se encontro el cliente solicitado."):
        super().__init__(mensaje)


# EXCEPCION PARA SERVICIOS NO DISPONIBLES


class ServicioNoDisponibleError(SoftwareFJError):

    def __init__(self, mensaje="El servicio solicitado no esta disponible."):
        super().__init__(mensaje)


# EXCEPCION PARA RESERVAS INVALIDAS


class ReservaInvalidaError(SoftwareFJError):

    def __init__(self, mensaje="La reserva ingresada no es valida."):
        super().__init__(mensaje)


# EXCEPCION PARA OPERACIONES NO PERMITIDAS


class OperacionNoPermitidaError(SoftwareFJError):

    def __init__(self, mensaje="La operacion solicitada no esta permitida."):
        super().__init__(mensaje)


# EXCEPCION PARA PARAMETROS FALTANTES


class ParametroFaltanteError(SoftwareFJError):

    def __init__(self, mensaje="Falta proporcionar un parametro obligatorio."):
        super().__init__(mensaje)
