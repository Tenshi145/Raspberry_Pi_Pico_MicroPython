# ---------------------------------------------------------------------------------
#  Lenguajes de Interfaz en TECNM Campus ITT
#  Autor: Castro Balbuena Angel Andres
#  Fecha: 2025-05-13
#  Descripción: Práctica #7 - Termometro
# ---------------------------------------------------------------------------------

from machine import Pin, I2C
import ssd1306
import dht
import time

sensor = dht.DHT22(Pin(15))
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    sensor.measure()
    temp = sensor.temperature()
    
    if temp < 20:
        nivel = "Fria"
    elif temp > 30:
        nivel = "Caliente"
    else:
        nivel = "Normal"

    oled.fill(0)
    oled.text("Temp: {:.1f}C".format(temp), 0, 0)
    oled.text("Nivel: {}".format(nivel), 0, 10)
    oled.show()
    time.sleep(2)
