import tkinter as tk
import customtkinter as ctk
import math
from src.data_manager import obtener_exoplanetas, filtrar_habitables
from src.radar_math import calcular_escala_zoom, coordenadas_polares_a_pixeles
from src.clustering import clasificar_exoplanetas  # Importamos el clustering

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RadarApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. Configuración de pantalla principal
        self.title("LIRA: Exoplanet Radar System")
        self.geometry("950x650")
        self.resizable(False, False)

        # Cargar datos y aplicar clustering
        todos = obtener_exoplanetas()
        filtrados = filtrar_habitables(todos)
        self.planetas_habitables = clasificar_exoplanetas(filtrados)

        # Variables de estado
        self.distancia_max_pc = 200.0
        self.planetas_dibujados = []

        # Layout
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1) 

        self._crear_panel_controles()
        self._crear_lienzo_radar()

        self.canvas_radar.bind("<Button-1>", self._al_hacer_clic)
        self.actualizar_radar()

    def _crear_panel_controles(self):
        self.panel_izquierdo = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_titulo = ctk.CTkLabel(
            self.panel_izquierdo,
            text="SISTEMA LIRA",
            font=ctk.CTkFont(size=16, weight="bold")
        )   
        self.label_titulo.pack(padx=20, pady=15)

        # Slider de Zoom
        self.label_zoom = ctk.CTkLabel(self.panel_izquierdo, text="Rango Visual (pc):", font=ctk.CTkFont(size=12))
        self.label_zoom.pack(padx=20, pady=(10, 0))

        self.slider_zoom = ctk.CTkSlider(
            self.panel_izquierdo,
            from_=50.0,
            to=500.0,
            command=self._cambiar_zoom_slider
        )
        self.slider_zoom.set(200.0)
        self.slider_zoom.pack(padx=20, pady=10)

        # 📄 TARJETA DE INFORMACIÓN DEL PLANETA
        self.frame_tarjeta = ctk.CTkFrame(self.panel_izquierdo, fg_color="#1c2128", corner_radius=8)
        self.frame_tarjeta.pack(padx=15, pady=15, fill="x")

        self.label_nombre_planeta = ctk.CTkLabel(
            self.frame_tarjeta,
            text="Selecciona un mundo",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00ffff"
        )
        self.label_nombre_planeta.pack(padx=10, pady=(10, 5))

        self.label_detalles_planeta = ctk.CTkLabel(
            self.frame_tarjeta,
            text="Haz clic en cualquier punto del radar para ver su telemetría científica.",
            font=ctk.CTkFont(size=11),
            justify="left",
            wraplength=220
        )
        self.label_detalles_planeta.pack(padx=10, pady=(0, 10))

        # Estadísticas rápidas
        self.label_stats = ctk.CTkLabel(
            self.panel_izquierdo,
            text=f"Candidatos: {len(self.planetas_habitables)} mundos",
            font=ctk.CTkFont(size=12),
            text_color="#8b949e"
        )
        self.label_stats.pack(padx=20, pady=10, side="bottom")

    def _crear_lienzo_radar(self):
        self.canvas_radar = tk.Canvas(
            self,
            width=550,
            height=550,
            bg="#0d1117",
            highlightthickness=0
        )
        self.canvas_radar.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def _cambiar_zoom_slider(self, valor):
        self.distancia_max_pc = float(valor)
        self.actualizar_radar()

    def actualizar_radar(self):
        self.canvas_radar.delete("all")
        self.planetas_dibujados.clear()

        self.canvas_radar.update_idletasks()
        ancho = self.canvas_radar.winfo_width()
        alto = self.canvas_radar.winfo_height()

        cx = ancho // 2
        cy = alto // 2
        radio_max_pixeles = min(ancho, alto) // 2 - 20

        # Anillos del radar
        for r in [radio_max_pixeles * 0.33, radio_max_pixeles * 0.66, radio_max_pixeles]:
            self.canvas_radar.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline="#eeff00",
                width=1
            )
        
        # Dibujamos el Sol / la Tierra en el centro (0,0)
        self.canvas_radar.create_oval(
            cx - 4, cy - 4, cx + 4, cy + 4,
            fill="#ffffff",  # Blanco brillante
            outline="#ffdd00", # Borde dorado/amarillo
            width=1
)

        zoom_z = calcular_escala_zoom(radio_max_pixeles, self.distancia_max_pc)

        total_planetas = len(self.planetas_habitables)
        for i, planeta in enumerate(self.planetas_habitables):
            angulo = i * (360.0 / total_planetas)
            distancia = planeta["dist"]

            px, py = coordenadas_polares_a_pixeles(
                distancia_pc=distancia,
                angulo_grados=angulo,
                zoom_Z=zoom_z,
                centro_x=cx,
                centro_y=cy
            )

            if 0 <= px <= ancho and 0 <= py <= alto:
                # AQUÍ DENTRO extraemos el color de ESTE planeta en particular
                color_planeta = planeta.get("color", "#00ffff")

                self.canvas_radar.create_oval(
                    px - 4, py - 4, px + 4, py + 4,
                    fill=color_planeta,
                    outline=""
                )
                
                self.planetas_dibujados.append({
                    "planeta": planeta,
                    "px": px,
                    "py": py
                })

    def _al_hacer_clic(self, event):
        mouse_x = event.x
        mouse_y = event.y

        for elemento in self.planetas_dibujados:
            px = elemento["px"]
            py = elemento["py"]
            
            distancia = math.sqrt((mouse_x - px)**2 + (mouse_y - py)**2)

            if distancia <= 8.0:
                self._mostrar_telemetria(elemento["planeta"])
                break

    def _mostrar_telemetria(self, planeta):
        nombre = planeta.get("name", "Desconocido")
        dist = planeta.get("dist", 0.0)
        temp_k = planeta.get("temp", 0.0)
        temp_c = temp_k - 273.15
        densidad = planeta.get("dens", 0.0)
        cluster = planeta.get("cluster", "Rocoso")

        self.label_nombre_planeta.configure(text=f"🪐 {nombre}")
        
        texto_info = (
            f"• Categoría: {cluster}\n"
            f"• Distancia: {dist:.2f} pc ({dist * 3.26:.1f} al)\n"
            f"• Temp. Superficie: {temp_k:.1f} K ({temp_c:.1f} °C)\n"
            f"• Densidad: {densidad:.2f} g/cm³\n"
            f"• Estado: Potencialmente Habitable"
        )
        self.label_detalles_planeta.configure(text=texto_info)