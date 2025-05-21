# ---------------------------------------------------------------------------------
#  Lenguajes de Interfaz en TECNM Campus ITT
#  Autor: Castro Balbuena Angel Andres
#  Fecha: 2025-05-20
#  Descripción:  Indicador de luz con niveles.
#               Muestra si hay oscuridad, luz media o alta.
# ---------------------------------------------------------------------------------

from machine import ADC, Pin, I2C
import ssd1306
import time

ldr = ADC(26)
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    luz = ldr.read_u16()
    
    if luz < 10000:
        nivel = "Oscuro"
    elif luz < 40000:
        nivel = "Medio"
    else:
        nivel = "Luminoso"

    oled.fill(0)
    oled.text("Luz: {}".format(nivel), 0, 0)
    oled.text("Valor: {}".format(luz), 0, 10)
    oled.show()
    time.sleep(1)
