# ---------------------------------------------------------------------------------
#  Lenguajes de Interfaz en TECNM Campus ITT
#  Autor: Castro Balbuena Angel Andres
#  Fecha: 2025-05-13
#  Descripción: Práctica - Contador de objetos con sensor ultrasónico.
#               Cada objeto detectado a <200cm incrementa el conteo.
# ---------------------------------------------------------------------------------

from machine import Pin, I2C
import ssd1306
import time

trigger = Pin(3, Pin.OUT)
echo = Pin(2, Pin.IN)

i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

contador = 0

def medir_distancia():
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(10)
    trigger.low()
    while echo.value() == 0:
        inicio = time.ticks_us()
    while echo.value() == 1:
        fin = time.ticks_us()
    duracion = fin - inicio
    return (duracion * 0.0343) / 2

while True:
    dist = medir_distancia()
    if dist < 200:
        contador += 1
        time.sleep(1)
    oled.fill(0)
    oled.text("Objetos:", 0, 0)
    oled.text(str(contador), 0, 10)
    oled.show()
    time.sleep(0.2)
