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
invcasona/
├── app.py                          # Punto de entrada principal
├── README.md                       # Documentación del proyecto
├── CHANGELOG.md                    # Historial de versiones
├── CONTRIBUTING.md                 # Guía de contribución
├── TECHNICAL.md                    # Documentación técnica
├── requirements.txt                # Dependencias del proyecto
├── .gitignore                      # Archivos ignorados por Git
│
├── invcasona/
│   ├── Inventarios.py             # Aplicación principal con Google Sheets
│   ├── Recetario.xlsx             # Mapeo de productos y factores de conversión
│   ├── Output.xlsx                # Inventario base de productos
│   ├── Resultado_Inventario.xlsx  # Resultado del último procesamiento
│   ├── casona-key.json            # 🔐 Credenciales de Google (NO versionar)
│   ├── temp_credentials.json      # 🔐 Credenciales temporales (NO versionar)
│   ├── Prueba.ipynb              # Notebook de pruebas y desarrollo
│   ├── pages/
│   │   └── Pedidos.py            # Página: Generador de pedidos por proveedor
│   └── __pycache__/               # Caché de Python
│
└── .streamlit/
    └── config.toml                # Configuración visual de Streamlit
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

#### 2. **Output.xlsx** (invcasona/)

Archivo con la lista de productos disponibles:

- `Productos` - Nombre del producto base

#### 3. **export.csv** (invcasona/)

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

### Ejecutar la aplicación (desde la raíz del proyecto)

```bash
streamlit run app.py
```

**Nota:** El archivo `app.py` en la raíz actúa como punto de entrada y redirige automáticamente a `Inventarios.py` en la carpeta `invcasona/` con las rutas configuradas correctamente.

Accede a `http://localhost:8501` en tu navegador.

### Estructura de Streamlit

- **Página principal**: `Inventarios.py` (con integración de Google Sheets)
- **Página secundaria**: `pages/Pedidos.py` (Generador de pedidos por proveedor)

Las páginas en la carpeta `pages/` se cargan automáticamente en Streamlit.

## 📝 Flujo de trabajo

1. **Cargar archivos base** - El programa lee automáticamente `Recetario.xlsx` y `Output.xlsx` desde la carpeta `invcasona/`
2. **Subir reporte de ventas** - Arrastra el archivo `export.csv` a la interfaz (o sube uno nuevo)
3. **Procesamiento automático**:
   - Limpia y estandariza los datos
   - Cruza ventas con factores de conversión
   - Calcula consumo total por producto
4. **Descargar resultados** - Obtén el Excel con los datos procesados (`Resultado_Inventario.xlsx`)
5. **(Opcional) Enviar a Google Sheets** - Proporciona la URL de tu Google Sheet y los datos se actualizan en la columna E de la hoja "INICIO/FIN/DIF"

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
