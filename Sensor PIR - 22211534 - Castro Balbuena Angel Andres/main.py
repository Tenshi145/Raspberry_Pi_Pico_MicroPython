# ---------------------------------------------------------------------------------
#  Lenguajes de Interfaz en TECNM Campus ITT
#  Autor: Castro Balbuena Angel Andres
#  Fecha: 2025-05-13
#  Descripción: Práctica #3 - Detector de movimiento con Raspberry Pi Pico W.
#               Detecta movimiento con sensor PIR y muestra el estado en OLED.
# ---------------------------------------------------------------------------------

from machine import Pin, I2C
import ssd1306
import time

# Configuración del sensor PIR
pir = Pin(14, Pin.IN)

# Configuración de la pantalla OLED
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    oled.fill(0)
    if pir.value():
        oled.text("ALERTA!", 0, 0)
        oled.text("Movimiento", 0, 10)
    else:
        oled.text("Todo tranqui", 0, 0)
    oled.show()
    time.sleep(0.5)
