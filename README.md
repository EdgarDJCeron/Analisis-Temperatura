# Analisis-Temperatura
Este proyecto demuestra el uso avanzado de Numpy aplicando el análisis de datos meteorológicos históricos. Obtiene información del último año de cualquier parte del mundo y realiza análisis estadísticos completos, detecta patrones climáticos y genera visualizaciones interactivas.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.20+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

### ✨ Características principales

- 📊 **Estadísticas descriptivas**: Media, mediana, desviación estándar, percentiles
- 🌡️ **Análisis de temperaturas**: Máximas, mínimas, amplitudes térmicas
- 🌧️ **Análisis de precipitación**: Días lluviosos, totales mensuales, intensidades
- 💨 **Análisis de viento**: Velocidades máximas y patrones
- 🔥 **Detección de olas de calor**: Períodos prolongados de temperaturas extremas
- 🥶 **Detección de olas de frío**: Identificación de períodos fríos
- 🔗 **Correlaciones**: Análisis de relaciones entre variables climáticas
- 📈 **Análisis por temporadas**: Comparación trimestral
- 📊 **Visualizaciones**: 6 gráficos interactivos con Matplotlib


## 🛠️ Instalación

### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Dependencias
```bash
pip install numpy matplotlib requests
```

O usando el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
numpy>=1.20.0
matplotlib>=3.3.0
requests>=2.25.0
```

### Personalizar ubicación

Edita las siguientes variables en el código:
```python
# Coordenadas (ejemplo: Ciudad de México)
latitud = 19.4326
longitud = -99.1332
ciudad = "Ciudad de México"
```

**Ejemplos de otras ciudades:**

| Ciudad | Latitud | Longitud |
|--------|---------|----------|
| Madrid | 40.4168 | -3.7038 |
| Buenos Aires | -34.6037 | -58.3816 |
| New York | 40.7128 | -74.0060 |
| Tokyo | 35.6762 | 139.6503 |
| Londres | 51.5074 | -0.1278 |

### Personalizar período de análisis
```python
# Cambiar el rango de días (por defecto: 365)
fecha_fin = datetime.now()
fecha_inicio = fecha_fin - timedelta(days=730)  # 2 años
```

## 📊 Salida del Programa

### Consola
El programa muestra un informe detallado con:
- Estadísticas de temperatura (media, máx, mín, desviación estándar)
- Amplitud térmica diaria
- Análisis por trimestres
- Análisis de precipitación (total anual, días lluviosos)
- Análisis de viento (velocidades máximas)
- Detección de olas de calor y frío
- Matriz de correlaciones entre variables

### Gráficos
Genera 6 visualizaciones:
1. **Evolución de temperaturas** (máx, mín, media)
2. **Precipitación diaria**
3. **Velocidad del viento**
4. **Histograma de distribución de temperatura**
5. **Amplitud térmica diaria**
6. **Box plot comparativo por trimestre**

## 🌐 API Utilizada

**Open-Meteo Archive API**
- URL: https://archive-api.open-meteo.com/v1/archive
- Documentación: https://open-meteo.com/en/docs/historical-weather-api

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Ideas para contribuir:
- [ ] Añadir más variables meteorológicas (humedad, presión)
- [ ] Implementar comparación entre múltiples ciudades
- [ ] Agregar predicción básica con regresión lineal
- [ ] Exportar resultados a CSV/Excel
- [ ] Crear dashboard interactivo
- [ ] Tests unitarios

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

Tu Nombre
- GitHub: [@EdgarDJCeron](https://github.com/EdgarDJCeron)
- LinkedIn: [Edgar de Jesus Ceron Espinosa]([https://www.linkedin.com/in/edgar-ceron09/)

## 🙏 Agradecimientos

- [Open-Meteo](https://open-meteo.com/) por proporcionar la API gratuita
- [NumPy](https://numpy.org/) por la biblioteca de computación científica
- [Matplotlib](https://matplotlib.org/) por las herramientas de visualización

## 📚 Recursos Adicionales

- [Documentación de NumPy](https://numpy.org/doc/)
- [Tutorial de NumPy](https://numpy.org/doc/stable/user/quickstart.html)
- [Documentación de Matplotlib](https://matplotlib.org/stable/contents.html)
- [API de Open-Meteo](https://open-meteo.com/en/docs)

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

**Última actualización**: Octubre 2025
