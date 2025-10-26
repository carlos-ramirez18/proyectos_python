import os
from analisis import cargar_datos, calcular_metricas
from graficos import generar_graficos
from reporte import generar_reporte

def limpiar_consola():
    # limpieza pantalla
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_menu():
    print("=== Sistema de Análisis de Ventas ===")
    print("1. Mostrar métricas en consola")
    print("2. Generar gráficos")
    print("3. Generar informe PDF")
    print("4. Salir")

def main():
    ruta_csv = "data/ventas.csv"
    ruta_pdf = "output/informe_ventas.pdf"

    # Cargar datos
    df = cargar_datos(ruta_csv)
    if df is None:
        print("No se pudo cargar el archivo CSV. Verifica la ruta y el formato.")
        return

    while True:
        limpiar_consola()
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        limpiar_consola()

        if opcion == "1":
            # Mostrar métricas en consola
            metricas = calcular_metricas(df)
            print("--- Métricas de Ventas ---")
            for clave, valor in metricas.items():
                print(f"{clave}: {valor}")
            input("\nPresiona Enter para volver al menú...")

        elif opcion == "2":
            # Generar gráficos
            print("Generando gráficos...")
            rutas = generar_graficos(df, guardar=True)
            if rutas:
                print("Gráficos generados en la carpeta 'output':")
                for r in rutas:
                    print(f" - {r}")
            else:
                print("No se generaron gráficos.")
            input("\nPresiona Enter para volver al menú...")

        elif opcion == "3":
            # Generar PDF completo
            print("Generando informe PDF...")
            metricas = calcular_metricas(df)
            rutas_graficos = generar_graficos(df, guardar=True)
            generar_reporte(metricas, rutas_graficos, ruta_pdf)
            input("\nPresiona Enter para volver al menú...")

        elif opcion == "4":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intenta nuevamente.")
            input("\nPresiona Enter para volver al menú...")

if __name__ == "__main__":
    main()
