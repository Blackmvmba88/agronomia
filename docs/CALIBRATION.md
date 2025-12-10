# Guía de Calibración - BlackMamba Smart Farming

Esta guía te ayudará a calibrar correctamente todos los sensores del sistema.

## 🎯 Importancia de la Calibración

Una calibración correcta es fundamental para obtener mediciones precisas y mantener condiciones óptimas para el cultivo hidropónico.

## 📊 Sensor de pH

### Materiales Necesarios
- Soluciones buffer de pH 4.0, 7.0 y 10.0
- Agua destilada para enjuagar
- Papel absorbente

### Procedimiento

1. **Preparación**
   - Enjuagar el sensor con agua destilada
   - Secar suavemente con papel absorbente

2. **Punto de Calibración pH 7.0**
   ```
   a. Sumergir el sensor en buffer pH 7.0
   b. Esperar 30 segundos para estabilización
   c. Abrir Monitor Serial (115200 baudios)
   d. Observar el voltaje reportado
   e. Anotar el valor (ejemplo: 2.48V)
   ```

3. **Ajustar Configuración**
   ```cpp
   // En config/config.h
   #define PH_NEUTRAL_VOLTAGE 2.48  // Tu voltaje medido
   ```

4. **Verificar Calibración**
   ```
   a. Volver a subir el código al ESP32
   b. Sumergir en buffer pH 7.0 → debe leer ~7.0
   c. Sumergir en buffer pH 4.0 → debe leer ~4.0
   d. Sumergir en buffer pH 10.0 → debe leer ~10.0
   ```

5. **Ajuste Fino (si es necesario)**
   
   Si las lecturas de pH 4.0 y 10.0 no son precisas, ajustar la pendiente:
   ```cpp
   // Cambiar 0.18 por un valor diferente
   float pH = 7.0 + ((PH_NEUTRAL_VOLTAGE - voltage) / 0.18);
   ```

### Mantenimiento
- Limpiar el sensor después de cada uso
- Calibrar cada 2-4 semanas
- Almacenar en solución de almacenamiento (KCl 3M)

## ⚡ Sensor de EC (Conductividad Eléctrica)

### Materiales Necesarios
- Solución de calibración EC (1413 µS/cm es estándar)
- Agua destilada
- Termómetro (la EC varía con temperatura)

### Procedimiento

1. **Preparación**
   - Enjuagar el sensor con agua destilada
   - Verificar temperatura de la solución (idealmente 25°C)

2. **Medición de Referencia**
   ```
   a. Sumergir sensor en solución de calibración
   b. Esperar 1 minuto para estabilización
   c. Observar voltaje en Monitor Serial
   d. Anotar voltaje (ejemplo: 1.42V)
   ```

3. **Calcular Factor de Conversión**
   ```
   EC_CONVERSION_FACTOR = EC_conocido / voltaje_medido
   
   Ejemplo:
   1413 µS/cm / 1.42V = 995.07
   ```

4. **Ajustar Configuración**
   ```cpp
   // En config/config.h
   #define EC_CONVERSION_FACTOR 995.07
   ```

5. **Verificar**
   ```
   a. Volver a subir el código
   b. Medir la solución de calibración
   c. Debe leer ~1413 µS/cm
   ```

6. **Verificación Múltiple (recomendado)**
   
   Probar con diferentes concentraciones:
   - 0 µS/cm (agua destilada)
   - 1413 µS/cm (solución estándar)
   - Otra concentración conocida

### Compensación de Temperatura

Si tu sensor EC tiene compensación de temperatura:
```cpp
// Ajustar EC basado en temperatura
float tempCoeff = 0.02;  // 2% por grado Celsius
float ecCompensated = ec * (1 + tempCoeff * (temp - 25.0));
```

### Mantenimiento
- Calibrar mensualmente
- Limpiar con solución ácida suave si hay depósitos
- No dejar secar el sensor

## 🌡️ Sensor de Temperatura (DS18B20)

### Verificación

Los sensores DS18B20 vienen calibrados de fábrica con precisión de ±0.5°C.

1. **Verificar Precisión**
   ```
   a. Preparar baño de hielo (0°C)
   b. Sumergir sensor
   c. Debe leer cerca de 0°C
   
   d. Preparar agua a temperatura corporal (37°C)
   e. Usar termómetro de referencia
   f. Comparar lecturas
   ```

2. **Si hay desviación consistente**
   ```cpp
   // Agregar offset en el código
   float temp = waterTempSensor.getTempCByIndex(0);
   temp = temp + 0.3;  // Ajustar según necesidad
   ```

### Instalación Correcta
- Usar manga termoretráctil o encapsulado impermeable
- Sumergir completamente en el líquido
- Evitar burbujas de aire alrededor del sensor

## 🌡️ Sensor DHT22 (Temperatura y Humedad)

### Verificación

El DHT22 también viene calibrado de fábrica.

1. **Verificar Temperatura**
   - Comparar con termómetro digital de referencia
   - Precisión típica: ±0.5°C

2. **Verificar Humedad**
   ```
   Método 1: Bolsa sellada con sal
   a. Poner sal en un recipiente pequeño
   b. Agregar unas gotas de agua (no disolver completamente)
   c. Colocar sensor y recipiente en bolsa sellada
   d. Esperar 8-12 horas
   e. Debe leer ~75% de humedad relativa
   
   Método 2: Comparar con higrómetro calibrado
   ```

3. **Ajuste si es necesario**
   ```cpp
   float humidity = dht.readHumidity();
   humidity = humidity * 1.05;  // Ajustar ±5% si es necesario
   ```

### Consideraciones
- Evitar luz solar directa
- Mantener alejado de fuentes de calor
- Buena circulación de aire alrededor del sensor

## 💡 Sensor de Luz (LDR)

### Caracterización

El LDR no proporciona valores absolutos en lux sin calibración compleja, pero sirve para monitoreo relativo.

1. **Establecer Rangos**
   ```
   a. Medir con todas las luces apagadas (oscuridad)
      → Valor mínimo (ej: 50)
   
   b. Medir con luces de crecimiento al máximo
      → Valor máximo (ej: 3500)
   
   c. Establecer umbral de "poca luz"
      → Por ejemplo: 1000
   ```

2. **Ajustar en Código**
   ```cpp
   #define LIGHT_MIN 50      // Oscuridad
   #define LIGHT_MAX 3500    // Luz máxima
   #define LIGHT_THRESHOLD 1000  // Umbral para encender luces
   ```

### Calibración con Luxómetro (Opcional)

Si tienes un luxómetro:
1. Medir lux real en diferentes condiciones
2. Anotar valor del LDR correspondiente
3. Crear tabla de conversión o función de mapeo

## 📝 Registro de Calibración

Mantén un registro de tus calibraciones:

```
Fecha: 2024-01-15
Sensor: pH
Solución: Buffer pH 7.0
Voltaje medido: 2.48V
Temperatura: 23°C
Resultados prueba:
  - pH 4.0: Lectura 4.05 ✓
  - pH 7.0: Lectura 7.01 ✓
  - pH 10.0: Lectura 10.15 ✓

Próxima calibración: 2024-02-15
```

## ⚠️ Solución de Problemas

### Lecturas Inestables
- Verificar conexiones eléctricas
- Asegurar buena alimentación (estable)
- Agregar capacitor de desacople (0.1µF) cerca del sensor
- Aumentar tiempo de espera antes de leer

### Lecturas Incorrectas
- Verificar que el sensor esté sumergido completamente
- Limpiar el sensor
- Verificar que no haya burbujas de aire
- Re-calibrar con soluciones frescas

### Drift (Deriva en el Tiempo)
- Normal en sensores electroquímicos
- Calibrar más frecuentemente
- Reemplazar sensor si el drift es excesivo

## 🔄 Frecuencia de Calibración Recomendada

| Sensor | Frecuencia | Notas |
|--------|------------|-------|
| pH | 2-4 semanas | Más frecuente en uso intensivo |
| EC | 1 mes | Calibrar si hay depósitos visibles |
| Temp. Agua | 6 meses | Solo verificación |
| DHT22 | 6 meses | Solo verificación |
| Luz | 1 mes | Re-caracterizar si cambia iluminación |

## 📚 Recursos Adicionales

- [Calibración de pH - Tutorial Detallado](https://www.example.com)
- [Guía de Sensores EC](https://www.example.com)
- [Foro de Soporte BlackMamba](https://www.example.com)

## 💡 Consejos Finales

1. **Siempre calibrar con soluciones frescas** - Las soluciones buffer viejas pierden precisión
2. **Temperatura constante** - Calibrar a la temperatura de operación (20-25°C)
3. **Limpiar antes de calibrar** - Sensores sucios dan lecturas incorrectas
4. **Documentar todo** - Mantén registro de calibraciones y resultados
5. **Verificar regularmente** - Mejor prevenir que corregir problemas
