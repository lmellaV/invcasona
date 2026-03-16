"""
Punto de entrada principal de la aplicación Procesador de Inventario Cocina
Redirige a la versión completa con integración de Google Sheets
"""
import sys
import os

# Agregar la carpeta invcasona al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'invcasona'))

# Cambiar el directorio de trabajo a invcasona para que las rutas relativas funcionen
os.chdir(os.path.join(os.path.dirname(__file__), 'invcasona'))

# Ejecutar Inventarios.py
exec(open('Inventarios.py').read())
