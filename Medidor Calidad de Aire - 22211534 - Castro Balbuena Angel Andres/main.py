# ---------------------------------------------------------------------------------
#  Medidor de Calidad del Aire con MicroPython
#  Autor: Castro Balbuena Angel Andres
#  Descripción: Utiliza un sensor MQ135 para medir la calidad del aire
#               y muestra los valores en un display OLED. Usa un LED RGB
#               para indicar visualmente la calidad del aire.
# ---------------------------------------------------------------------------------

from machine import Pin, I2C, ADC, PWM
import ssd1306
import time
import math

# Configuración de los pines
mq135_pin = ADC(26)  # Sensor MQ135 en GP26 (ADC0)

# LED RGB (Común Cátodo)
led_r = PWM(Pin(18))
led_g = PWM(Pin(19))
led_b = PWM(Pin(20))

# Inicializar PWM para los LEDs
led_r.freq(1000)
led_g.freq(1000)
led_b.freq(1000)

# Configuración del display OLED
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Constantes para la calibración del sensor MQ135
CALIBRACION_R0 = 76.63  # Resistencia R0 en aire limpio
RL_VALOR = 10.0  # Valor de la resistencia de carga RL en KOhms

# Umbral para determinar la calidad del aire
NIVEL_BUENO = 400
NIVEL_REGULAR = 1000
NIVEL_MALO = 2000

# Variables para el sistema
lecturas = []
max_lecturas = 10  # Número de lecturas para promediar

def establecer_color_rgb(r, g, b):
    """Establece el color del LED RGB (0-255 para cada canal)"""
    # Convertir a rango de 0-65535 para PWM
    r_pwm = int(r * 65535 / 255)
    g_pwm = int(g * 65535 / 255)
    b_pwm = int(b * 65535 / 255)
    
    led_r.duty_u16(r_pwm)
    led_g.duty_u16(g_pwm)
    led_b.duty_u16(b_pwm)

def obtener_resistencia_sensor():
    """Calcula la resistencia del sensor basado en la lectura analógica"""
    lectura = mq135_pin.read_u16()
    voltaje = lectura * (3.3 / 65535)
    
    # Fórmula para calcular la resistencia del sensor (Rs)
    if voltaje == 0:
        return float('inf')
    
    rs = RL_VALOR * (3.3 - voltaje) / voltaje
    return rs

def calcular_ppm():
    """Calcula la concentración equivalente de CO2 en ppm"""
    rs = obtener_resistencia_sensor()
    ratio = rs / CALIBRACION_R0
    
    # Fórmula para estimar ppm de CO2 (aproximada)
    if ratio == 0:
        return 0
    
    ppm = 116.6020682 * math.pow(ratio, -2.769034857)
    
    # Limitar el rango a valores razonables
    if ppm < 350:
        ppm = 350
    elif ppm > 10000:
        ppm = 10000
        
    return ppm

def obtener_calidad_aire(ppm):
    """Determina la calidad del aire basado en ppm"""
    if ppm < NIVEL_BUENO:
        return "BUENA", (0, 255, 0)  # Verde
    elif ppm < NIVEL_REGULAR:
        return "REGULAR", (255, 255, 0)  # Amarillo
    elif ppm < NIVEL_MALO:
        return "MALA", (255, 165, 0)  # Naranja
    else:
        return "PELIGROSA", (255, 0, 0)  # Rojo

def dibujar_grafico(valores, y_base, altura):
    """Dibuja un gráfico de líneas en el display OLED"""
    if not valores:
        return
    
    # Encontrar el valor máximo y mínimo para escalar
    max_val = max(valores)
    min_val = min(valores)
    rango = max(max_val - min_val, 1)
    
    # Dibujar ejes
    oled.hline(0, y_base + altura, 128, 1)
    oled.vline(0, y_base, altura, 1)
    
    # Dibujar líneas del gráfico
    for i in range(len(valores) - 1):
        x1 = int(i * 128 / (len(valores) - 1))
        y1 = y_base + altura - int((valores[i] - min_val) * altura / rango)
        x2 = int((i + 1) * 128 / (len(valores) - 1))
        y2 = y_base + altura - int((valores[i + 1] - min_val) * altura / rango)
        
        oled.line(x1, y1, x2, y2, 1)

# Inicialización del display
oled.fill(0)
oled.text("Iniciando...", 0, 0)
oled.text("Medidor de", 0, 15)
oled.text("Calidad del Aire", 0, 25)
oled.text("Calibrando...", 0, 45)
oled.show()

# Tiempo de calentamiento/estabilización
for i in range(30, 0, -1):
    oled.fill_rect(0, 55, 128, 9, 0)
    oled.text("Espere: {}s".format(i), 0, 55)
    oled.show()
    time.sleep(1)

while True:
    try:
        # Obtener valor de PPM
        ppm_actual = calcular_ppm()
        
        # Agregar a la lista de lecturas para promediar
        lecturas.append(ppm_actual)
        if len(lecturas) > max_lecturas:
            lecturas.pop(0)
        
        # Calcular promedio
        ppm_promedio = sum(lecturas) / len(lecturas)
        
        # Obtener calidad del aire y color LED
        calidad, color = obtener_calidad_aire(ppm_promedio)
        
        # Establecer color del LED RGB
        establecer_color_rgb(color[0], color[1], color[2])
        
        # Actualizar display
        oled.fill(0)
        oled.text("CALIDAD DEL AIRE", 0, 0)
        oled.text("CO2: {} ppm".format(int(ppm_promedio)), 0, 15)
        oled.text("Estado: {}".format(calidad), 0, 25)
        
        # Mostrar gráfico de tendencia
        dibujar_grafico(lecturas, 35, 20)
        
        oled.show()
    except Exception as e:
        # En caso de error, mostrar mensaje
        oled.fill(0)
        oled.text("Error:", 0, 0)
        oled.text(str(e)[:16], 0, 10)
        oled.text(str(e)[16:32], 0, 20)
        oled.show()
    
    time.sleep(1)