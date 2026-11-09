"""
VENTANA PRINCIPAL DE SOFTWARE FJ.

Interfaz grafica desarrollada con CustomTkinter.

Incluye:
- Gestion de clientes.
- Gestion de servicios.
- Gestion de reservas.
- Dashboard administrativo.
- Validaciones.
- Manejo de excepciones.
- Registro de operaciones.
"""

import customtkinter as ctk
import logging
import re

from tkinter import messagebox

from sistema import SistemaFJ
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria

from excepciones import (
    DatosInvalidosError,
    ClienteNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
)

# =====================================================
# CONFIGURACION GENERAL
# =====================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

COLOR_FONDO = "#0B1120"
COLOR_MENU = "#111827"
COLOR_PANEL = "#1F2937"
COLOR_PRIMARIO = "#2563EB"
COLOR_SECUNDARIO = "#374151"
COLOR_TEXTO = "#F9FAFB"
COLOR_TEXTO_SECUNDARIO = "#9CA3AF"
COLOR_EXITO = "#16A34A"
COLOR_ERROR = "#DC2626"
COLOR_ADVERTENCIA = "#D97706"


# =====================================================
# CLASE PRINCIPAL
# =====================================================


class VentanaPrincipal(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Software FJ | Sistema de Gestion")
        self.geometry("1250x780")
        self.minsize(1050, 680)
        self.configure(fg_color=COLOR_FONDO)

        self.sistema = SistemaFJ()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_menu_lateral()
        self.crear_contenido_principal()

        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        logging.info("Interfaz grafica de Software FJ iniciada.")

    # =================================================
    # MENU LATERAL
    # =================================================

    def crear_menu_lateral(self):

        self.menu = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLOR_MENU)

        self.menu.grid(row=0, column=0, sticky="nsew")

        self.menu.grid_propagate(False)

        ctk.CTkLabel(
            self.menu,
            text="SOFTWARE FJ",
            font=("Segoe UI", 26, "bold"),
            text_color="#3B82F6",
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.menu,
            text="Sistema de gestion empresarial",
            font=("Segoe UI", 11),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).pack(pady=(0, 35))

        opciones = [
            ("⌂  Dashboard", self.mostrar_dashboard),
            ("♙  Clientes", self.mostrar_clientes),
            ("▣  Servicios", self.mostrar_servicios),
            ("▤  Reservas", self.mostrar_reservas),
        ]

        for nombre, comando in opciones:

            ctk.CTkButton(
                self.menu,
                text=nombre,
                height=48,
                corner_radius=8,
                anchor="w",
                fg_color="transparent",
                hover_color="#1E3A5F",
                text_color=COLOR_TEXTO,
                font=("Segoe UI", 14),
                command=comando,
            ).pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            self.menu,
            text="SOFTWARE FJ",
            font=("Segoe UI", 12, "bold"),
            text_color="#60A5FA",
        ).pack(side="bottom", pady=(0, 5))

        ctk.CTkLabel(
            self.menu,
            text="Version 2.0",
            font=("Segoe UI", 10),
            text_color=COLOR_TEXTO_SECUNDARIO,
        ).pack(side="bottom", pady=(0, 20))

    # =================================================
    # CONTENIDO PRINCIPAL
    # =================================================

    def crear_contenido_principal(self):

        self.contenido = ctk.CTkFrame(self, fg_color=COLOR_FONDO, corner_radius=0)

        self.contenido.grid(row=0, column=1, sticky="nsew")

        self.mostrar_dashboard()

    # =================================================
    # LIMPIAR CONTENIDO
    # =================================================

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    # =================================================
    # CREAR TITULOS
    # =================================================

    def crear_titulo(self, titulo, descripcion=""):

        ctk.CTkLabel(
            self.contenido,
            text=titulo,
            font=("Segoe UI", 30, "bold"),
            text_color=COLOR_TEXTO,
        ).pack(anchor="w", padx=35, pady=(30, 5))

        if descripcion:

            ctk.CTkLabel(
                self.contenido,
                text=descripcion,
                font=("Segoe UI", 14),
                text_color=COLOR_TEXTO_SECUNDARIO,
            ).pack(anchor="w", padx=35, pady=(0, 20))

    # =================================================
    # BOTON REUTILIZABLE
    # =================================================

    def crear_boton(self, contenedor, texto, comando, color=COLOR_PRIMARIO):

        return ctk.CTkButton(
            contenedor,
            text=texto,
            command=comando,
            height=40,
            corner_radius=8,
            fg_color=color,
            font=("Segoe UI", 13, "bold"),
        )

    # =================================================
    # DASHBOARD
    # =================================================

    def mostrar_dashboard(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Panel de control", "Resumen general del sistema Software FJ."
        )

        contenedor = ctk.CTkFrame(self.contenido, fg_color="transparent")

        contenedor.pack(fill="x", padx=25, pady=15)

        try:

            clientes = self.sistema.listar_clientes()
            servicios = self.sistema.listar_servicios()
            reservas = self.sistema.listar_reservas()

            datos = [
                ("CLIENTES REGISTRADOS", len(clientes), "#2563EB"),
                ("SERVICIOS REGISTRADOS", len(servicios), "#16A34A"),
                ("RESERVAS REGISTRADAS", len(reservas), "#D97706"),
            ]

            for titulo, cantidad, color in datos:

                tarjeta = ctk.CTkFrame(
                    contenedor,
                    fg_color=COLOR_PANEL,
                    corner_radius=12,
                    border_width=1,
                    border_color="#374151",
                )

                tarjeta.pack(side="left", expand=True, fill="both", padx=10, pady=10)

                ctk.CTkLabel(
                    tarjeta,
                    text=titulo,
                    font=("Segoe UI", 12, "bold"),
                    text_color=COLOR_TEXTO_SECUNDARIO,
                ).pack(pady=(25, 10))

                ctk.CTkLabel(
                    tarjeta,
                    text=str(cantidad),
                    font=("Segoe UI", 38, "bold"),
                    text_color=color,
                ).pack(pady=(0, 25))

        except Exception as error:

            logging.exception("Error al cargar el dashboard.")

            messagebox.showerror("Error", str(error))

            return

        informacion = ctk.CTkFrame(
            self.contenido, fg_color=COLOR_PANEL, corner_radius=12
        )

        informacion.pack(fill="both", expand=True, padx=35, pady=20)

        ctk.CTkLabel(
            informacion,
            text="Acerca de Software FJ",
            font=("Segoe UI", 22, "bold"),
            text_color=COLOR_TEXTO,
        ).pack(anchor="w", padx=25, pady=(25, 15))

        descripcion = (
            "Software FJ es un sistema integral de gestion "
            "empresarial desarrollado mediante programacion "
            "orientada a objetos.\n\n"
            "Permite administrar clientes, registrar servicios "
            "y gestionar reservas de salas, alquiler de equipos "
            "y asesorias especializadas.\n\n"
            "Incluye calculos de costos, descuentos e IVA del 19%, "
            "validaciones, excepciones personalizadas y logging."
        )

        ctk.CTkLabel(
            informacion,
            text=descripcion,
            font=("Segoe UI", 14),
            text_color="#D1D5DB",
            justify="left",
            wraplength=850,
        ).pack(anchor="w", padx=25, pady=10)

        ctk.CTkButton(
            informacion,
            text="Actualizar estadisticas",
            height=42,
            width=220,
            fg_color=COLOR_PRIMARIO,
            command=self.mostrar_dashboard,
        ).pack(anchor="w", padx=25, pady=25)

        logging.info("Dashboard actualizado.")

    # =================================================
    # MODULO DE CLIENTES
    # =================================================

    def mostrar_clientes(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Gestion de clientes", "Consulta, registra y administra los clientes."
        )

        barra = ctk.CTkFrame(self.contenido, fg_color="transparent")

        barra.pack(fill="x", padx=35, pady=10)

        self.crear_boton(barra, "+ Registrar cliente", self.formulario_cliente).pack(
            side="left", padx=5
        )

        self.crear_boton(
            barra, "Actualizar", self.mostrar_clientes, COLOR_SECUNDARIO
        ).pack(side="left", padx=5)

        tabla = ctk.CTkScrollableFrame(self.contenido, fg_color=COLOR_PANEL)

        tabla.pack(fill="both", expand=True, padx=35, pady=15)

        encabezados = ["ID", "NOMBRE", "APELLIDO", "DOCUMENTO", "TELEFONO", "CORREO"]

        for columna, encabezado in enumerate(encabezados):

            tabla.grid_columnconfigure(columna, weight=1)

            ctk.CTkLabel(
                tabla,
                text=encabezado,
                font=("Segoe UI", 11, "bold"),
                text_color="#60A5FA",
            ).grid(row=0, column=columna, padx=6, pady=12)

        try:

            clientes = self.sistema.listar_clientes()

            if not clientes:

                ctk.CTkLabel(
                    tabla,
                    text="No hay clientes registrados.",
                    text_color=COLOR_TEXTO_SECUNDARIO,
                ).grid(row=1, column=0, columnspan=6, pady=30)

                return

            for fila, cliente in enumerate(clientes, start=1):

                datos = [
                    cliente.identificador,
                    cliente.nombre,
                    cliente.apellido,
                    cliente.documento,
                    cliente.telefono,
                    cliente.correo,
                ]

                for columna, dato in enumerate(datos):

                    ctk.CTkLabel(
                        tabla,
                        text=str(dato),
                        text_color=COLOR_TEXTO,
                        font=("Segoe UI", 11),
                    ).grid(row=fila, column=columna, padx=6, pady=12)

        except Exception as error:

            logging.exception("Error al consultar clientes.")

            messagebox.showerror("Error de consulta", str(error))

    # =================================================
    # FORMULARIO DE CLIENTES
    # =================================================

    def formulario_cliente(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Registrar nuevo cliente", "Complete todos los datos personales."
        )

        formulario = ctk.CTkScrollableFrame(self.contenido, fg_color=COLOR_PANEL)

        formulario.pack(fill="both", expand=True, padx=35, pady=10)

        campos = [
            ("Identificador", "Ejemplo: 1"),
            ("Nombre", "Ingrese el nombre"),
            ("Apellido", "Ingrese el apellido"),
            ("Documento", "Ingrese el documento"),
            ("Telefono", "Ingrese el telefono"),
            ("Correo", "ejemplo@gmail.com"),
        ]

        self.campos_cliente = {}

        for etiqueta, placeholder in campos:

            ctk.CTkLabel(
                formulario,
                text=etiqueta,
                font=("Segoe UI", 13, "bold"),
                text_color=COLOR_TEXTO,
            ).pack(anchor="w", padx=25, pady=(12, 3))

            entrada = ctk.CTkEntry(
                formulario, width=420, height=40, placeholder_text=placeholder
            )

            entrada.pack(anchor="w", padx=25, pady=5)

            self.campos_cliente[etiqueta] = entrada

        botones = ctk.CTkFrame(formulario, fg_color="transparent")

        botones.pack(anchor="w", padx=25, pady=25)

        self.crear_boton(
            botones, "Guardar cliente", self.registrar_cliente_interfaz
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones, "Volver", self.mostrar_clientes, COLOR_SECUNDARIO
        ).pack(side="left", padx=5)

    # =================================================
    # REGISTRAR CLIENTE
    # =================================================

    def registrar_cliente_interfaz(self):

        try:

            identificador_texto = self.campos_cliente["Identificador"].get().strip()

            nombre = self.campos_cliente["Nombre"].get().strip()
            apellido = self.campos_cliente["Apellido"].get().strip()
            documento = self.campos_cliente["Documento"].get().strip()
            telefono = self.campos_cliente["Telefono"].get().strip()
            correo = self.campos_cliente["Correo"].get().strip()

            if not all(
                [identificador_texto, nombre, apellido, documento, telefono, correo]
            ):

                raise ValueError("Todos los campos son obligatorios.")

            if not identificador_texto.isdigit():

                raise ValueError("El identificador debe ser numerico.")

            identificador = int(identificador_texto)

            if identificador <= 0:

                raise ValueError("El identificador debe ser mayor que cero.")

            if not documento.isdigit():

                raise ValueError("El documento solamente debe contener numeros.")

            if not 6 <= len(documento) <= 12:

                raise ValueError("El documento debe tener entre 6 y 12 digitos.")

            if not telefono.isdigit():

                raise ValueError("El telefono solamente debe contener numeros.")

            if not 7 <= len(telefono) <= 15:

                raise ValueError("El telefono debe tener entre 7 y 15 digitos.")

            patron_correo = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

            if not re.match(patron_correo, correo):

                raise ValueError("El correo electronico no tiene un formato valido.")

            nuevo_cliente = Cliente(
                identificador, nombre, apellido, documento, telefono, correo
            )

            resultado = self.sistema.registrar_cliente(nuevo_cliente)

            logging.info("Cliente registrado correctamente: %s", identificador)

            messagebox.showinfo("Registro exitoso", str(resultado))

            self.mostrar_clientes()

        except Exception as error:

            logging.exception("Error al registrar cliente.")

            messagebox.showerror("Error de registro", str(error))

    # =================================================
    # MODULO DE SERVICIOS
    # =================================================

    def mostrar_servicios(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Gestion de servicios",
            "Consulta y administra los servicios de Software FJ.",
        )

        barra = ctk.CTkFrame(self.contenido, fg_color="transparent")

        barra.pack(fill="x", padx=35, pady=10)

        self.crear_boton(barra, "+ Registrar servicio", self.formulario_servicio).pack(
            side="left", padx=5
        )

        self.crear_boton(
            barra, "Actualizar", self.mostrar_servicios, COLOR_SECUNDARIO
        ).pack(side="left", padx=5)

        tabla = ctk.CTkScrollableFrame(self.contenido, fg_color=COLOR_PANEL)

        tabla.pack(fill="both", expand=True, padx=35, pady=15)

        encabezados = ["ID", "SERVICIO", "TIPO", "PRECIO BASE", "DISPONIBLE"]

        for columna, encabezado in enumerate(encabezados):

            tabla.grid_columnconfigure(columna, weight=1)

            ctk.CTkLabel(
                tabla,
                text=encabezado,
                font=("Segoe UI", 11, "bold"),
                text_color="#60A5FA",
            ).grid(row=0, column=columna, padx=8, pady=12)

        try:

            servicios = self.sistema.listar_servicios()

            if not servicios:

                ctk.CTkLabel(
                    tabla,
                    text="No hay servicios registrados.",
                    text_color=COLOR_TEXTO_SECUNDARIO,
                ).grid(row=1, column=0, columnspan=5, pady=30)

                return

            for fila, servicio in enumerate(servicios, start=1):

                datos = [
                    servicio.identificador,
                    servicio.nombre,
                    type(servicio).__name__,
                    f"${servicio.precio_base:,.2f}",
                    "Si" if servicio.disponible else "No",
                ]

                for columna, dato in enumerate(datos):

                    ctk.CTkLabel(
                        tabla,
                        text=str(dato),
                        text_color=COLOR_TEXTO,
                        font=("Segoe UI", 11),
                    ).grid(row=fila, column=columna, padx=8, pady=12)

        except Exception as error:

            logging.exception("Error al consultar servicios.")

            messagebox.showerror("Error de consulta", str(error))

    # =================================================
    # FORMULARIO DE SERVICIOS
    # =================================================

    def formulario_servicio(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Registrar nuevo servicio",
            "Seleccione el tipo de servicio e ingrese sus datos.",
        )

        formulario = ctk.CTkScrollableFrame(self.contenido, fg_color=COLOR_PANEL)

        formulario.pack(fill="both", expand=True, padx=35, pady=10)

        self.campos_servicio = {}

        ctk.CTkLabel(
            formulario, text="Tipo de servicio", font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=25, pady=(15, 5))

        self.tipo_servicio = ctk.CTkOptionMenu(
            formulario,
            values=["Reserva de sala", "Alquiler de equipo", "Asesoria"],
            command=self.actualizar_campos_servicio,
            width=420,
            height=40,
        )

        self.tipo_servicio.pack(anchor="w", padx=25, pady=5)

        campos = [
            ("Identificador", "Ejemplo: 101"),
            ("Nombre", "Nombre del servicio"),
            ("Descripcion", "Descripcion del servicio"),
            ("Precio base", "Ejemplo: 50000"),
        ]

        for etiqueta, placeholder in campos:

            self.crear_campo_servicio(formulario, etiqueta, placeholder)

        self.campos_extra = ctk.CTkFrame(formulario, fg_color="transparent")

        self.campos_extra.pack(fill="x")

        self.actualizar_campos_servicio(self.tipo_servicio.get())

        botones = ctk.CTkFrame(formulario, fg_color="transparent")

        botones.pack(anchor="w", padx=25, pady=20)

        self.crear_boton(
            botones, "Guardar servicio", self.registrar_servicio_interfaz
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones, "Volver", self.mostrar_servicios, COLOR_SECUNDARIO
        ).pack(side="left", padx=5)

    # =================================================
    # CREAR CAMPOS DE SERVICIOS
    # =================================================

    def crear_campo_servicio(self, contenedor, etiqueta, placeholder, diccionario=None):

        if diccionario is None:
            diccionario = self.campos_servicio

        ctk.CTkLabel(
            contenedor,
            text=etiqueta,
            font=("Segoe UI", 13, "bold"),
            text_color=COLOR_TEXTO,
        ).pack(anchor="w", padx=25, pady=(10, 3))

        entrada = ctk.CTkEntry(
            contenedor, width=420, height=40, placeholder_text=placeholder
        )

        entrada.pack(anchor="w", padx=25, pady=5)

        diccionario[etiqueta] = entrada

    # =================================================
    # ACTUALIZAR CAMPOS SEGUN EL TIPO
    # =================================================

    def actualizar_campos_servicio(self, tipo):

        for widget in self.campos_extra.winfo_children():
            widget.destroy()

        self.campos_especiales = {}

        if tipo == "Reserva de sala":

            self.crear_campo_servicio(
                self.campos_extra, "Capacidad", "Ejemplo: 30", self.campos_especiales
            )

        elif tipo == "Alquiler de equipo":

            self.crear_campo_servicio(
                self.campos_extra,
                "Cantidad disponible",
                "Ejemplo: 10",
                self.campos_especiales,
            )

        elif tipo == "Asesoria":

            self.crear_campo_servicio(
                self.campos_extra,
                "Especialidad",
                "Ejemplo: Desarrollo de software",
                self.campos_especiales,
            )

    # =================================================
    # REGISTRAR SERVICIO
    # =================================================

    def registrar_servicio_interfaz(self):

        try:

            identificador_texto = self.campos_servicio["Identificador"].get().strip()

            nombre = self.campos_servicio["Nombre"].get().strip()

            descripcion = self.campos_servicio["Descripcion"].get().strip()

            precio_texto = self.campos_servicio["Precio base"].get().strip()

            if not all([identificador_texto, nombre, descripcion, precio_texto]):

                raise ValueError("Todos los campos generales son obligatorios.")

            identificador = int(identificador_texto)

            precio = float(precio_texto)

            if identificador <= 0 or precio <= 0:

                raise ValueError(
                    "El identificador y el precio deben ser mayores que cero."
                )

            if not nombre.strip() or not descripcion.strip():

                raise ValueError("El nombre y la descripcion son obligatorios.")

            tipo = self.tipo_servicio.get()

            if tipo == "Reserva de sala":

                capacidad_texto = self.campos_especiales["Capacidad"].get().strip()

                capacidad = int(capacidad_texto)

                if capacidad <= 0:

                    raise ValueError("La capacidad debe ser mayor que cero.")

                servicio = ReservaSala(
                    identificador, nombre, descripcion, precio, capacidad
                )

            elif tipo == "Alquiler de equipo":

                cantidad_texto = (
                    self.campos_especiales["Cantidad disponible"].get().strip()
                )

                cantidad = int(cantidad_texto)

                if cantidad < 0:

                    raise ValueError("La cantidad no puede ser negativa.")

                servicio = AlquilerEquipo(
                    identificador, nombre, descripcion, precio, cantidad
                )

            elif tipo == "Asesoria":

                especialidad = self.campos_especiales["Especialidad"].get().strip()

                if not especialidad:

                    raise ValueError("La especialidad es obligatoria.")

                servicio = Asesoria(
                    identificador, nombre, descripcion, precio, especialidad
                )

            else:

                raise ValueError("El tipo de servicio seleccionado no es valido.")

            resultado = self.sistema.registrar_servicio(servicio)

            logging.info("Servicio registrado: %s", identificador)

            messagebox.showinfo("Registro exitoso", str(resultado))

            self.mostrar_servicios()

        except Exception as error:

            logging.exception("Error al registrar servicio.")

            messagebox.showerror("Error de registro", str(error))

    # =================================================
    # MODULO DE RESERVAS
    # =================================================

    def mostrar_reservas(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Gestion de reservas", "Administra y consulta las reservas registradas."
        )

        botones = ctk.CTkFrame(self.contenido, fg_color="transparent")

        botones.pack(fill="x", padx=35, pady=10)

        self.crear_boton(botones, "+ Crear reserva", self.formulario_reserva).pack(
            side="left", padx=5
        )

        self.crear_boton(
            botones,
            "Confirmar reserva",
            lambda: self.formulario_estado_reserva("confirmar"),
            COLOR_EXITO,
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones,
            "Cancelar reserva",
            lambda: self.formulario_estado_reserva("cancelar"),
            COLOR_ERROR,
        ).pack(side="left", padx=5)

        tabla = ctk.CTkScrollableFrame(self.contenido, fg_color=COLOR_PANEL)

        tabla.pack(fill="both", expand=True, padx=35, pady=15)

        encabezados = ["ID", "CLIENTE", "SERVICIO", "DURACION", "COSTO", "ESTADO"]

        for columna, encabezado in enumerate(encabezados):

            tabla.grid_columnconfigure(columna, weight=1)

            ctk.CTkLabel(
                tabla,
                text=encabezado,
                font=("Segoe UI", 11, "bold"),
                text_color="#60A5FA",
            ).grid(row=0, column=columna, padx=8, pady=12)

        try:

            reservas = self.sistema.listar_reservas()

            if not reservas:

                ctk.CTkLabel(
                    tabla,
                    text="No hay reservas registradas.",
                    text_color=COLOR_TEXTO_SECUNDARIO,
                ).grid(row=1, column=0, columnspan=6, pady=30)

                return

            for fila, reserva in enumerate(reservas, start=1):

                datos = [
                    reserva.identificador,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    f"{reserva.duracion} horas",
                    f"${reserva.costo:,.2f}",
                    str(reserva.estado),
                ]

                for columna, dato in enumerate(datos):

                    ctk.CTkLabel(
                        tabla,
                        text=str(dato),
                        text_color=COLOR_TEXTO,
                        font=("Segoe UI", 11),
                    ).grid(row=fila, column=columna, padx=8, pady=12)

        except Exception as error:

            logging.exception("Error al consultar reservas.")

            messagebox.showerror("Error de consulta", str(error))

    # =================================================
    # FORMULARIO DE RESERVAS
    # =================================================

    def formulario_reserva(self):

        self.limpiar_contenido()

        self.crear_titulo(
            "Crear nueva reserva",
            "Ingrese los datos necesarios para registrar una reserva.",
        )

        formulario = ctk.CTkScrollableFrame(self.contenido, fg_color=COLOR_PANEL)

        formulario.pack(fill="both", expand=True, padx=35, pady=10)

        self.campos_reserva = {}

        campos = [
            ("Identificador", "Ejemplo: 201"),
            ("ID del cliente", "Ejemplo: 1"),
            ("ID del servicio", "Ejemplo: 101"),
            ("Duracion", "Ejemplo: 2"),
        ]

        for etiqueta, placeholder in campos:

            ctk.CTkLabel(
                formulario,
                text=etiqueta,
                font=("Segoe UI", 13, "bold"),
                text_color=COLOR_TEXTO,
            ).pack(anchor="w", padx=25, pady=(12, 3))

            entrada = ctk.CTkEntry(
                formulario, width=420, height=40, placeholder_text=placeholder
            )

            entrada.pack(anchor="w", padx=25, pady=5)

            self.campos_reserva[etiqueta] = entrada

        botones = ctk.CTkFrame(formulario, fg_color="transparent")

        botones.pack(anchor="w", padx=25, pady=25)

        self.crear_boton(
            botones, "Guardar reserva", self.registrar_reserva_interfaz
        ).pack(side="left", padx=5)

        self.crear_boton(
            botones, "Volver", self.mostrar_reservas, COLOR_SECUNDARIO
        ).pack(side="left", padx=5)

    # =================================================
    # REGISTRAR RESERVA
    # =================================================

    def registrar_reserva_interfaz(self):

        try:

            identificador = int(self.campos_reserva["Identificador"].get().strip())

            cliente_id = int(self.campos_reserva["ID del cliente"].get().strip())

            servicio_id = int(self.campos_reserva["ID del servicio"].get().strip())

            duracion_texto = self.campos_reserva["Duracion"].get().strip().lower()

            if not duracion_texto:

                raise ValueError("La duracion es obligatoria.")

            partes = duracion_texto.split()

            if len(partes) > 2:

                raise ValueError("Ingrese la duracion en formato: 2 o 2 horas.")

            duracion = int(partes[0])

            if len(partes) == 2 and partes[1] not in ("hora", "horas"):

                raise ValueError("La unidad de duracion debe ser hora u horas.")

            if min(identificador, cliente_id, servicio_id, duracion) <= 0:

                raise ValueError(
                    "Todos los identificadores y la duracion "
                    "deben ser mayores que cero."
                )

            resultado = self.sistema.crear_reserva(
                identificador, cliente_id, servicio_id, duracion
            )

            logging.info("Reserva creada correctamente: %s", identificador)

            messagebox.showinfo("Reserva exitosa", resultado.mostrar_informacion())

            self.mostrar_reservas()

        except Exception as error:

            logging.exception("Error al registrar reserva.")

            messagebox.showerror("Error de reserva", str(error))

    # =================================================
    # FORMULARIO DE CONFIRMACION Y CANCELACION
    # =================================================

    def formulario_estado_reserva(self, operacion):

        self.limpiar_contenido()

        titulo = "Confirmar reserva" if operacion == "confirmar" else "Cancelar reserva"

        color = COLOR_EXITO if operacion == "confirmar" else COLOR_ERROR

        self.crear_titulo(titulo, "Ingrese el identificador de la reserva.")

        formulario = ctk.CTkFrame(
            self.contenido, fg_color=COLOR_PANEL, corner_radius=12
        )

        formulario.pack(fill="x", padx=35, pady=20)

        ctk.CTkLabel(
            formulario,
            text="Identificador de la reserva",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=25, pady=(25, 5))

        self.campo_id_reserva = ctk.CTkEntry(
            formulario, width=420, height=40, placeholder_text="Ejemplo: 201"
        )

        self.campo_id_reserva.pack(anchor="w", padx=25, pady=10)

        metodo = (
            self.confirmar_reserva_interfaz
            if operacion == "confirmar"
            else self.cancelar_reserva_interfaz
        )

        ctk.CTkButton(
            formulario,
            text=titulo,
            height=42,
            width=200,
            fg_color=color,
            command=metodo,
        ).pack(anchor="w", padx=25, pady=15)

        ctk.CTkButton(
            formulario,
            text="Volver a reservas",
            height=40,
            width=200,
            fg_color=COLOR_SECUNDARIO,
            command=self.mostrar_reservas,
        ).pack(anchor="w", padx=25, pady=(0, 25))

    # =================================================
    # CONFIRMAR RESERVA
    # =================================================

    def confirmar_reserva_interfaz(self):

        try:

            texto = self.campo_id_reserva.get().strip()

            if not texto:

                raise ValueError("Debe ingresar el identificador de la reserva.")

            if not texto.isdigit():

                raise ValueError("El identificador debe ser numerico.")

            identificador = int(texto)

            if identificador <= 0:

                raise ValueError("El identificador debe ser mayor que cero.")

            resultado = self.sistema.confirmar_reserva(identificador)

            logging.info("Reserva confirmada: %s", identificador)

            messagebox.showinfo("Confirmacion exitosa", str(resultado))

            self.mostrar_reservas()

        except Exception as error:

            logging.exception("Error al confirmar reserva.")

            messagebox.showerror("Error de confirmacion", str(error))

    # =================================================
    # CANCELAR RESERVA
    # =================================================

    def cancelar_reserva_interfaz(self):

        try:

            texto = self.campo_id_reserva.get().strip()

            if not texto:

                raise ValueError("Debe ingresar el identificador de la reserva.")

            if not texto.isdigit():

                raise ValueError("El identificador debe ser numerico.")

            identificador = int(texto)

            if identificador <= 0:

                raise ValueError("El identificador debe ser mayor que cero.")

            respuesta = messagebox.askyesno(
                "Confirmar cancelacion", "¿Esta seguro de cancelar esta reserva?"
            )

            if not respuesta:
                return

            resultado = self.sistema.cancelar_reserva(identificador)

            logging.info("Reserva cancelada: %s", identificador)

            messagebox.showinfo("Cancelacion exitosa", str(resultado))

            self.mostrar_reservas()

        except Exception as error:

            logging.exception("Error al cancelar reserva.")

            messagebox.showerror("Error de cancelacion", str(error))

    # =================================================
    # CERRAR APLICACION
    # =================================================

    def cerrar_aplicacion(self):

        try:

            respuesta = messagebox.askyesno(
                "Cerrar Software FJ", "¿Desea salir del sistema?"
            )

            if respuesta:

                self.sistema.cerrar_sistema()

                logging.info("Software FJ cerrado correctamente.")

                self.destroy()

        except Exception as error:

            logging.exception("Error al cerrar Software FJ.")

            messagebox.showerror("Error", str(error))


# =====================================================
# EJECUCION PRINCIPAL
# =====================================================

if __name__ == "__main__":

    logging.basicConfig(
        filename="software_fj.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )

    try:

        aplicacion = VentanaPrincipal()

        aplicacion.mainloop()

    except Exception as error:

        logging.exception("Error critico al ejecutar Software FJ.")

        messagebox.showerror(
            "Error del sistema",
            "No fue posible iniciar Software FJ. " "Consulte el archivo de registros.",
        )
