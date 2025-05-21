# ---------------------------------------------------------------------------------
#  Detector de Movimiento con MicroPython
#  Alumno: Castro Balbuena Angel Andres
#  Descripción: Utiliza un sensor PIR para detectar movimiento y muestra
#               el estado en un display OLED. También activa un buzzer
#               como alarma cuando se detecta movimiento.
# ---------------------------------------------------------------------------------

from machine import Pin, I2C, PWM
import ssd1306
import time

# Configuración de los pines
pir_sensor = Pin(16, Pin.IN)  # Sensor PIR en GP16
buzzer = PWM(Pin(17))  # Buzzer en GP17
led = Pin(25, Pin.OUT)  # LED integrado en Pico

# Configuración del display OLED
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Variables para el sistema
tiempo_alarma = 0
alarma_activa = False
detecciones = 0
umbral_sensibilidad = 5  # Número de detecciones para considerar movimiento real
ultimo_movimiento = 0

def sonar_alarma(frecuencia=1000, duracion=300):
    """Activa el buzzer con la frecuencia especificada"""
    buzzer.freq(frecuencia)
    buzzer.duty_u16(32768)  # 50% duty cycle
    time.sleep_ms(duracion)
    buzzer.duty_u16(0)

def actualizar_display(movimiento_detectado, tiempo_ultimo, contador):
    """Actualiza la información en el display OLED"""
    oled.fill(0)
    oled.text("DETECTOR MOVIM.", 0, 0)
    
    if movimiento_detectado:
        oled.fill_rect(0, 15, 128, 14, 1)
        oled.text("MOVIMIENTO!", 10, 18, 0)
    else:
        oled.text("Sin movimiento", 0, 15)
    
    # Tiempo desde última detección
    if tiempo_ultimo > 0:
        segundos = time.ticks_diff(time.ticks_ms(), tiempo_ultimo) // 1000
        oled.text("Ultimo: {} seg".format(segundos), 0, 30)
    else:
        oled.text("Esperando...", 0, 30)
    
    # Contador de eventos
    oled.text("Eventos: {}".format(contador), 0, 45)
    
    # Barra de estado del sistema
    oled.rect(0, 57, 128, 7, 1)
    if alarma_activa:
        for i in range(0, 128, 8):
            oled.fill_rect(i, 57, 4, 7, 1)
    
    oled.show()

# Inicialización del display
oled.fill(0)
oled.text("Iniciando...", 0, 0)
oled.text("Sistema de", 0, 15)
oled.text("deteccion de", 0, 25)
oled.text("movimiento", 0, 35)
oled.show()
time.sleep(2)

while True:
    movimiento = pir_sensor.value()
    tiempo_actual = time.ticks_ms()
    
    # Verificar si hay movimiento
    if movimiento == 1:
        led.value(1)  # Encender LED
        detecciones += 1
        
        if detecciones >= umbral_sensibilidad and not alarma_activa:
            # Activar alarma
            alarma_activa = True
            tiempo_alarma = tiempo_actual
            ultimo_movimiento = tiempo_actual
            sonar_alarma(1500, 200)
            time.sleep_ms(100)
            sonar_alarma(2000, 200)
    else:
        led.value(0)  # Apagar LED
        
        # Reducir contador de detecciones gradualmente
        if detecciones > 0 and time.ticks_diff(tiempo_actual, tiempo_alarma) > 500:
            detecciones -= 1
    
    # Desactivar alarma después de 5 segundos
    if alarma_activa and time.ticks_diff(tiempo_actual, tiempo_alarma) > 5000:
        alarma_activa = False
    
    # Actualizar display
    actualizar_display(alarma_activa, ultimo_movimiento, detecciones)
    
    # Si la alarma está activa, hacer sonar el buzzer intermitentemente
    if alarma_activa:
        if time.ticks_diff(tiempo_actual, tiempo_alarma) % 1000 < 200:
            sonar_alarma(1000, 100)
    
    time.sleep_ms(100)