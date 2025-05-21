# ---------------------------------------------------------------------------------
#  Lenguajes de Interfaz en TECNM Campus ITT
#  Autor: Castro Balbuena Angel Andres
#  Fecha: 2025-05-13
#  Descripción: Práctica - Medidor de luz con LDR y pantalla OLED SSD1306.
#               El programa lee la intensidad de luz mediante un sensor LDR y
#               muestra el porcentaje de luminosidad en una pantalla OLED.
# ---------------------------------------------------------------------------------

from machine import Pin, ADC, I2C
from time import sleep
import ssd1306

# Configuración del sensor LDR
ldr = ADC(Pin(26))  # GP26 es ADC0

# Configuración de la pantalla OLED
i2c = I2C(0, scl=Pin(5), sda=Pin(4))  # GP5 = SCL, GP4 = SDA
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

while True:
    # Lectura del valor analógico del LDR
    valor_ldr = ldr.read_u16()
    porcentaje_luz = (1 - (valor_ldr / 65535)) * 100  # Invertido para Wokwi


    # Mostrar en la pantalla OLED
    oled.fill(0)  # Limpiar pantalla
    oled.text("Sensor de Luz", 0, 0)
    oled.text("Luminosidad:", 0, 20)
    oled.text("{:.2f}%".format(porcentaje_luz), 0, 40)
    oled.show()

    sleep(1)
