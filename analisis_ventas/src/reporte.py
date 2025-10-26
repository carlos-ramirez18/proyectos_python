from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import os

def generar_reporte(metricas, rutas_graficos, ruta_salida):
    """
    Genera un informe PDF con las métricas y los gráficos del análisis de ventas.
    metricas: dict con las métricas calculadas
    rutas_graficos: lista con las rutas de las imágenes generadas
    ruta_salida: ruta donde se guardará el PDF final
    """
    # Crear directorio de salida si no existe
    carpeta = os.path.dirname(ruta_salida)
    if carpeta and not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Configurar documento
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    elementos = []
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos["Title"]
    estilo_normal = estilos["Normal"]

    # --- Título principal ---
    elementos.append(Paragraph("Informe de Ventas", estilo_titulo))
    elementos.append(Spacer(1, 12))

    # --- Métricas ---
    elementos.append(Paragraph("Resumen de métricas principales:", estilo_normal))
    elementos.append(Spacer(1, 12))

    data = [["Métrica", "Valor"]]
    for clave, valor in metricas.items():
        data.append([clave, str(valor)])

    tabla = Table(data, colWidths=[8*cm, 7*cm])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 24))

    # --- Gráficos ---
    elementos.append(Paragraph("Visualizaciones:", estilo_normal))
    elementos.append(Spacer(1, 12))

    for ruta in rutas_graficos:
        if os.path.exists(ruta):
            elementos.append(Image(ruta, width=14*cm, height=8*cm))
            elementos.append(Spacer(1, 12))

    # --- Generar PDF ---
    try:
        doc.build(elementos)
        print(f"Informe PDF generado correctamente en: {ruta_salida}")
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
