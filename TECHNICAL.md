# Documentación Técnica

## Arquitectura del Sistema

### Flujo de datos

```
CSV (Export) ──┐
              ├──> Procesamiento ──> Merge ──> Agrupación ──> Output
Excel Base ──┤
(Recetario)  │
             └──> Normalización
```

### Componentes principales

#### 1. **Entrada de datos**

```python
# Carga de CSV de ventas
df_ventas = pd.read_csv(uploaded_file)
# Columnas esperadas: ID, Producto, Cantidad
```

#### 2. **Estandarización**

Los datos se transforman en varias fases:

- **Capitalización**: Todos los nombres se capitalizan
- **Normalización de variantes**: Se unifican nombres similares
  - "Entraña" → "Entrana"
  - "patita" → "Patitas"
  - "sp", "s.p.", "s.p" → "Viña San Pedro" (en Pedidos)
- **Limpieza**: Se eliminan espacios en blanco innecesarios

#### 3. **Merge y cálculo**

```python
# Proceso de cruce de datos
merged = ventas.merge(
    recetario[['ID', 'Productos Cocina', 'Factor']],
    on='ID',
    how='left'
)

# Cálculo del consumo total
merged['VENTA_TOTAL'] = merged['Cantidad'] * merged['Factor']

# Agrupación por producto
consumo_agrupado = merged.groupby('Productos Cocina')['VENTA_TOTAL'].sum()
```

#### 4. **Salida**

```python
# Merge final con inventario base
inventario_final = output.merge(
    consumo_agrupado,
    on='Productos Cocina',
    how='left'
).fillna(0)
```

## Integración con Google Sheets

### Flujo de autenticación

```
Service Account JSON ──> Credenciales ──> OAuth2 ──> Google Sheets API
```

### Proceso de sincronización

1. **Autenticación**

   ```python
   creds = Credentials.from_service_account_file(
       'casona-key.json',
       scopes=['spreadsheets', 'drive']
   )
   ```

2. **Conexión**

   ```python
   client = gspread.authorize(creds)
   spreadsheet = client.open_by_key(sheet_id)
   ```

3. **Actualización**
   ```python
   worksheet = spreadsheet.worksheet('INICIO/FIN/DIF')
   worksheet.update('E3:E{n}', valores)
   ```

## Estructura de datos

### Entrada: export.csv

| ID  | Producto     | Cantidad |
| --- | ------------ | -------- |
| 1   | Carne Molida | 5        |
| 2   | Filete       | 3        |

### Referencia: Recetario.xlsx

| ID  | Nombre Producto | Productos Cocina | Factor |
| --- | --------------- | ---------------- | ------ |
| 1   | Carne Molida    | Carne Molida     | 1.0    |
| 2   | Filete          | Filete           | 0.95   |

### Salida: Resultado_Inventario.xlsx

| Productos Cocina | VENTA |
| ---------------- | ----- |
| Carne Molida     | 5.00  |
| Filete           | 2.85  |

## Tratamiento de errores

### Validaciones principales

```python
# 1. Archivos requeridos
if not os.path.exists('output.xlsx'):
    raise FileNotFoundError("output.xlsx no encontrado")

# 2. Columnas requeridas
required_cols = ['ID', 'Producto', 'Cantidad']
if not all(col in df.columns for col in required_cols):
    raise ValueError("Columnas faltantes")

# 3. Datos válidos
df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce')
df = df.dropna(subset=['Cantidad'])
```

## Performance

### Optimizaciones

- **Merge en una sola pasada**: Usa `merge()` en lugar de loops
- **Groupby eficiente**: Agrupación vectorizada con pandas
- **Caching de Streamlit**: Uso de `@st.cache_data` para archivos base

### Complejidad computacional

| Operación     | Complejidad |
| ------------- | ----------- |
| Carga CSV     | O(n)        |
| Normalización | O(n)        |
| Merge         | O(n log n)  |
| Groupby       | O(n)        |
| Google Sheets | O(n)        |

**Total**: O(n log n) donde n = número de registros

## Seguridad

### Credenciales

```
✅ HACER:
- Guardar casona-key.json en .gitignore
- Usar variables de entorno para credenciales
- Revisar permisos de la Service Account

❌ NO HACER:
- Versionar archivos JSON
- Hardcodear credenciales
- Compartir tokens públicamente
```

### Validación de entrada

- Se validan tipos de datos
- Se normalizan strings
- Se filtran valores nulos
- Se convierten tipos automáticamente

## Extensibilidad

### Agregar nuevas transformaciones

```python
# 1. Crear función de transformación
def transformar_producto(nombre):
    # Lógica aquí
    return nombre_transformado

# 2. Aplicar en el pipeline
df['Productos Cocina'] = df['Productos Cocina'].apply(transformar_producto)
```

### Agregar nuevas páginas

```
pages/
├── Nueva_Pagina.py  # Streamlit detecta automáticamente
└── Pedidos.py
```

## Testing

### Casos de prueba sugeridos

```python
def test_carga_csv():
    """Verifica carga correcta de CSV"""
    pass

def test_normalizado_datos():
    """Verifica estandarización"""
    pass

def test_calculo_consumo():
    """Verifica cálculo de VENTA_TOTAL"""
    pass

def test_merge_datos():
    """Verifica cruce de datos"""
    pass

def test_conexion_google_sheets():
    """Verifica conexión a Google Sheets"""
    pass
```

## Logs y debugging

### Información de depuración

Habilita logs en `streamlit:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Comandos útiles

```bash
# Ejecutar en modo debug
streamlit run app.py --logger.level=debug

# Ver configuración
streamlit config show

# Limpiar cache
streamlit cache clear
```

---

**Última actualización:** Marzo 2026
