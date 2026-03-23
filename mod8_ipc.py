# mod8_ipc.py
from decimal import Decimal, ROUND_HALF_UP

def ajustar_precio(precio_actual, variacion_ipc):
    variacion_decimal = Decimal(str(variacion_ipc))
    factor = Decimal("1") + (variacion_decimal / Decimal("100"))
    nuevo_precio = precio_actual * factor
    return nuevo_precio.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)



