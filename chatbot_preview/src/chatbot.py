import re
import json
import os
from src.datos import RESPUESTAS

class Chatbot:
    def __init__(self):
        self.historial_path = "historial.json"
        self.historial = self._cargar_historial()

        # Patrones regex → categoría
        self.patrones = {
            r"horario|abrir|cerrar|hora|atencion": "horarios",
            r"turno|cita|reserva|pedir|agendar": "turnos",
            r"emergencia|urgencia|auxilio": "emergencias",
            r"especialidad|doctor|medico|area": "especialidades",
            r"obra social|prepaga|plan|seguro": "obras sociales",
            r"donde|ubicacion|direccion|queda": "ubicacion"
        }

    def _cargar_historial(self):
        if os.path.exists(self.historial_path):
            with open(self.historial_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _guardar_historial(self):
        with open(self.historial_path, "w", encoding="utf-8") as f:
            json.dump(self.historial, f, ensure_ascii=False, indent=2)

    def responder(self, mensaje):
        mensaje = mensaje.lower()
        categoria = "default"

        # Buscar coincidencia con patrones
        for patron, clave in self.patrones.items():
            if re.search(patron, mensaje):
                categoria = clave
                break

        respuesta = RESPUESTAS.get(categoria, RESPUESTAS["default"])

        # Guardar en historial
        self.historial.append({"usuario": mensaje, "bot": respuesta})
        self._guardar_historial()

        return respuesta, categoria
