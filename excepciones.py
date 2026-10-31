"""
Programa para gestionar los errores del Sistema Integral de Gestión
de Clientes, Servicios y Reservas de la empresa Software FJ.

Contiene excepciones personalizadas para controlar errores
durante el funcionamiento de la aplicación.
"""

# CLASE BASE QUE REPRESENTA LOS ERRORES GENERALES DEL SISTEMA


class ErrorSistema(Exception):

    # CONSTRUCTOR DE LA CLASE DE ERROR GENERAL
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


# CLASE QUE REPRESENTA ERRORES EN LOS DATOS INGRESADOS


class DatosInvalidosError(ErrorSistema):

    # CONSTRUCTOR DEL ERROR DE DATOS INVALIDOS
    def __init__(self, mensaje="Los datos ingresados no son validos."):
        super().__init__(mensaje)


# CLASE QUE REPRESENTA ERRORES CUANDO NO SE ENCUENTRA UN CLIENTE


class ClienteNoEncontradoError(ErrorSistema):

    # CONSTRUCTOR DEL ERROR DE CLIENTE NO ENCONTRADO
    def __init__(self, mensaje="El cliente solicitado no existe."):
        super().__init__(mensaje)


# CLASE QUE REPRESENTA ERRORES DE SERVICIOS NO DISPONIBLES


class ServicioNoDisponibleError(ErrorSistema):

    # CONSTRUCTOR DEL ERROR DE SERVICIO NO DISPONIBLE
    def __init__(self, mensaje="El servicio solicitado no esta disponible."):
        super().__init__(mensaje)


# CLASE QUE REPRESENTA ERRORES EN LA GESTION DE RESERVAS


class ReservaInvalidaError(ErrorSistema):

    # CONSTRUCTOR DEL ERROR DE RESERVA INVALIDA
    def __init__(self, mensaje="La reserva no cumple las condiciones requeridas."):
        super().__init__(mensaje)


# CLASE QUE REPRESENTA OPERACIONES NO PERMITIDAS


class OperacionNoPermitidaError(ErrorSistema):

    # CONSTRUCTOR DEL ERROR DE OPERACION NO PERMITIDA
    def __init__(self, mensaje="La operacion solicitada no esta permitida."):
        super().__init__(mensaje)


# CLASE QUE REPRESENTA PARAMETROS OBLIGATORIOS FALTANTES


class ParametroFaltanteError(ErrorSistema):

    # CONSTRUCTOR DEL ERROR DE PARAMETRO FALTANTE
    def __init__(self, mensaje="Falta un parametro obligatorio."):
        super().__init__(mensaje)
