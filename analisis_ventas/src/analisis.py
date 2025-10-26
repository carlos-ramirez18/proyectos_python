import pandas as pd

def cargar_datos(ruta_csv):
    """
    Carga los datos del archivo CSV de ventas.
    Devuelve un DataFrame de pandas o None si hay un error.
    """
    try:
        df = pd.read_csv(ruta_csv)
        print(f"Archivo cargado correctamente ({len(df)} registros).")
        return df
    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV en la ruta indicada.")
    except pd.errors.EmptyDataError:
        print("Error: El archivo CSV está vacío.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
    return None


def calcular_metricas(df):
    """
    Calcula algunas métricas básicas de las ventas a partir del DataFrame.
    Retorna un diccionario con resultados.
    """
    metricas = {}

    # Verificamos que el DataFrame tenga las columnas esperadas
    columnas_necesarias = {"fecha", "producto", "categoria", "cantidad", "precio_unitario", "vendedor"}
    if not columnas_necesarias.issubset(df.columns):
        print("El archivo CSV no contiene todas las columnas necesarias.")
        print(f"Columnas esperadas: {columnas_necesarias}")
        return {}

    # Calcular el total de ventas (cantidad * precio_unitario)
    df["venta_total"] = df["cantidad"] * df["precio_unitario"]

    # Total de ventas
    metricas["Total de ventas ($)"] = round(df["venta_total"].sum(), 2)

    # Promedio de venta por transacción
    metricas["Promedio por venta ($)"] = round(df["venta_total"].mean(), 2)

    # Producto más vendido
    producto_top = df.groupby("producto")["venta_total"].sum().idxmax()
    metricas["Producto más vendido"] = producto_top

    # Categoría más rentable
    categoria_top = df.groupby("categoria")["venta_total"].sum().idxmax()
    metricas["Categoría más rentable"] = categoria_top

    # Día con mayor facturación
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    dia_top = df.groupby("fecha")["venta_total"].sum().idxmax().strftime("%Y-%m-%d")
    metricas["Día con mayor facturación"] = dia_top

    return metricas
