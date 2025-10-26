import os
import pandas as pd
import matplotlib.pyplot as plt

def generar_graficos(df, guardar=False):
    """
    Genera gráficos a partir del DataFrame de ventas.
    Si guardar=True, los guarda en la carpeta /output y devuelve sus rutas.
    """
    rutas = []
    carpeta_salida = "./output/graficos/"

    if guardar and not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Asegurarse de que exista la columna de ventas totales
    if "venta_total" not in df.columns:
        df["venta_total"] = df["cantidad"] * df["precio_unitario"]

    # Convertir fechas
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    # --- Gráfico 1: Ventas totales por mes ---
    ventas_mensuales = df.groupby(df["fecha"].dt.to_period("M"))["venta_total"].sum()
    plt.figure(figsize=(8, 4))
    ventas_mensuales.plot(kind="bar")
    plt.title("Ventas totales por mes")
    plt.xlabel("Mes")
    plt.ylabel("Monto total ($)")
    plt.tight_layout()
    if guardar:
        ruta1 = os.path.join(carpeta_salida, "ventas_mensuales.png")
        plt.savefig(ruta1)
        rutas.append(ruta1)
    else:
        plt.show()
    plt.close()

    # --- Gráfico 2: Top 5 productos más vendidos ---
    productos_top = df.groupby("producto")["venta_total"].sum().nlargest(5)
    plt.figure(figsize=(8, 4))
    productos_top.plot(kind="bar", color="orange")
    plt.title("Top 5 productos más vendidos")
    plt.xlabel("Producto")
    plt.ylabel("Ventas ($)")
    plt.tight_layout()
    if guardar:
        ruta2 = os.path.join(carpeta_salida, "top_productos.png")
        plt.savefig(ruta2)
        rutas.append(ruta2)
    else:
        plt.show()
    plt.close()

    # --- Gráfico 3: Ventas por categoría ---
    ventas_categoria = df.groupby("categoria")["venta_total"].sum()
    plt.figure(figsize=(6, 6))
    ventas_categoria.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Distribución de ventas por categoría")
    plt.ylabel("")
    plt.tight_layout()
    if guardar:
        ruta3 = os.path.join(carpeta_salida, "ventas_categoria.png")
        plt.savefig(ruta3)
        rutas.append(ruta3)
    else:
        plt.show()
    plt.close()

    return rutas
