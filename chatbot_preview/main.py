import customtkinter as ctk
from src.chatbot import Chatbot

# Iconos por categoría
ICONOS = {
    "horarios": "🕒",
    "turnos": "📅",
    "emergencias": "🚑",
    "especialidades": "🩺",
    "obras sociales": "💳",
    "ubicacion": "📍",
    "default": "❓"
}

BOTONES_RAPIDOS = ["horarios", "turnos", "emergencias", "especialidades", "obras sociales", "ubicacion"]

# Frases de botones para que coincidan con patrones
FRASES_BOTONES = {
    "horarios": "Necesito saber el horario de atención",
    "turnos": "Quiero sacar un turno",
    "emergencias": "Tengo una emergencia",
    "especialidades": "Qué especialidades médicas tienen",
    "obras sociales": "Aceptan obra social o prepaga",
    "ubicacion": "Dónde están ubicados"
}

class AsistenteUI:
    def __init__(self):
        self.bot = Chatbot()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Asistente Médico Virtual")
        self.root.geometry("600x800")

        # Título
        self.label_titulo = ctk.CTkLabel(
            self.root, text="Centro Médico Salud Total", font=("Segoe UI", 20, "bold")
        )
        self.label_titulo.pack(pady=10)

        # Frame chat
        self.chat_frame = ctk.CTkScrollableFrame(self.root, width=560, height=500, corner_radius=10)
        self.chat_frame.pack(pady=10)
        self.mensajes_widgets = []

        # Botones rápidos
        self.botones_frame = ctk.CTkFrame(self.root, width=560, height=50)
        self.botones_frame.pack(pady=(0,10))
        self._crear_botones_rapidos()

        # Entrada y botón enviar
        self.entry = ctk.CTkEntry(self.root, placeholder_text="Escribí tu consulta aquí...", width=400)
        self.entry.pack(side="left", padx=(20,0), pady=10)
        self.entry.bind("<Return>", self.enviar_mensaje)

        self.btn_enviar = ctk.CTkButton(self.root, text="Enviar", width=100, command=self.enviar_mensaje)
        self.btn_enviar.pack(side="right", padx=(0,20), pady=10)

        # Mensaje inicial
        self.mostrar_mensaje("Asistente", "Hola, soy tu asistente médico. ¿En qué puedo ayudarte hoy?", "default")

        self.root.mainloop()

    def _crear_botones_rapidos(self):
        for categoria in BOTONES_RAPIDOS:
            btn = ctk.CTkButton(
                self.botones_frame,
                text=categoria.capitalize(),
                width=85,
                command=lambda c=categoria: self.enviar_consulta_rapida(c)
            )
            btn.pack(side="left", padx=5, pady=5)

    def enviar_consulta_rapida(self, categoria):
        mensaje = FRASES_BOTONES.get(categoria, categoria)
        self.mostrar_mensaje("Tú", mensaje)
        respuesta, cat = self.bot.responder(mensaje)
        self.mostrar_mensaje("Asistente", respuesta, cat)

    def mostrar_mensaje(self, remitente, texto, categoria=None):
        if remitente == "Tú":
            color, fg, anchor, texto_final = "#0A84FF", "white", "e", texto
        else:
            color, fg, anchor = "#E5E5EA", "black", "w"
            icono = ICONOS.get(categoria, "❓")
            texto_final = f"{icono} {texto}"

        burbuja = ctk.CTkLabel(
            self.chat_frame,
            text=texto_final,
            fg_color=color,
            text_color=fg,
            corner_radius=15,
            wraplength=400,
            font=("Segoe UI", 11),
            justify="left"
        )
        burbuja.pack(pady=5, padx=10, anchor=anchor)
        self.mensajes_widgets.append(burbuja)

        # Scroll automático
        self.chat_frame._parent_canvas.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1.0)

    def enviar_mensaje(self, event=None):
        mensaje = self.entry.get().strip()
        if mensaje:
            self.mostrar_mensaje("Tú", mensaje)
            respuesta, categoria = self.bot.responder(mensaje)
            self.mostrar_mensaje("Asistente", respuesta, categoria)
            self.entry.delete(0, "end")


if __name__ == "__main__":
    AsistenteUI()
