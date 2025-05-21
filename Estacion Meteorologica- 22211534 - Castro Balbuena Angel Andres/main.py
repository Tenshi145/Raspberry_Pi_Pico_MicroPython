# ---------------------------------------------------------------------------------
#  Estación Meteorológica Simple con MicroPython
#  Alumno: Castro Balbuena Angel Andres 
#  Descripción: Muestra temperatura y humedad en una pantalla OLED
#               utilizando un sensor DHT22. También muestra alertas
#               cuando la temperatura o humedad alcanzan ciertos niveles.
# ---------------------------------------------------------------------------------

from machine import Pin, I2C
import ssd1306
import dht
import time

# Configuración de los pines
sensor = dht.DHT22(Pin(15))  # DHT22 conectado al pin GP15
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Umbral para alertas
TEMP_ALTA = 30
TEMP_BAJA = 10
HUM_ALTA = 70
HUM_BAJA = 30

def obtener_alerta_temp(temp):
    if temp > TEMP_ALTA:
        return "CALOR"
    elif temp < TEMP_BAJA:
        return "FRIO"
    else:
        return "NORMAL"

def obtener_alerta_hum(hum):
    if hum > HUM_ALTA:
        return "HUMEDO"
    elif hum < HUM_BAJA:
        return "SECO"
    else:
        return "NORMAL"

def dibujar_barra(y, valor, max_valor=100):
    # Dibuja una barra de progreso horizontal
    ancho_barra = min(int(valor * 100 / max_valor), 100)
    oled.rect(0, y, 100, 10, 1)
    if ancho_barra > 0:
        oled.fill_rect(0, y, ancho_barra, 10, 1)
    return y + 12

while True:
    try:
        # Lectura del sensor
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()
        
        # Alerta para temperatura y humedad
        alerta_temp = obtener_alerta_temp(temperatura)
        alerta_hum = obtener_alerta_hum(humedad)
        
        # Limpiar pantalla
        oled.fill(0)
        
        # Mostrar datos
        oled.text("ESTACION METEO", 0, 0)
        oled.text("Temp: {:.1f} C".format(temperatura), 0, 16)
        oled.text("Estado: {}".format(alerta_temp), 0, 26)
        
        # Barra para temperatura (0-50°C)
        y_pos = dibujar_barra(36, temperatura, 50)
        
        oled.text("Hum: {:.1f} %".format(humedad), 0, y_pos)
        oled.text("Estado: {}".format(alerta_hum), 0, y_pos + 10)
        
        oled.show()
    except Exception as e:
        # En caso de error, mostrar mensaje
        oled.fill(0)
        oled.text("Error sensor", 0, 0)
        oled.text(str(e), 0, 10)
        oled.show()
    
    time.sleep(2)