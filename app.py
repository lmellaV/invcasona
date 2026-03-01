import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="Procesador de Inventario", layout="wide")
st.title("📊 Procesador de Inventario Cocina")

# --- LÓGICA DE CARGA DE ARCHIVOS LOCALES ---
def cargar_archivos_locales():
    if os.path.exists('output.xlsx') and os.path.exists('Recetario.xlsx'):
        out = pd.read_excel('output.xlsx')
        df_recetario = pd.read_excel('Recetario.xlsx')
        return out, df_recetario
    else:
        return None, None

out_local, df_local = cargar_archivos_locales()

# Verificar que los archivos locales existan antes de continuar
if out_local is None or df_local is None:
    st.error("❌ No se encontraron 'output.xlsx' o 'Recetario.xlsx' en la carpeta local.")
else:
    # --- INTERFAZ DE CARGA (DRAG & DROP) ---
    st.info("Archivos locales cargados correctamente. Por favor, sube el reporte de ventas.")
    uploaded_file = st.file_uploader("Arrastra aquí el archivo 'export.csv'", type=["csv"])

    if uploaded_file is not None:
        try:
            # 1. Cargar el CSV subido por el usuario
            de = pd.read_csv(uploaded_file)
            
            # 2. Procesar 'Output' (Local)
            out = out_local.iloc[:, :1].copy()
            out['Productos'] = out['Productos'].str.capitalize()
            out.rename(columns={'Productos': 'Productos Cocina'}, inplace=True)
            out['Productos Cocina'] = out['Productos Cocina'].str.replace('Entraña', 'Entrana', case=False)

            # 3. Procesar 'Recetario' (Local)
            df = df_local.copy()
            df.dropna(subset=['ID', 'Nombre Producto'], inplace=True)
            df.rename(columns={'Nombre Producto': 'Producto'}, inplace=True)
            df['ID'] = df['ID'].astype(str).str.strip()
            df['Productos Cocina'] = df['Productos Cocina'].astype(str).str.strip()
            df['Productos Cocina'] = df['Productos Cocina'].str.replace(r'(?i)\bpatita\b', 'Patitas', regex=True)
            df['Productos Cocina'] = df['Productos Cocina'].str.capitalize()

            # 4. Procesar 'Export' (Subido)
            de = de[['ID', 'Producto', 'Cantidad']].copy()
            de['ID'] = de['ID'].astype(str).str.strip()

            # 5. Cruce de datos (Merge)
            merged = de.merge(df[['ID', 'Productos Cocina', 'Factor']], on='ID', how='left')
            merged['VENTA_TOTAL'] = merged['Cantidad'] * merged['Factor']

            consumo_agrupado = merged.groupby('Productos Cocina')['VENTA_TOTAL'].sum().reset_index()

            # 6. Inventario Final
            inventario_final = out.merge(consumo_agrupado, on='Productos Cocina', how='left').fillna(0)
            inventario_final.rename(columns={'VENTA_TOTAL': 'VENTA'}, inplace=True)

            # --- MOSTRAR RESULTADOS ---
            st.success("✅ Procesamiento completado con éxito.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vista Previa del Resultado")
                st.dataframe(inventario_final, use_container_width=True)
            
            with col2:
                st.subheader("Acciones")
                # Botón para descargar a Excel
                output_path = "Resultado_Inventario.xlsx"
                inventario_final.to_excel(output_path, index=False)
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Inventario en Excel",
                        data=file,
                        file_name="inventario_final_cocina.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

        except Exception as e:
            st.error(f"Error al procesar los datos: {e}")