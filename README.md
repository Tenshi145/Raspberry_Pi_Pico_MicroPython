# Raspberry Pi Pico MicroPython

Colección de proyectos y ejemplos utilizando MicroPython con Raspberry Pi Pico en el simulador Wokwi.

## Proyectos Disponibles

### 1. Medidor de Luz con LDR
**Descripción:** Sistema que mide la intensidad de luz utilizando un fotorresistor (LDR).  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431500465856806913)


### 2. Sensor PIR
**Descripción:** Detector de movimiento utilizando un sensor PIR.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431501164265124865)


### 3. Sensor de Distancia
**Descripción:** Medidor de distancia utilizando un sensor ultrasónico.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431501918493400065)


### 4. Sensor de Temperatura
**Descripción:** Monitor de temperatura ambiente usando un sensor digital.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431500977049188353)


### 5. Sensor Distancia/Contador
**Descripción:** Sistema que mide distancia y cuenta objetos detectados.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431514282076962817)

### 6. Temperatura: Fría/Normal/Caliente
**Descripción:** Medidor de temperatura con clasificación de rangos.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431514896794216449)


### 7. LDR: Oscuro/Medio/Luminoso
**Descripción:** Detector de niveles de luz con clasificación.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431541410940085249)


### 8. Estación Meteorológica
**Descripción:** Sistema completo que muestra datos meteorológicos.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431543937245718529)


### 9. Detector de Movimiento
**Descripción:** Sistema avanzado para detección de intrusos con alarma.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431544346475665409)


### 10. Medidor de Calidad de Aire
**Descripción:** Monitoreo de calidad del aire con indicación visual.  
**Simulador:** [Ver en Wokwi](https://wokwi.com/projects/431545464361765889)


## Guías de Conexión

### Conexión de DHT22 (Sensor de Temperatura y Humedad)
```
DHT22          Raspberry Pi Pico
------         ----------------
VCC    ------> 3V3 (Pin 36)
DATA   ------> GP15 (Pin 20)
GND    ------> GND (cualquier pin GND)
```

### Conexión de MQ135 (Sensor de Calidad de Aire)
```
MQ135          Raspberry Pi Pico
-----          ----------------
VCC    ------> VBUS (5V) o 3V3 (Pin 36)
AOUT   ------> GP26 (Pin 31) / ADC0
GND    ------> GND (cualquier pin GND)
DOUT   ------> No conectado
```

### Conexión de Pantalla OLED SSD1306
```
OLED           Raspberry Pi Pico
----           ----------------
VCC    ------> 3V3 (Pin 36)
GND    ------> GND (cualquier pin GND)
SDA    ------> GP4 (Pin 6)
SCL    ------> GP5 (Pin 7)
```

### Conexión de LDR (Fotorresistor)
```
LDR            Raspberry Pi Pico
---            ----------------
VCC    ------> 3V3 (Pin 36)
GND    ------> GND (cualquier pin GND)
AO     ------> GP26/ADC0 (Pin 31)
```

## Recursos Adicionales

- [Documentación oficial de MicroPython](https://docs.micropython.org/)
- [Pinout de Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/Pico-R3-A4-Pinout.pdf)
- [Tutorial de Wokwi para Raspberry Pi Pico](https://docs.wokwi.com/guides/raspberry-pi-pico)

---

*Nota: Los enlaces proporcionados dirigen a simulaciones en Wokwi donde se pueden ver y probar los proyectos. Cada proyecto incluye el código fuente completo y el diagrama de conexiones.*
