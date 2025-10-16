import numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta

print("Obteniendo datos meteorológicos...")

latitud = 19.18095
longitud = -96.1429
ciudad = "Veracruz, México"

fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=365)

url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitud,
    "longitude": longitud,
    "start_date": fecha_inicio.strftime("%Y-%m-%d"),
    "end_date": fecha_fin.strftime("%Y-%m-%d"),
    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,windspeed_10m_max",
    "timezone": "America/Mexico_City"
}

try:
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    datos = response.json()

    fechas = np.array(datos['daily']['time'])
    temp_max = np.array(datos['daily']['temperature_2m_max'])
    temp_min = np.array(datos['daily']['temperature_2m_min'])
    temp_media = np.array(datos['daily']['temperature_2m_mean'])
    precipitacion = np.array(datos['daily']['precipitation_sum'])
    viento = np.array(datos['daily']['windspeed_10m_max'])

    print(f"Datos obtenidos correctamente para {ciudad}.")
    print(f"Periodo: {fechas[0]} a {fechas[-1]}")
    print(f"Número de días: {len(fechas)}")

except Exception as e:
    print("Error al obtener los datos:", e)
    exit()

print("\n" + "=" * 70)
print(f"Análisis de datos meteorológicos para {ciudad.upper()}")
print("=" * 70)

print(f"ESTADÍSTICAS DE TEMPERATURA (°C):")
print(f"    Temperatura media anual: {np.mean(temp_media):.2f} °C")
print(f"    Temperatura máxima Absoluta: {np.max(temp_max):.2f} °C (Día {np.argmax(temp_max)+1})")
print(f"    Temperatura mínima absoluta: {np.min(temp_min):.2f} °C (Día {np.argmin(temp_min)+1})")
print(f"    Desviación estándar: {np.std(temp_media):.2f} °C")
print(f"    Rango térmico anual: {np.max(temp_max) - np.min(temp_min):.2f} °C")

amplitud_diaria = temp_max - temp_min
print(f"\n    AMPLITUD TÉRMICA DIARIA:")
print(f"    Amplitud promedio: : {np.mean(amplitud_diaria):.2f} °C")
print(f"    Amplitud máxima: {np.max(amplitud_diaria):.2f} °C (Día {np.argmax(amplitud_diaria)+1})")
print(f"    Amplitud mínima: {np.min(amplitud_diaria):.2f} °C (Día {np.argmin(amplitud_diaria)+1})")

num_dias = len(temp_media)
trimestre_size = num_dias // 4
estaciones = ['Trimestre 1 (Octo-Dic)', 'Trimestre 2 (Ene-Mar)', 'Trimestre 3 (Abr-Jun)', 'Trimestre 4 (Jul-Sep)']

print(f"\n    TEMPERATURA PROMEDIO POR TRIMESTRE:")
for i in range(4):
    inicio = i * trimestre_size
    fin = (i + 1) * trimestre_size if i < 3 else num_dias
    temp_trimestre = temp_media[inicio:fin]
    print(f"    {estaciones[i]}: {np.mean(temp_trimestre):.2f} °C" + f"(MAX: {np.max(temp_trimestre):.2f} °C, MIN: {np.min(temp_trimestre):.2f} °C)")

total_precipitacion = np.sum(precipitacion)
dias_lluvia = np.count_nonzero(precipitacion > 0)
dias_lluvia_fuerte = np.count_nonzero(precipitacion >= 10)

print(f"\n    ESTADÍSTICAS DE PRECIPITACIÓN:")
print(f"    Precipitación total anual: {total_precipitacion:.2f} mm")
print(f"    Número de días con lluvia: {dias_lluvia} días ({(dias_lluvia / num_dias) * 100:.2f} % del año)")
print(f"    Número de días con lluvia fuerte (>=10mm): {dias_lluvia_fuerte}")
if dias_lluvia > 0:
    print(f"    Precipitación promedio en días con lluvia: {np.mean(precipitacion[precipitacion > 0]):.2f} mm")
    print(f"    Día con mayor precipitación: Día {np.max(precipitacion) +1} ({np.max(precipitacion):.2f} mm)")

precipitacion_mensual = []
for i in range(0, num_dias, 30):
    fin = min(i + 30, num_dias)
    precipitacion_mensual.append(np.sum(precipitacion[i:fin]))
mes_mas_lluvioso = np.argmax(precipitacion_mensual)
print(f"    periodo más lluvioso: Días {mes_mas_lluvioso*30 + 1} a {(mes_mas_lluvioso+1)*30} " + f"({precipitacion_mensual[mes_mas_lluvioso]:.2f} mm)")

print(f"\n    ESTADÍSTICAS DE VIENTO (km/h):")
print(f"    Velocidad máxima promedio: {np.mean(viento):.2f} km/h")
print(f"    Velocidad máxima absoluta: {np.max(viento):.2f} km/h (Día {np.argmax(viento)+1})")
print(f"    Desviación estándar: {np.std(viento):.2f} km/h")

dias_con_viento_fuerte = np.count_nonzero(viento > 30)
print(f"    Número de días con viento fuerte (>30 km/h): {dias_con_viento_fuerte} ({(dias_con_viento_fuerte / num_dias) * 100:.1f} % del año)")

umbral_calor = np.percentile(temp_max, 90)
dias_calor_extremo = np.count_nonzero(temp_max > umbral_calor)

olas_calor = []
contador = 0
inicio = -1
for i, es_caluroso in enumerate(temp_max > umbral_calor):
    if es_caluroso:
       if contador == 0:
           inicio = i
       contador += 1
    else:
        if contador >= 3:
            olas_calor.append((inicio, contador, np.mean(temp_max[inicio:inicio+contador])))
        contador = 0
if contador >= 3:
    olas_calor.append((inicio, contador, np.mean(temp_max[inicio:inicio+contador])))

print(f"\n    OLAS DE CALOR (3+ días consecutivos  > {umbral_calor:.1f} °C):")
print(f"      Número de olas de calor: {len(olas_calor)}")
for inicio, duracion, temp_promedio in olas_calor:
    print(f"      OLA: Días {inicio+1} a {inicio+duracion} (Duración: {duracion} días, Temp. Promedio: {temp_promedio:.1f} °C)")

umbral_frio = np.percentile(temp_min, 10)
dias_frios = temp_min < umbral_frio

olas_frio = []
contador = 0
inicio = 0
for i, es_frio in enumerate(dias_frios):
    if es_frio:
        if contador == 0:
            inicio = i
        contador += 1
    else:
        if contador >= 3:
            olas_frio.append((inicio, contador, np.mean(temp_min[inicio:inicio+contador])))
        contador = 0
if contador >= 3:
    olas_frio.append((inicio, contador, np.mean(temp_min[inicio:inicio+contador])))

print(f"\n OLAS DE FRÍO (3+ días consecutivos <{umbral_frio:.1f}°C):")
print(f"   Número de olas de frío: {len(olas_frio)}")
for inicio, duracion, temp_prom in olas_frio:
    print(f"   - Días {inicio + 1} a {inicio + duracion}: {duracion} días " +
          f"(temp. promedio: {temp_prom:.1f}°C)")

print(f"\n ANÁLISIS DE CORRELACIONES:")
corr_temp_precip = np.corrcoef(temp_media, precipitacion)[0, 1]
corr_temp_viento = np.corrcoef(temp_media, viento)[0, 1]
corr_precip_viento = np.corrcoef(precipitacion, viento)[0, 1]

print(f"   Temperatura vs Precipitación: {corr_temp_precip:.3f}")
print(f"   Temperatura vs Viento: {corr_temp_viento:.3f}")
print(f"   Precipitación vs Viento: {corr_precip_viento:.3f}")

print(f"\n DISTRIBUCIÓN POR PERCENTILES (Temperatura Media):")
percentiles = [10, 25, 50, 75, 90]
for p in percentiles:
    valor = np.percentile(temp_media, p)
    print(f"   Percentil {p}: {valor:.2f}°C")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle(f'Análisis Meteorológico Anual - {ciudad}', fontsize=16, fontweight='bold')

dias_num = np.arange(len(fechas))

axes[0, 0].plot(dias_num, temp_max, color='red', linewidth=1, label='Máxima', alpha=0.7)
axes[0, 0].plot(dias_num, temp_min, color='blue', linewidth=1, label='Mínima', alpha=0.7)
axes[0, 0].plot(dias_num, temp_media, color='orange', linewidth=1.5, label='Media')
axes[0, 0].fill_between(dias_num, temp_min, temp_max, alpha=0.2, color='gray')
axes[0, 0].axhline(np.mean(temp_media), color='black', linestyle='--', linewidth=1, label='Promedio anual')
axes[0, 0].set_xlabel('Día del año')
axes[0, 0].set_ylabel('Temperatura (°C)')
axes[0, 0].set_title('Evolución de Temperaturas')
axes[0, 0].legend(loc='best', fontsize=8)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].bar(dias_num, precipitacion, color='steelblue', alpha=0.7, width=1)
axes[0, 1].axhline(np.mean(precipitacion[precipitacion > 0]) if dias_lluvia > 0 else 0, 
                   color='red', linestyle='--', linewidth=1, label='Promedio días lluvia')
axes[0, 1].set_xlabel('Día del año')
axes[0, 1].set_ylabel('Precipitación (mm)')
axes[0, 1].set_title('Precipitación Diaria')
axes[0, 1].legend(fontsize=8)
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].plot(dias_num, viento, color='green', linewidth=1, alpha=0.7)
axes[0, 2].axhline(np.mean(viento), color='red', linestyle='--', linewidth=1, label='Promedio')
axes[0, 2].axhline(30, color='orange', linestyle='--', linewidth=1, label='Umbral ventoso')
axes[0, 2].set_xlabel('Día del año')
axes[0, 2].set_ylabel('Velocidad máxima (km/h)')
axes[0, 2].set_title('Velocidad del Viento')
axes[0, 2].legend(fontsize=8)
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].hist(temp_media, bins=25, color='coral', edgecolor='black', alpha=0.7)
axes[1, 0].axvline(np.mean(temp_media), color='red', linestyle='--', linewidth=2, 
                   label=f'Media: {np.mean(temp_media):.1f}°C')
axes[1, 0].axvline(np.median(temp_media), color='blue', linestyle='--', linewidth=2,
                   label=f'Mediana: {np.median(temp_media):.1f}°C')
axes[1, 0].set_xlabel('Temperatura (°C)')
axes[1, 0].set_ylabel('Frecuencia (días)')
axes[1, 0].set_title('Distribución de Temperatura Media')
axes[1, 0].legend(fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(dias_num, amplitud_diaria, color='purple', linewidth=1, alpha=0.7)
axes[1, 1].axhline(np.mean(amplitud_diaria), color='red', linestyle='--', linewidth=1,
                   label=f'Promedio: {np.mean(amplitud_diaria):.1f}°C')
axes[1, 1].set_xlabel('Día del año')
axes[1, 1].set_ylabel('Amplitud térmica (°C)')
axes[1, 1].set_title('Amplitud Térmica Diaria')
axes[1, 1].legend(fontsize=8)
axes[1, 1].grid(True, alpha=0.3)

temp_por_trimestre = []
for i in range(4):
    inicio = i * trimestre_size
    fin = (i + 1) * trimestre_size if i < 3 else num_dias
    temp_por_trimestre.append(temp_media[inicio:fin])

axes[1, 2].boxplot(temp_por_trimestre, labels=['T1', 'T2', 'T3', 'T4'])
axes[1, 2].set_xlabel('Trimestre')
axes[1, 2].set_ylabel('Temperatura (°C)')
axes[1, 2].set_title('Distribución por Trimestre')
axes[1, 2].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print(" Análisis completado con éxito")
print("=" * 70)