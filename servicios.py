"""
Programa para gestionar los servicios de la empresa Software FJ.

Contiene una clase abstracta Servicio y tres clases especializadas:
ReservaSala, AlquilerEquipo y Asesoria.

Implementa abstraccion, herencia, polimorfismo, encapsulacion,
validaciones y calculo de costos con impuestos y descuentos.
"""

# IMPORTA LA CLASE ABSTRACTA Y SUS METODOS

from abc import abstractmethod

# IMPORTA LA CLASE ENTIDAD

from entidades import Entidad

# IMPORTA LAS EXCEPCIONES PERSONALIZADAS

from excepciones import DatosInvalidosError, ServicioNoDisponibleError

# CLASE ABSTRACTA QUE REPRESENTA LOS SERVICIOS DE SOFTWARE FJ


class Servicio(Entidad):

    # CONSTRUCTOR DE LA CLASE SERVICIO
    def __init__(
        self, identificador, nombre, descripcion, precio_base, disponible=True
    ):

        # INICIALIZA LOS ATRIBUTOS DE LA CLASE PADRE
        super().__init__(identificador, nombre)

        # GUARDA LA DESCRIPCION DEL SERVICIO
        self.__descripcion = descripcion

        # GUARDA EL PRECIO BASE DEL SERVICIO
        self.__precio_base = precio_base

        # DEFINE SI EL SERVICIO ESTA DISPONIBLE
        self.__disponible = disponible

        # VALIDA LOS DATOS DEL SERVICIO
        self.validar_datos()

    # CONSULTA LA DESCRIPCION DEL SERVICIO
    @property
    def descripcion(self):
        return self.__descripcion

    # CONSULTA EL PRECIO BASE DEL SERVICIO
    @property
    def precio_base(self):
        return self.__precio_base

    # CONSULTA LA DISPONIBILIDAD DEL SERVICIO
    @property
    def disponible(self):
        return self.__disponible

    # MUESTRA LA INFORMACION GENERAL DEL SERVICIO
    def mostrar_informacion(self):

        return (
            f"\nINFORMACION DEL SERVICIO\n"
            f"Identificador: {self.identificador}\n"
            f"Nombre: {self.nombre}\n"
            f"Descripcion: {self.__descripcion}\n"
            f"Precio base: ${self.__precio_base}\n"
            f"Disponible: {self.__disponible}"
        )

    # MODIFICA LA DISPONIBILIDAD DEL SERVICIO
    def cambiar_disponibilidad(self, estado):

        if not isinstance(estado, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")

        self.__disponible = estado

    # VALIDA LOS DATOS GENERALES DEL SERVICIO
    def validar_datos(self):

        if not isinstance(self.__descripcion, str) or not self.__descripcion.strip():
            raise DatosInvalidosError("La descripcion del servicio es obligatoria.")

        if isinstance(self.__precio_base, bool) or not isinstance(
            self.__precio_base, (int, float)
        ):
            raise DatosInvalidosError("El precio base debe ser un valor numerico.")

        if self.__precio_base <= 0:
            raise DatosInvalidosError("El precio base debe ser mayor que cero.")

        if not isinstance(self.__disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")

        # EJECUTA LAS VALIDACIONES ESPECIFICAS DE CADA SERVICIO
        self.validar_parametros()

        return True

    # CALCULA EL COSTO FINAL CON DESCUENTOS E IMPUESTOS
    def calcular_total(self, costo, descuento=0, impuesto=0):

        # VALIDA QUE LOS VALORES SEAN NUMERICOS
        valores = [costo, descuento, impuesto]

        if any(
            isinstance(valor, bool) or not isinstance(valor, (int, float))
            for valor in valores
        ):
            raise DatosInvalidosError(
                "Los costos, descuentos e impuestos deben ser numericos."
            )

        # VALIDA QUE LOS VALORES NO SEAN NEGATIVOS
        if costo <= 0 or descuento < 0 or impuesto < 0:
            raise DatosInvalidosError(
                "Los valores deben ser positivos o cero segun corresponda."
            )

        # VALIDA LOS PORCENTAJES
        if descuento > 100 or impuesto > 100:
            raise DatosInvalidosError(
                "Los porcentajes no pueden superar el 100 por ciento."
            )

        # CALCULA EL DESCUENTO
        valor_descuento = costo * (descuento / 100)

        subtotal = costo - valor_descuento

        # CALCULA EL IMPUESTO
        valor_impuesto = subtotal * (impuesto / 100)

        # CALCULA EL COSTO FINAL
        total = subtotal + valor_impuesto

        return round(total, 2)

    # METODO ABSTRACTO PARA VALIDAR PARAMETROS ESPECIFICOS
    @abstractmethod
    def validar_parametros(self):
        pass

    # METODO ABSTRACTO PARA CALCULAR EL COSTO DEL SERVICIO
    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    # METODO ABSTRACTO PARA DESCRIBIR EL SERVICIO
    @abstractmethod
    def describir_servicio(self):
        pass


# CLASE QUE REPRESENTA EL SERVICIO DE RESERVA DE SALAS
class ReservaSala(Servicio):

    # CONSTRUCTOR DE LA CLASE RESERVA SALA
    def __init__(
        self,
        identificador,
        nombre,
        descripcion,
        precio_base,
        capacidad,
        disponible=True,
    ):

        # INICIALIZA LOS ATRIBUTOS DE LA CLASE PADRE
        self.__capacidad = capacidad

        super().__init__(identificador, nombre, descripcion, precio_base, disponible)

    # VALIDA LOS PARAMETROS DE LA SALA
    def validar_parametros(self):

        if isinstance(self.__capacidad, bool) or not isinstance(self.__capacidad, int):
            raise DatosInvalidosError(
                "La capacidad de la sala debe ser un numero entero."
            )

        if self.__capacidad <= 0:
            raise DatosInvalidosError(
                "La capacidad de la sala debe ser mayor que cero."
            )

    # CONSULTA LA CAPACIDAD DE LA SALA
    @property
    def capacidad(self):
        return self.__capacidad

    # CALCULA EL COSTO DE RESERVAR UNA SALA
    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        # VALIDA LA DURACION
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise DatosInvalidosError(
                "La duracion de la reserva debe ser mayor que cero."
            )

        # VERIFICA LA DISPONIBILIDAD
        if not self.disponible:
            raise ServicioNoDisponibleError("La sala seleccionada no esta disponible.")

        # CALCULA EL COSTO POR HORA
        costo = self.precio_base * duracion

        return self.calcular_total(costo, descuento, impuesto)

    # DESCRIBE LAS CARACTERISTICAS DE LA SALA
    def describir_servicio(self):

        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Reserva de sala\n"
            f"Descripcion: {self.descripcion}\n"
            f"Capacidad: {self.__capacidad} personas\n"
            f"Precio por hora: ${self.precio_base}\n"
            f"Disponible: {self.disponible}"
        )


# CLASE QUE REPRESENTA EL ALQUILER DE EQUIPOS TECNOLOGICOS


class AlquilerEquipo(Servicio):

    # CONSTRUCTOR DE LA CLASE ALQUILER DE EQUIPO
    def __init__(
        self,
        identificador,
        nombre,
        descripcion,
        precio_base,
        equipo,
        cantidad,
        disponible=True,
    ):

        # INICIALIZA LOS ATRIBUTOS ESPECIFICOS
        self.__equipo = equipo
        self.__cantidad = cantidad

        # INICIALIZA LOS ATRIBUTOS DE LA CLASE PADRE
        super().__init__(identificador, nombre, descripcion, precio_base, disponible)

    # VALIDA LOS PARAMETROS DEL EQUIPO
    def validar_parametros(self):

        if not isinstance(self.__equipo, str) or not self.__equipo.strip():
            raise DatosInvalidosError("El nombre del equipo es obligatorio.")

        if isinstance(self.__cantidad, bool) or not isinstance(self.__cantidad, int):
            raise DatosInvalidosError("La cantidad debe ser un numero entero.")

        if self.__cantidad <= 0:
            raise DatosInvalidosError("La cantidad debe ser mayor que cero.")

    # CONSULTA EL NOMBRE DEL EQUIPO
    @property
    def equipo(self):
        return self.__equipo

    # CONSULTA LA CANTIDAD DE EQUIPOS
    @property
    def cantidad(self):
        return self.__cantidad

    # CALCULA EL COSTO DEL ALQUILER DE EQUIPOS
    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        # VALIDA LA DURACION DEL ALQUILER
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise DatosInvalidosError(
                "La duracion del alquiler debe ser mayor que cero."
            )

        # VERIFICA LA DISPONIBILIDAD DEL SERVICIO
        if not self.disponible:
            raise ServicioNoDisponibleError("El equipo solicitado no esta disponible.")

        # CALCULA EL COSTO SEGUN CANTIDAD Y DURACION
        costo = self.precio_base * self.__cantidad * duracion

        return self.calcular_total(costo, descuento, impuesto)

    # DESCRIBE LAS CARACTERISTICAS DEL EQUIPO
    def describir_servicio(self):

        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Alquiler de equipo\n"
            f"Equipo: {self.__equipo}\n"
            f"Cantidad: {self.__cantidad}\n"
            f"Precio por unidad y hora: ${self.precio_base}\n"
            f"Disponible: {self.disponible}"
        )


# CLASE QUE REPRESENTA LAS ASESORIAS ESPECIALIZADAS


class Asesoria(Servicio):

    # CONSTRUCTOR DE LA CLASE ASESORIA
    def __init__(
        self,
        identificador,
        nombre,
        descripcion,
        precio_base,
        especialidad,
        disponible=True,
    ):

        # GUARDA LA ESPECIALIDAD DE LA ASESORIA
        self.__especialidad = especialidad

        # INICIALIZA LOS ATRIBUTOS DE LA CLASE PADRE
        super().__init__(identificador, nombre, descripcion, precio_base, disponible)

    # VALIDA LOS PARAMETROS DE LA ASESORIA
    def validar_parametros(self):

        if not isinstance(self.__especialidad, str) or not self.__especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoria es obligatoria.")

    # CONSULTA LA ESPECIALIDAD DE LA ASESORIA
    @property
    def especialidad(self):
        return self.__especialidad

    # CALCULA EL COSTO DE LA ASESORIA
    def calcular_costo(self, duracion, descuento=0, impuesto=0):

        # VALIDA LA DURACION DE LA ASESORIA
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or duracion <= 0
        ):
            raise DatosInvalidosError(
                "La duracion de la asesoria debe ser mayor que cero."
            )

        # VERIFICA LA DISPONIBILIDAD
        if not self.disponible:
            raise ServicioNoDisponibleError(
                "La asesoria solicitada no esta disponible."
            )

        # CALCULA EL COSTO SEGUN LAS HORAS CONTRATADAS
        costo = self.precio_base * duracion

        return self.calcular_total(costo, descuento, impuesto)

    # DESCRIBE LAS CARACTERISTICAS DE LA ASESORIA
    def describir_servicio(self):

        return (
            f"Servicio: {self.nombre}\n"
            f"Tipo: Asesoria especializada\n"
            f"Especialidad: {self.__especialidad}\n"
            f"Descripcion: {self.descripcion}\n"
            f"Precio por hora: ${self.precio_base}\n"
            f"Disponible: {self.disponible}"
        )
