"""
Interfaz gráfica en Python (Tkinter) para el proyecto "Código Defensa
Torre", puerto de app/TowerDefenseGUI.java.

Cada clase de modelo/negocio vive en su propio archivo (igual que en
el proyecto Java), importada desde los paquetes modelo/ y negocio/.

Ejecutar con:  python3 tower_defense_gui.py
"""

import tkinter as tk
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tkinter import ttk, messagebox
from tkinter import ttk, messagebox

from modelo.torre import Torre
from modelo.enemigo import Enemigo
from modelo.oleada import Oleada
from negocio.lista_secuencial_torres import ListaSecuencialTorres
from negocio.lista_doble_enemigos import ListaDobleEnemigos
from negocio.lista_circular_oleadas import ListaCircularOleadas

# ------------------------------------------------------------------
# Paleta y fuentes
# ------------------------------------------------------------------
BG_OSCURO = "#171B24"
PANEL_OSCURO = "#1E232E"
ACCENT_TEAL = "#2DBEB2"
ACCENT_TEAL_OSCURO = "#1F8A81"
ACCENT_NARANJA = "#F0963C"
ACCENT_ROJO = "#DC4646"
ACCENT_AZUL = "#5A82DC"
TEXT_CLARO = "#E4E8F0"
TEXT_TENUE = "#969EAF"
GRIS_BOTON = "#5A606E"
GRIS_BOTON_OSCURO = "#3C404A"
CANVAS_BG = "#10141C"

FUENTE_TITULO = ("Segoe UI", 12, "bold")
FUENTE_ESTADO = ("Segoe UI", 11, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_PEQUENA = ("Segoe UI", 9)
FUENTE_MINI = ("Segoe UI", 8, "bold")
FUENTE_MONO = ("Consolas", 10)

VIDAS_INICIALES = 3
FIN_CAMINO = 20

# Escalado de dificultad por cada oleada iniciada (ver _accion_iniciar_oleada)
VIDA_EXTRA_POR_RONDA = 10
VELOCIDAD_EXTRA_CADA_N_RONDAS = 2

PALETA_TORRE = [ACCENT_TEAL, ACCENT_NARANJA, "#818CF8", "#34D399", "#F472B6"]
PALETA_ENEMIGO = [ACCENT_ROJO, "#FBBF24", "#A78BFA", "#F87171", "#60A5FA"]


def color_por_tipo(tipo, paleta):
    return paleta[abs(hash(tipo)) % len(paleta)]


class CampoDeBatallaCanvas(tk.Canvas):
    """Equivalente a PathPanel: dibuja la ruta, torres y enemigos (en
    línea recta sobre el camino) y muestra un tooltip al pasar el
    mouse sobre cada elemento."""

    def __init__(self, master, gui, **kwargs):
        super().__init__(master, bg=CANVAS_BG, highlightthickness=0, **kwargs)
        self.gui = gui
        self.posiciones_animadas = None
        self.hitboxes = []
        self.tooltip = None
        self.bind("<Configure>", lambda e: self.dibujar())
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", lambda e: self._ocultar_tooltip())

    def set_posiciones_animadas(self, mapa):
        self.posiciones_animadas = mapa
        self.dibujar()

    def limpiar_animacion(self):
        self.posiciones_animadas = None
        self.dibujar()

    def _map_pos(self, pos, left, right):
        clamped = max(0, min(FIN_CAMINO, pos))
        return left + (clamped / FIN_CAMINO) * (right - left)

    def dibujar(self):
        self.delete("all")
        self.hitboxes = []
        w = self.winfo_width() or 900
        h = self.winfo_height() or 320
        left, right = 80, w - 80
        track_y = h // 2

        self.create_rectangle(0, 0, w, h, fill=CANVAS_BG, outline="")

        self.create_line(left, track_y, right, track_y, fill="#483A2E", width=25,
                          capstyle=tk.ROUND)
        self.create_line(left, track_y, right, track_y, fill="#D6B28C", width=2,
                          dash=(2, 10))

        for p in range(0, FIN_CAMINO + 1, 5):
            x = self._map_pos(p, left, right)
            self.create_line(x, track_y - 6, x, track_y + 6, fill="#FFFFFF")
            self.create_text(x, track_y + 20, text=str(p), fill=TEXT_TENUE,
                              font=FUENTE_PEQUENA)

        self._dibujar_base(right, track_y)
        self._dibujar_inicio(left, track_y)
        self._dibujar_torres(left, right, track_y)
        self._dibujar_enemigos(left, right, track_y)

        if self.gui.juego_terminado:
            self.create_rectangle(0, 0, w, h, fill="#000000", stipple="gray50")
            self.create_text(w / 2, h / 2, text="GAME OVER", fill="white",
                              font=("Segoe UI", 26, "bold"))

    def _dibujar_base(self, x, track_y):
        vidas = self.gui.vidas_jugador
        color_base = "#4ADE80" if vidas >= 2 else ("#FACC15" if vidas == 1 else "#F87171")
        self.create_rectangle(x - 18, track_y - 55, x + 22, track_y, fill=color_base,
                               outline="")
        self.create_text(x, track_y + 14, text="BASE", fill=TEXT_CLARO, font=FUENTE_MINI)
        self.hitboxes.append((x - 22, track_y - 70, x + 22, track_y + 2,
                               f"Base del jugador\nVidas restantes: {vidas} / {VIDAS_INICIALES}"))

    def _dibujar_inicio(self, x, track_y):
        self.create_line(x - 2, track_y - 35, x - 2, track_y, fill=TEXT_TENUE, width=3)
        self.create_polygon(x + 1, track_y - 35, x + 22, track_y - 27, x + 1, track_y - 19,
                             fill=ACCENT_TEAL)

    def _dibujar_torres(self, left, right, track_y):
        torres_y = track_y - 80
        lista = self.gui.lista_torres
        for i in range(lista.contar_activas()):
            t = lista.get_torre(i)
            if t is None:
                continue
            x = self._map_pos(t.posicion, left, right)
            c = color_por_tipo(t.tipo, PALETA_TORRE)

            radio_px = (t.rango / FIN_CAMINO) * (right - left)
            self.create_rectangle(x - radio_px, track_y - 8, x + radio_px, track_y + 8,
                                   fill=c, outline="", stipple="gray25")

            yy = torres_y - (i % 2) * 16
            self.create_line(x, yy + 40, x, track_y, fill="#FFFFFF", width=1)
            self.create_rectangle(x - 15, yy + 12, x + 15, yy + 42, fill=c, outline="")
            self.create_oval(x - 15, yy - 4, x + 15, yy + 26, fill=c, outline="")
            self.create_text(x, yy + 11, text=str(t.id), fill="white", font=FUENTE_MINI)
            self.create_text(x, yy + 58, text=t.nombre, fill=TEXT_CLARO, font=FUENTE_PEQUENA)

            self.hitboxes.append((x - 15, yy - 4, x + 15, yy + 56,
                                   f"{t.nombre} (ID {t.id})\nTipo: {t.tipo}  Daño: {t.danio}\n"
                                   f"Rango: {t.rango}  Posición: {t.posicion}  Costo: {t.costo}"))

    def _dibujar_enemigos(self, left, right, track_y):
        # Todos los enemigos se dibujan sobre la MISMA línea (el camino),
        # avanzando de forma lineal según su posición — ya no se apilan
        # en filas distintas.
        enemigos_y = track_y 
        n = self.gui.lista_enemigos.get_primero()
        while n is not None:
            e = n.enemigo
            if self.posiciones_animadas is not None and e.id in self.posiciones_animadas:
                pos_mostrar = self.posiciones_animadas[e.id]
            else:
                pos_mostrar = e.posicion
            x = self._map_pos(pos_mostrar, left, right)
            yy = enemigos_y
            c = color_por_tipo(e.tipo, PALETA_ENEMIGO)

            max_vida = self.gui.vida_maxima_enemigo.get(e.id, max(e.vida, 1))
            frac = max(0, min(1, e.vida / max_vida))
            bar_w = 28
            self.create_rectangle(x - bar_w / 2, yy - 19, x + bar_w / 2, yy - 14,
                                   fill="#000000", outline="")
            color_barra = "#4ADE80" if frac > 0.5 else ("#FACC15" if frac > 0.2 else "#F87171")
            self.create_rectangle(x - bar_w / 2, yy - 19, x - bar_w / 2 + bar_w * frac, yy - 14,
                                   fill=color_barra, outline="")

            self.create_oval(x - 13, yy - 13, x + 13, yy + 13, fill=c, outline="")
            self.create_text(x, yy, text=str(e.id), fill="white", font=FUENTE_MINI)

            self.hitboxes.append((x - 14, yy - 20, x + 14, yy + 20,
                                   f"Enemigo #{e.id} ({e.tipo})\nVida: {e.vida}/{max_vida}  "
                                   f"Velocidad: {e.velocidad}\nPosición: {pos_mostrar:.1f}"))
            n = n.siguiente

    def _on_motion(self, event):
        for (x0, y0, x1, y1, texto) in self.hitboxes:
            if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                self._mostrar_tooltip(event, texto)
                return
        self._ocultar_tooltip()

    def _mostrar_tooltip(self, event, texto):
        if self.tooltip is None:
            self.tooltip = tk.Toplevel(self)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.attributes("-topmost", True)
            self._tooltip_label = tk.Label(
                self.tooltip, text=texto, justify="left", bg="#FFFFE0",
                fg="black", relief="solid", borderwidth=1, font=FUENTE_PEQUENA,
            )
            self._tooltip_label.pack(ipadx=4, ipady=2)
        else:
            self._tooltip_label.config(text=texto)
        x = self.winfo_rootx() + event.x + 16
        y = self.winfo_rooty() + event.y + 12
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.deiconify()

    def _ocultar_tooltip(self):
        if self.tooltip is not None:
            self.tooltip.withdraw()


class TowerDefenseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Código Defensa Torre — Tower Defense (Estructuras de Datos)")
        self.configure(bg=BG_OSCURO)
        self.minsize(1080, 680)
        self.geometry("1200x760")

        self.lista_torres = ListaSecuencialTorres()
        self.lista_enemigos = ListaDobleEnemigos()
        self.lista_oleadas = ListaCircularOleadas()

        self.vidas_jugador = VIDAS_INICIALES
        self.contador_id_enemigos = 1
        self.juego_terminado = False
        self.vida_maxima_enemigo = {}
        self.oleadas_iniciadas = 0  # ronda global -> escala la dificultad
        self.historial = []

        self._inicializar_caso_prueba()
        self._construir_interfaz()
        self._registrar_log("Caso de prueba inicial cargado correctamente.")
        self._refrescar_todo()

    def _inicializar_caso_prueba(self):
        self.lista_torres.insertar(Torre(1, "Arquero", "Fisico", 3, 20, 2, 50))
        self.lista_torres.insertar(Torre(2, "Cañón", "Explosivo", 8, 35, 3, 100))
        self.lista_oleadas.registrar(Oleada(1, 3, "Básico", 50, 1))
        self.lista_oleadas.registrar(Oleada(2, 2, "Rápido", 40, 2))

    # ==============================================================
    # Construcción de la interfaz (layout según boceto)
    # ==============================================================
    def _construir_interfaz(self):
        self._aplicar_estilos_ttk()

        cuerpo = tk.Frame(self, bg=BG_OSCURO)
        cuerpo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        cuerpo.grid_columnconfigure(0, weight=1)  # campo de batalla: se come todo el sobrante
        cuerpo.grid_columnconfigure(1, weight=0)  # panel de estadísticas: ancho FIJO (no crece)
        cuerpo.grid_rowconfigure(0, weight=0)
        cuerpo.grid_rowconfigure(1, weight=1)
        cuerpo.grid_rowconfigure(2, weight=0)

        # ---- columna izquierda ----
        self._construir_fila_labels(cuerpo).grid(row=0, column=0, sticky="ew", pady=(0, 6))

        campo_frame = tk.LabelFrame(cuerpo, text="Campo de batalla", bg=BG_OSCURO,
                                     fg=TEXT_CLARO, font=FUENTE_TITULO, labelanchor="nw",
                                     bd=1, relief=tk.GROOVE)
        self.canvas_campo = CampoDeBatallaCanvas(campo_frame, self)
        self.canvas_campo.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        campo_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))

        self._construir_fila_botones_inferior(cuerpo).grid(row=2, column=0, sticky="ew",
                                                             padx=(0, 10), pady=(8, 0))

        # ---- columna derecha ----
        # Frame con ancho FIJO en píxeles: grid_propagate(False) evita que
        # el Treeview de adentro "empuje" el panel para hacerse más ancho.
        # <<< AJUSTA EL ANCHO DEL PANEL DE ESTADÍSTICAS AQUÍ (en píxeles) >>>
        ANCHO_PANEL_ESTADISTICAS = 320
        panel_derecho = tk.Frame(cuerpo, width=ANCHO_PANEL_ESTADISTICAS, bg=BG_OSCURO)
        panel_derecho.grid(row=0, column=1, rowspan=2, sticky="nsew")
        # OJO: adentro metemos el contenido con .pack(), así que el que
        # manda aquí es pack_propagate, no grid_propagate.
        panel_derecho.pack_propagate(False)
        panel_derecho.grid_propagate(False)

        self.notebook_stats = self._construir_notebook_estadisticas(panel_derecho)
        self.notebook_stats.pack(fill=tk.BOTH, expand=True)

        self._construir_columna_partida(cuerpo).grid(row=2, column=1, sticky="new", pady=(8, 0))

    def _aplicar_estilos_ttk(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("Treeview", background="white", fieldbackground="white",
                          foreground="black", rowheight=24, font=FUENTE_NORMAL)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        estilo.configure("TNotebook", background=BG_OSCURO, borderwidth=0)
        estilo.configure("TNotebook.Tab", font=FUENTE_NORMAL, padding=(10, 4))

    # ---- fila superior: Vida / Cantidad de torres / Oleada ----
    def _construir_fila_labels(self, master):
        fila = tk.Frame(master, bg=BG_OSCURO)
        self.lbl_vidas = tk.Label(fila, bg=BG_OSCURO, fg=ACCENT_ROJO, font=FUENTE_ESTADO)
        self.lbl_torres_activas = tk.Label(fila, bg=BG_OSCURO, fg=ACCENT_TEAL, font=FUENTE_ESTADO)
        self.lbl_oleada_actual = tk.Label(fila, bg=BG_OSCURO, fg=ACCENT_NARANJA, font=FUENTE_ESTADO)
        self.lbl_vidas.pack(side=tk.LEFT, padx=(4, 0))
        self.lbl_torres_activas.pack(side=tk.LEFT, expand=True)
        self.lbl_oleada_actual.pack(side=tk.RIGHT, padx=(0, 4))
        return fila

    # ---- panel de estadísticas (tabs Torre / Enemigo / Oleada) ----
    def _construir_notebook_estadisticas(self, master):
        notebook = ttk.Notebook(master)
        pagina_torres, self.torres_tree = self._construir_tabla(
            notebook, ("ID", "Nombre", "Tipo", "Posición", "Daño", "Rango", "Costo"))
        pagina_enemigos, self.enemigos_tree = self._construir_tabla(
            notebook, ("ID", "Tipo", "Vida", "Velocidad", "Posición", "Recompensa"))
        pagina_oleadas = self._construir_tab_oleadas(notebook)
        notebook.add(pagina_torres, text="Torre")
        notebook.add(pagina_enemigos, text="Enemigo")
        notebook.add(pagina_oleadas, text="Oleada")
        return notebook

    def _construir_tabla(self, master, cols):
        pagina = tk.Frame(master, bg=BG_OSCURO)
        tree = ttk.Treeview(pagina, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            # stretch=False: sin esto, la columna se estira sola para
            # llenar el espacio sobrante del panel sin importar el width.
            tree.column(c, width=70, minwidth=40, anchor=tk.CENTER, stretch=False)

        scroll_y = ttk.Scrollbar(pagina, orient=tk.VERTICAL, command=tree.yview)
        scroll_x = ttk.Scrollbar(pagina, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        pagina.grid_rowconfigure(0, weight=1)
        pagina.grid_columnconfigure(0, weight=1)
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        return pagina, tree

    def _construir_tab_oleadas(self, master):
        panel = tk.Frame(master, bg="white")
        self.oleadas_text = tk.Text(panel, font=FUENTE_MONO, bg="white", fg="black",
                                     state=tk.DISABLED, wrap=tk.WORD)
        self.oleadas_text.pack(fill=tk.BOTH, expand=True)
        self.lbl_dificultad = tk.Label(
            panel, bg="white", fg="gray", font=FUENTE_PEQUENA, anchor="w",
            justify="left", wraplength=260)
        self.lbl_dificultad.pack(fill=tk.X, padx=4, pady=4)
        return panel

    # ---- fila inferior izquierda: botones de torres/oleadas + avanzar turno ----
    def _construir_fila_botones_inferior(self, master):
        fila = tk.Frame(master, bg=BG_OSCURO)

        caja_izq = tk.LabelFrame(fila, bg=PANEL_OSCURO, bd=1, relief=tk.GROOVE)
        caja_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        caja_izq.grid_columnconfigure(0, weight=1)
        caja_izq.grid_columnconfigure(1, weight=1)

        self.btn_registrar_torre = self._boton_grid(
            caja_izq, "+  Registrar torre", ACCENT_TEAL,
            self._abrir_dialogo_registrar_torre, 0, 0)
        self.btn_eliminar_torre = self._boton_grid(
            caja_izq, "x  Eliminar torre", ACCENT_ROJO,
            self._abrir_dialogo_eliminar_torre, 0, 1)
        self.btn_registrar_oleada = self._boton_grid(
            caja_izq, "+  Registrar oleada", ACCENT_AZUL,
            self._abrir_dialogo_registrar_oleada, 1, 0)
        self.btn_iniciar_oleada = self._boton_grid(
            caja_izq, "▶  Iniciar siguiente oleada", ACCENT_NARANJA,
            self._accion_iniciar_oleada, 1, 1)

        caja_avanzar = tk.LabelFrame(fila, bg=PANEL_OSCURO, bd=1, relief=tk.GROOVE)
        caja_avanzar.pack(side=tk.LEFT, fill=tk.BOTH)
        self.btn_avanzar_turno = tk.Button(
            caja_avanzar, text="▶▶\nAvanzar\nturno", bg=ACCENT_TEAL_OSCURO, fg="white",
            font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground=ACCENT_TEAL_OSCURO,
            activeforeground="white", cursor="hand2", command=self._accion_avanzar_turno,
            width=12, justify=tk.CENTER)
        self.btn_avanzar_turno.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        return fila

    def _boton_grid(self, master, texto, color, comando, fila, col):
        btn = tk.Button(master, text=texto, bg=color, fg="white", font=("Segoe UI", 9, "bold"),
                         relief=tk.FLAT, activebackground=color, activeforeground="white",
                         cursor="hand2", command=comando, padx=6, pady=10,
                         wraplength=140, justify=tk.CENTER)
        btn.grid(row=fila, column=col, sticky="nsew", padx=6, pady=6)
        return btn

    # ---- columna derecha inferior: Estado general / Reiniciar / Salir ----
    def _construir_columna_partida(self, master):
        col = tk.Frame(master, bg=BG_OSCURO)
        self._boton_ancho_completo(col, "Estado General", GRIS_BOTON, self._mostrar_estado_general)
        self._boton_ancho_completo(col, "Reiniciar Partida", GRIS_BOTON, self._reiniciar_juego)
        self._boton_ancho_completo(col, "Salir", GRIS_BOTON_OSCURO, self._salir)
        return col

    def _boton_ancho_completo(self, master, texto, color, comando):
        caja = tk.LabelFrame(master, bg=PANEL_OSCURO, bd=1, relief=tk.GROOVE)
        caja.pack(fill=tk.X, pady=4)
        btn = tk.Button(caja, text=texto, bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                         relief=tk.FLAT, activebackground=color, activeforeground="white",
                         cursor="hand2", command=comando, pady=10)
        btn.pack(fill=tk.X, padx=8, pady=8)
        return btn

    # ==================================================================
    # Diálogos
    # ==================================================================
    def _siguiente_id_torre_sugerido(self):
        id_ = 1
        while self.lista_torres.existe_id(id_):
            id_ += 1
        return id_

    def _siguiente_id_oleada_sugerido(self):
        id_ = 1
        while self.lista_oleadas.existe_id(id_):
            id_ += 1
        return id_

    def _abrir_dialogo_registrar_torre(self):
        dialog = tk.Toplevel(self)
        dialog.title("Registrar torre defensiva")
        dialog.configure(bg=PANEL_OSCURO)
        dialog.transient(self)
        dialog.grab_set()

        var_id = tk.IntVar(value=self._siguiente_id_torre_sugerido())
        var_nombre = tk.StringVar()
        var_tipo = tk.StringVar(value="Fisico")
        var_pos = tk.IntVar(value=0)
        var_danio = tk.IntVar(value=10)
        var_rango = tk.IntVar(value=2)
        var_costo = tk.IntVar(value=50)

        campos = [
            ("ID de torre:", tk.Spinbox(dialog, from_=1, to=9999, textvariable=var_id, width=18)),
            ("Nombre:", tk.Entry(dialog, textvariable=var_nombre, width=20)),
            ("Tipo:", ttk.Combobox(dialog, textvariable=var_tipo, width=18,
                                    values=["Fisico", "Explosivo", "Mágico", "Hielo", "Veneno"])),
            (f"Posición en la ruta (0-{FIN_CAMINO}):",
             tk.Spinbox(dialog, from_=0, to=FIN_CAMINO, textvariable=var_pos, width=18)),
            ("Daño:", tk.Spinbox(dialog, from_=1, to=999, textvariable=var_danio, width=18)),
            ("Rango de alcance:", tk.Spinbox(dialog, from_=1, to=50, textvariable=var_rango, width=18)),
            ("Costo:", tk.Spinbox(dialog, from_=0, to=9999, increment=5, textvariable=var_costo, width=18)),
        ]
        self._layout_campos(dialog, campos)

        lbl_error = tk.Label(dialog, text=" ", bg=PANEL_OSCURO, fg=ACCENT_ROJO, font=FUENTE_PEQUENA)
        lbl_error.grid(row=len(campos), column=0, columnspan=2, pady=(4, 0))

        def guardar():
            id_ = var_id.get()
            if self.lista_torres.existe_id(id_):
                lbl_error.config(text="Ya existe una torre con ese ID.")
                return
            nombre = var_nombre.get().strip()
            if not nombre:
                lbl_error.config(text="El nombre no puede estar vacío.")
                return
            tipo = var_tipo.get().strip() or "Fisico"
            nueva = Torre(id_, nombre, tipo, var_pos.get(), var_danio.get(),
                          var_rango.get(), var_costo.get())
            if self.lista_torres.insertar(nueva):
                self._registrar_log(f"Torre registrada: {nueva}")
                self._refrescar_todo()
                dialog.destroy()
            else:
                lbl_error.config(text="Capacidad máxima de torres alcanzada.")

        btn = tk.Button(dialog, text="Registrar torre", bg=ACCENT_TEAL, fg="white",
                         relief=tk.FLAT, command=guardar, padx=8, pady=6)
        btn.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(6, 12))
        dialog.bind("<Return>", lambda e: guardar())

    def _abrir_dialogo_registrar_oleada(self):
        dialog = tk.Toplevel(self)
        dialog.title("Registrar oleada")
        dialog.configure(bg=PANEL_OSCURO)
        dialog.transient(self)
        dialog.grab_set()

        var_id = tk.IntVar(value=self._siguiente_id_oleada_sugerido())
        var_cantidad = tk.IntVar(value=3)
        var_tipo = tk.StringVar(value="Básico")
        var_vida = tk.IntVar(value=50)
        var_velocidad = tk.IntVar(value=1)

        campos = [
            ("ID de oleada:", tk.Spinbox(dialog, from_=1, to=9999, textvariable=var_id, width=18)),
            ("Cantidad de enemigos:", tk.Spinbox(dialog, from_=1, to=50, textvariable=var_cantidad, width=18)),
            ("Tipo de enemigo:", ttk.Combobox(dialog, textvariable=var_tipo, width=18,
                                               values=["Básico", "Rápido", "Tanque", "Volador", "Élite"])),
            ("Vida base:", tk.Spinbox(dialog, from_=1, to=9999, increment=5, textvariable=var_vida, width=18)),
            ("Velocidad base:", tk.Spinbox(dialog, from_=1, to=10, textvariable=var_velocidad, width=18)),
        ]
        self._layout_campos(dialog, campos)

        lbl_error = tk.Label(dialog, text=" ", bg=PANEL_OSCURO, fg=ACCENT_ROJO, font=FUENTE_PEQUENA)
        lbl_error.grid(row=len(campos), column=0, columnspan=2, pady=(4, 0))

        def guardar():
            id_ = var_id.get()
            if self.lista_oleadas.existe_id(id_):
                lbl_error.config(text="Ya existe una oleada con ese ID.")
                return
            tipo = var_tipo.get().strip() or "Básico"
            oleada = Oleada(id_, var_cantidad.get(), tipo, var_vida.get(), var_velocidad.get())
            self.lista_oleadas.registrar(oleada)
            self._registrar_log(f"Oleada registrada: {oleada}")
            self._refrescar_todo()
            dialog.destroy()

        btn = tk.Button(dialog, text="Registrar oleada", bg=ACCENT_AZUL, fg="white",
                         relief=tk.FLAT, command=guardar, padx=8, pady=6)
        btn.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(6, 12))
        dialog.bind("<Return>", lambda e: guardar())

    def _layout_campos(self, dialog, campos):
        for i, (etiqueta, widget) in enumerate(campos):
            tk.Label(dialog, text=etiqueta, bg=PANEL_OSCURO, fg=TEXT_CLARO,
                     font=FUENTE_NORMAL).grid(row=i, column=0, sticky="w", padx=10, pady=6)
            widget.grid(row=i, column=1, sticky="w", padx=10, pady=6)

    def _abrir_dialogo_eliminar_torre(self):
        if self.lista_torres.contar_activas() == 0:
            messagebox.showinfo("Eliminar torre", "No hay torres registradas.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Eliminar torre")
        dialog.configure(bg=PANEL_OSCURO)
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(dialog, text="Selecciona la torre a eliminar:", bg=PANEL_OSCURO,
                 fg=TEXT_CLARO, font=FUENTE_NORMAL).pack(padx=12, pady=(12, 6))

        opciones = []
        for i in range(self.lista_torres.contar_activas()):
            t = self.lista_torres.get_torre(i)
            opciones.append(f"{t.id} — {t.nombre} ({t.tipo})")

        var_sel = tk.StringVar(value=opciones[0])
        combo = ttk.Combobox(dialog, textvariable=var_sel, values=opciones,
                              state="readonly", width=30)
        combo.pack(padx=12, pady=6)

        def confirmar():
            seleccion = var_sel.get()
            id_ = int(seleccion.split(" — ")[0].strip())
            if self.lista_torres.eliminar_por_id(id_):
                self._registrar_log(f"Torre eliminada (ID {id_}).")
                self._refrescar_todo()
            else:
                self._registrar_log(f"No se encontró la torre con ID {id_}.")
            dialog.destroy()

        tk.Button(dialog, text="Eliminar", bg=ACCENT_ROJO, fg="white", relief=tk.FLAT,
                  command=confirmar, padx=8, pady=6).pack(pady=(6, 12))

    # ==================================================================
    # Acciones de juego
    # ==================================================================
    def _accion_iniciar_oleada(self):
        if self.juego_terminado:
            return
        if self.lista_oleadas.get_tamanio() == 0:
            self._registrar_log("No hay oleadas registradas todavía.")
            return
        oleada = self.lista_oleadas.avanzar_siguiente_oleada()
        if oleada is None:
            self._registrar_log("No hay oleadas disponibles.")
            return

        # --- Dificultad progresiva ---
        # Cada vez que se inicia una oleada (aunque el ciclo circular
        # repita la misma Oleada registrada), la ronda global sube y
        # los enemigos nacen más fuertes y más rápidos que la vez
        # anterior.
        self.oleadas_iniciadas += 1
        ronda = self.oleadas_iniciadas
        vida_extra = (ronda - 1) * VIDA_EXTRA_POR_RONDA
        velocidad_extra = (ronda - 1) // VELOCIDAD_EXTRA_CADA_N_RONDAS
        vida_final = oleada.vida_base + vida_extra
        velocidad_final = oleada.velocidad_base + velocidad_extra

        self._registrar_log(
            f"¡Iniciando Oleada {oleada.id_oleada} ({oleada.tipo_enemigo}) — ronda global #{ronda}!")
        self._registrar_log(
            f"Dificultad escalada: vida {vida_final} (base {oleada.vida_base} +{vida_extra}), "
            f"velocidad {velocidad_final} (base {oleada.velocidad_base} +{velocidad_extra}).")

        for _ in range(oleada.cantidad_enemigos):
            e = Enemigo(self.contador_id_enemigos, oleada.tipo_enemigo, vida_final,
                        velocidad_final, 0, 10)
            self.vida_maxima_enemigo[self.contador_id_enemigos] = vida_final
            self.contador_id_enemigos += 1
            self.lista_enemigos.insertar_al_final(e)
        self._registrar_log(f"Se generaron {oleada.cantidad_enemigos} enemigos en la posición 0.")
        self._refrescar_todo()

    def _accion_avanzar_turno(self):
        if self.juego_terminado:
            return
        if self.lista_enemigos.get_tamanio() == 0:
            self._registrar_log("No hay enemigos activos en el campo. Inicia una oleada primero.")
            return

        self._set_botones_habilitados(False)
        self._registrar_log("--- EJECUTANDO TURNO ---")

        inicio = {}
        n = self.lista_enemigos.get_primero()
        while n is not None:
            inicio[n.enemigo.id] = float(n.enemigo.posicion)
            n = n.siguiente

        # Todos avanzan en línea recta sobre el camino, cada uno según
        # su propia velocidad (no se cruzan de carril, solo avanzan).
        n = self.lista_enemigos.get_primero()
        while n is not None:
            n.enemigo.posicion += n.enemigo.velocidad
            n = n.siguiente

        fin = {}
        n = self.lista_enemigos.get_primero()
        while n is not None:
            fin[n.enemigo.id] = float(n.enemigo.posicion)
            n = n.siguiente

        self._animar_movimiento(inicio, fin, self._continuar_turno_tras_animacion)

    def _animar_movimiento(self, inicio, fin, al_terminar):
        pasos = 22
        estado = {"paso": 0}

        def paso_animacion():
            estado["paso"] += 1
            t = min(1.0, estado["paso"] / pasos)
            intermedio = {}
            for id_, hasta in fin.items():
                desde = inicio.get(id_, hasta)
                intermedio[id_] = desde + (hasta - desde) * t
            self.canvas_campo.set_posiciones_animadas(intermedio)
            if t >= 1.0:
                self.canvas_campo.limpiar_animacion()
                al_terminar()
            else:
                self.after(16, paso_animacion)

        paso_animacion()

    def _continuar_turno_tras_animacion(self):
        for i in range(self.lista_torres.contar_activas()):
            t = self.lista_torres.get_torre(i)
            nodo_e = self.lista_enemigos.get_primero()
            while nodo_e is not None:
                e = nodo_e.enemigo
                distancia = abs(e.posicion - t.posicion)
                if distancia <= t.rango and e.vida > 0:
                    nueva_vida = e.vida - t.danio
                    e.vida = max(0, nueva_vida)
                    self._registrar_log(
                        f"{t.nombre} atacó al Enemigo #{e.id} (-{t.danio} HP). "
                        f"Vida restante: {e.vida}")
                nodo_e = nodo_e.siguiente

        actual_eval = self.lista_enemigos.get_primero()
        while actual_eval is not None:
            siguiente_eval = actual_eval.siguiente
            e = actual_eval.enemigo
            if e.vida <= 0:
                self._registrar_log(f"¡Enemigo #{e.id} ({e.tipo}) destruido!")
                self.lista_enemigos.eliminar_por_id(e.id)
                self.vida_maxima_enemigo.pop(e.id, None)
            elif e.posicion >= FIN_CAMINO:
                self._registrar_log(f"¡Enemigo #{e.id} llegó a la base! Pierdes 1 vida.")
                self.vidas_jugador -= 1
                self.lista_enemigos.eliminar_por_id(e.id)
                self.vida_maxima_enemigo.pop(e.id, None)
            actual_eval = siguiente_eval

        self._registrar_log(f"Turno finalizado. Vidas actuales del jugador: {self.vidas_jugador}")

        if self.vidas_jugador <= 0:
            self.juego_terminado = True

        self._refrescar_todo()
        self._set_botones_habilitados(not self.juego_terminado)

        if self.juego_terminado:
            messagebox.showwarning("Fin del juego", "¡Has perdido todas tus vidas!\nGAME OVER.")

    def _mostrar_estado_general(self):
        msg = (
            "====== ESTADO GENERAL DEL JUEGO ======\n"
            f"Vidas del Jugador: {self.vidas_jugador}\n"
            f"Torres Activas: {self.lista_torres.contar_activas()}\n"
            f"Enemigos Activos en Campo: {self.lista_enemigos.get_tamanio()}\n"
            f"Oleadas Registradas: {self.lista_oleadas.get_tamanio()}\n"
            f"Ronda global de dificultad: {self.oleadas_iniciadas}\n"
            "----------------------------------------\n"
            "Últimos eventos:\n" + "\n".join(self.historial[-8:])
        )
        messagebox.showinfo("Estado general del juego", msg)

    def _reiniciar_juego(self):
        if not messagebox.askyesno("Reiniciar partida", "¿Reiniciar la partida desde cero?"):
            return
        self.lista_torres = ListaSecuencialTorres()
        self.lista_enemigos = ListaDobleEnemigos()
        self.lista_oleadas = ListaCircularOleadas()
        self.vidas_jugador = VIDAS_INICIALES
        self.contador_id_enemigos = 1
        self.juego_terminado = False
        self.vida_maxima_enemigo.clear()
        self.oleadas_iniciadas = 0
        self.historial.clear()
        self._inicializar_caso_prueba()

        self._registrar_log("Partida reiniciada.")
        self._set_botones_habilitados(True)
        self._refrescar_todo()

    def _salir(self):
        if messagebox.askyesno("Salir", "¿Seguro que quieres salir?\n¡Gracias por jugar!"):
            self.destroy()

    # ==================================================================
    # Refresco de la interfaz
    # ==================================================================
    def _refrescar_todo(self):
        self.lbl_vidas.config(text=f"Vida: {self._corazones()}")
        self.lbl_torres_activas.config(
            text=f"Cantidad de torres: {self.lista_torres.contar_activas()}")
        self.lbl_oleada_actual.config(text=f"Oleada: {self.oleadas_iniciadas}")

        self.torres_tree.delete(*self.torres_tree.get_children())
        for i in range(self.lista_torres.contar_activas()):
            t = self.lista_torres.get_torre(i)
            self.torres_tree.insert("", tk.END, values=(t.id, t.nombre, t.tipo, t.posicion,
                                                          t.danio, t.rango, t.costo))

        self.enemigos_tree.delete(*self.enemigos_tree.get_children())
        n = self.lista_enemigos.get_primero()
        while n is not None:
            e = n.enemigo
            self.enemigos_tree.insert("", tk.END, values=(e.id, e.tipo, e.vida, e.velocidad,
                                                            e.posicion, e.recompensa))
            n = n.siguiente

        self.oleadas_text.config(state=tk.NORMAL)
        self.oleadas_text.delete("1.0", tk.END)
        self.oleadas_text.insert(tk.END, "\n".join(self.lista_oleadas.mostrar()))
        self.oleadas_text.config(state=tk.DISABLED)
        self.lbl_dificultad.config(
            text=f"Ronda global: {self.oleadas_iniciadas}  |  +{VIDA_EXTRA_POR_RONDA} vida "
                 f"por ronda, +1 velocidad cada {VELOCIDAD_EXTRA_CADA_N_RONDAS} rondas.")

        self.notebook_stats.tab(0, text=f"Torre ({self.lista_torres.contar_activas()})")
        self.notebook_stats.tab(1, text=f"Enemigo ({self.lista_enemigos.get_tamanio()})")
        self.notebook_stats.tab(2, text=f"Oleada ({self.lista_oleadas.get_tamanio()})")

        self.canvas_campo.dibujar()

    def _corazones(self):
        return " ".join("♥" if i < self.vidas_jugador else "♡" for i in range(VIDAS_INICIALES))

    def _registrar_log(self, mensaje):
        self.historial.append(mensaje)

    def _set_botones_habilitados(self, habilitado):
        estado = tk.NORMAL if habilitado else tk.DISABLED
        for btn in (self.btn_registrar_torre, self.btn_eliminar_torre,
                    self.btn_registrar_oleada, self.btn_iniciar_oleada,
                    self.btn_avanzar_turno):
            btn.config(state=estado)


def main():
    app = TowerDefenseGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
