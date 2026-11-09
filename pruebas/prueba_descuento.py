from servicios import ReservaSala, AlquilerEquipo, Asesoria


def probar_descuentos_impuestos():

    servicio = ReservaSala(1, "Sala principal", "Sala de reuniones", 100000, 10)

    costo = servicio.precio_base * 2

    detalle = servicio.calcular_detalle_pago(costo, descuento=10, impuesto=19)

    print("\n===== PRUEBA DE DESCUENTOS E IMPUESTOS =====")

    print(f"Costo base: ${detalle['costo_base']:,.2f}")
    print(f"Descuento: ${detalle['valor_descuento']:,.2f}")
    print(f"Subtotal: ${detalle['subtotal']:,.2f}")
    print(f"Impuesto: ${detalle['valor_impuesto']:,.2f}")
    print(f"Total a pagar: ${detalle['total_pagar']:,.2f}")

    assert detalle["costo_base"] == 200000
    assert detalle["valor_descuento"] == 20000
    assert detalle["subtotal"] == 180000
    assert detalle["valor_impuesto"] == 34200
    assert detalle["total_pagar"] == 214200

    print("\n¡PRUEBA SUPERADA CORRECTAMENTE!")


if __name__ == "__main__":
    probar_descuentos_impuestos()
