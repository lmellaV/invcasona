# 📊 Procesador de Inventario Cocina

Sistema automatizado de gestión de inventario para cocina que calcula el consumo de ingredientes basándose en reportes de ventas.

## 🎯 Descripción

Este proyecto es una aplicación web construida con **Streamlit** que automatiza el seguimiento del consumo de ingredientes en una cocina/restaurante. Procesa reportes de ventas (CSV), cruza los datos con un recetario que contiene factores de conversión, y genera un inventario final detallado.

### Características principales

✅ **Carga automática de datos** - Lee archivos CSV de ventas y archivos Excel base  
✅ **Estandarización de datos** - Limpia y normaliza nombres de productos  
✅ **Cálculo de consumo** - Multiplica ventas por factores de conversión  
✅ **Agrupación inteligente** - Suma el consumo por tipo de ingrediente  
✅ **Exportación a Excel** - Descarga del inventario procesado  
✅ **Integración Google Sheets** - Envío automático de datos a Google Sheets  
✅ **Generador de pedidos** - Página adicional para crear pedidos por proveedor

## 📋 Requisitos previos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)

### Paquetes requeridos

```
streamlit>=1.28.0
pandas>=1.5.0
openpyxl>=3.10.0
gspread>=5.10.0
google-auth>=2.20.0
```

## 🚀 Instalación

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/tu-usuario/casona-receta.git
cd casona-receta
```

### 2. Crear un ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 📁 Estructura del proyecto

```
casona-receta/
├── app.py                          # Versión simplificada sin Google Sheets
├── README.md                       # Este archivo
├── requirements.txt                # Dependencias del proyecto
├── export.csv                      # Ejemplo de reporte de ventas
├── invcasona/
│   ├── Inventarios.py             # Versión completa con Google Sheets
│   ├── casona-key.json            # Credenciales de Google (no versionar)
│   ├── Recetario.xlsx             # Mapeo de productos y factores
│   ├── output.xlsx                # Inventario base de productos
│   ├── temp_credentials.json      # Credenciales temporales (no versionar)
│   ├── Prueba.ipynb              # Notebook de pruebas
│   └── pages/
│       └── Pedidos.py            # Generador de pedidos por proveedor
```

## 🔧 Configuración

### Archivos requeridos

Para que el programa funcione correctamente, necesitas los siguientes archivos en directorios específicos:

#### 1. **Recetario.xlsx** (invcasona/)

Debe contener una hoja con las siguientes columnas:

- `ID` - Identificador único del producto
- `Nombre Producto` - Nombre del producto vendido
- `Productos Cocina` - Nombre estandarizado en cocina
- `Factor` - Factor de conversión (cantidad en cocina / cantidad vendida)

**Ejemplo:**
| ID | Nombre Producto | Productos Cocina | Factor |
|---|---|---|---|
| 1 | Carne Molida | Carne Molida | 1.0 |
| 2 | Filete | Filete | 0.95 |
| 3 | Patita | Patitas | 2.0 |

#### 2. **output.xlsx** (invcasona/)

Archivo con la lista de productos disponibles:

- `Productos` - Nombre del producto base

#### 3. **export.csv** (carpeta raíz)

Reporte de ventas con:

- `ID` - ID del producto vendido
- `Producto` - Nombre del producto
- `Cantidad` - Cantidad vendida

**Ejemplo:**

```csv
ID,Producto,Cantidad
1,Carne Molida,5
2,Filete,3
```

### Integración con Google Sheets (opcional)

Si deseas usar la función de envío automático a Google Sheets:

1. **Crear una Google Cloud Project**
   - Ve a [Google Cloud Console](https://console.cloud.google.com/)
   - Crea un nuevo proyecto
   - Activa la API de Google Sheets

2. **Generar credenciales**
   - Crea una "Service Account"
   - Descarga el archivo JSON de credenciales
   - Renómbralo como `casona-key.json` y colócalo en la carpeta `invcasona/`

3. **Compartir el Google Sheet**
   - Abre tu Google Sheet
   - Comparte el acceso con el email de la Service Account (encontrado en casona-key.json)

## 🎮 Uso

### Versión simplificada (sin Google Sheets)

```bash
cd invcasona
streamlit run ../app.py
```

### Versión completa (con Google Sheets)

```bash
cd invcasona
streamlit run Inventarios.py
```

Accede a `http://localhost:8501` en tu navegador.

### Generador de Pedidos

La página de pedidos está disponible automáticamente como una página secundaria de Streamlit (requiere la estructura `pages/`).

## 📝 Flujo de trabajo

1. **Cargar archivos base** - El programa lee automáticamente `Recetario.xlsx` y `output.xlsx`
2. **Subir reporte de ventas** - Arrastra el archivo `export.csv` a la interfaz
3. **Procesamiento automático**:
   - Limpia y estandariza los datos
   - Cruza ventas con factores de conversión
   - Calcula consumo total por producto
4. **Descargar resultados** - Obtén el Excel con los datos procesados
5. **(Opcional) Enviar a Google Sheets** - Los datos se actualizan automáticamente en la columna E de la hoja "INICIO/FIN/DIF"

## 🔄 Transformaciones de datos

### Limpieza de datos

- Capitalización de nombres de productos
- Reemplazo de variantes (ej: "Entraña" → "Entrana", "patita" → "Patitas")
- Eliminación de espacios en blanco innecesarios
- Conversión de tipos de datos

### Cálculo de consumo

```
VENTA_TOTAL = Cantidad_Vendida × Factor_Conversión
CONSUMO_AGRUPADO = SUM(VENTA_TOTAL) por Productos Cocina
```

## 📊 Salidas

### Inventario Final

| Productos Cocina | VENTA |
| ---------------- | ----- |
| Carne Molida     | 5.00  |
| Filete           | 2.85  |
| Patitas          | 6.00  |

### Archivos generados

- `Resultado_Inventario.xlsx` - Tabla con el inventario procesado

## 🐛 Troubleshooting

### Error: "No se encontraron 'output.xlsx' o 'Recetario.xlsx'"

- Verifica que los archivos existan en el directorio correcto
- Asegúrate de que los nombres sean exactos (case-sensitive en algunos sistemas)

### Error: "No se encontró la hoja 'INICIO/FIN/DIF'"

- Verifica que el Google Sheet tenga esa hoja exactamente
- Revisa que la Service Account tenga acceso al documento

### El CSV no sube correctamente

- Verifica que el formato sea CSV (no Excel)
- Comprueba que las columnas sean: `ID`, `Producto`, `Cantidad`
- Revisa la codificación del archivo (UTF-8 recomendado)

## 📖 Documentación adicional

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [gspread documentation](https://gspread.readthedocs.io/)

## 👥 Equipo

Desarrollado para la gestión de inventario de la Cocina Casona.

## 📄 Licencia

Este proyecto es propietario. Todos los derechos reservados.

## ✨ Notas finales

- Los datos sensibles como credenciales (`casona-key.json`) **nunca deben** versionarse en Git
- El archivo `.gitignore` debe excluir archivos JSON y archivos temporales
- Realiza backups regulares de tus Google Sheets

---

**Última actualización:** Marzo 2026
