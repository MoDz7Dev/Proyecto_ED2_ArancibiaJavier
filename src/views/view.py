import tkinter as tk
from tkinter import ttk, messagebox


class View(tk.Frame):
    # ── Paleta de colores ──────────────────────────────────────────────
    COLOR_BG       = "#ffffff"
    COLOR_PANEL    = "#f5f5f5"
    COLOR_VERDE    = "#83e60a"
    COLOR_OSCURO   = "#24272c"
    COLOR_TEXTO    = "#000000"
    COLOR_BLANCO   = "#ffffff"
    COLOR_ROJO     = "#e53935"
    COLOR_AZUL     = "#1565C0"
    COLOR_MSG_OK   = "#83e60a"
    COLOR_MSG_ERR  = "#e53935"
    COLOR_MSG_INFO = "#1565C0"

    def __init__(self, parent):
        super().__init__(parent, bg=self.COLOR_BG)
        self.pack(fill=tk.BOTH, expand=True)
        self._controller = None
        self._build_ui()

    def set_controller(self, controller):
        self._controller = controller

    # ─────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA UI
    # ─────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        contenedor = tk.Frame(self, bg=self.COLOR_BG)
        contenedor.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)
        self._build_panel_acciones(contenedor)
        self._build_panel_tabla(contenedor)

    def _build_header(self):
        header = tk.Frame(self, bg=self.COLOR_OSCURO)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="INVENTARIO DE PRODUCTOS",
            bg=self.COLOR_OSCURO,
            fg=self.COLOR_BLANCO,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=12)

    def _build_panel_acciones(self, parent):
        panel = tk.Frame(parent, bg=self.COLOR_PANEL, width=300,
                         highlightbackground="#dddddd", highlightthickness=1)
        panel.grid(row=0, column=0, sticky="ns", padx=(0, 15))
        panel.pack_propagate(False)

        tk.Label(panel, text="GESTIÓN DE PRODUCTOS", bg=self.COLOR_PANEL,
                 fg=self.COLOR_TEXTO, font=("Segoe UI", 10, "bold")).pack(
                     anchor="w", padx=15, pady=(15, 10))

        # ── Formulario ──
        campos = [
            ("Código:",    "input_codigo"),
            ("Nombre:",    "input_nombre"),
            ("Precio:",    "input_precio"),
            ("Stock:",     "input_stock"),
            ("Categoría:", "input_categoria"),
        ]
        for label, attr in campos:
            tk.Label(panel, text=label, bg=self.COLOR_PANEL,
                     fg=self.COLOR_TEXTO, font=("Segoe UI", 9)).pack(
                         anchor="w", padx=15)
            entry = tk.Entry(panel, font=("Segoe UI", 10),
                             bg=self.COLOR_BG, fg=self.COLOR_TEXTO,
                             insertbackground=self.COLOR_TEXTO,
                             relief="solid", bd=1)
            entry.pack(fill=tk.X, padx=15, pady=(2, 6))
            setattr(self, attr, entry)

        ttk.Separator(panel, orient="horizontal").pack(fill=tk.X, padx=15, pady=8)

        # ── Botones ──
        self._boton(panel, "Insertar producto",   self.COLOR_VERDE,
                    lambda: self._controller.insertar())
        self._boton(panel, "Buscar producto",     self.COLOR_AZUL,
                    lambda: self._controller.buscar())
        self._boton(panel, "Eliminar producto",   self.COLOR_ROJO,
                    lambda: self._controller.eliminar())
        self._boton(panel, "Actualizar stock",    self.COLOR_OSCURO,
                    lambda: self._controller.actualizar_stock())

        ttk.Separator(panel, orient="horizontal").pack(fill=tk.X, padx=15, pady=8)

        # ── Búsqueda por categoría ──
        tk.Label(panel, text="Filtrar por categoría:", bg=self.COLOR_PANEL,
                 fg=self.COLOR_TEXTO, font=("Segoe UI", 9)).pack(anchor="w", padx=15)
        self.input_filtro = tk.Entry(panel, font=("Segoe UI", 10),
                                     bg=self.COLOR_BG, fg=self.COLOR_TEXTO,
                                     insertbackground=self.COLOR_TEXTO,
                                     relief="solid", bd=1)
        self.input_filtro.pack(fill=tk.X, padx=15, pady=(2, 6))
        self._boton(panel, "Filtrar",  "#37474F",
                    lambda: self._controller.filtrar_categoria())
        self._boton(panel, "Ver todos", "#546E7A",
                    lambda: self._controller.listar_todos())

        ttk.Separator(panel, orient="horizontal").pack(fill=tk.X, padx=15, pady=8)

        self._boton(panel, "Guardar estado", "#37474F",
                    lambda: self._controller.guardar_estado())

        # ── Mensaje feedback ──
        self.lbl_mensaje = tk.Label(panel, text="", bg=self.COLOR_PANEL,
                                    fg=self.COLOR_MSG_OK,
                                    font=("Segoe UI", 9), wraplength=260)
        self.lbl_mensaje.pack(padx=15, pady=(8, 15))

    def _build_panel_tabla(self, parent):
        panel = tk.Frame(parent, bg=self.COLOR_PANEL,
                         highlightbackground="#dddddd", highlightthickness=1)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        tk.Label(panel, text="LISTA DE PRODUCTOS (ordenado por nombre)",
                 bg=self.COLOR_PANEL, fg=self.COLOR_TEXTO,
                 font=("Segoe UI", 10, "bold")).grid(
                     row=0, column=0, sticky="w", padx=15, pady=(10, 4))

        # ── Treeview ──
        frame_tabla = tk.Frame(panel, bg=self.COLOR_PANEL)
        frame_tabla.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        columnas = ("codigo", "nombre", "precio", "stock", "categoria")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas,
                                  show="headings", selectmode="browse")

        # Encabezados
        encabezados = {
            "codigo"   : ("Código",    80),
            "nombre"   : ("Nombre",    200),
            "precio"   : ("Precio",    90),
            "stock"    : ("Stock",     80),
            "categoria": ("Categoría", 120),
        }
        for col, (texto, ancho) in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, anchor="center")

        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical",   command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Selección de fila → rellena el formulario
        self.tabla.bind("<<TreeviewSelect>>", self._on_seleccionar_fila)

    # ─────────────────────────────────────────
    #  EVENTOS
    # ─────────────────────────────────────────
    def _on_seleccionar_fila(self, event):
        """Al seleccionar una fila de la tabla, rellena el formulario."""
        seleccion = self.tabla.selection()
        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            self.limpiar_formulario()
            self.input_codigo.insert(0,    valores[0])
            self.input_nombre.insert(0,    valores[1])
            self.input_precio.insert(0,    valores[2])
            self.input_stock.insert(0,     valores[3])
            self.input_categoria.insert(0, valores[4])

    def _boton(self, parent, texto, color, comando):
        btn = tk.Button(
            parent, text=texto, bg=color,
            fg=self.COLOR_BLANCO,
            activebackground=color,
            activeforeground=self.COLOR_BLANCO,
            font=("Segoe UI", 9, "bold"),
            relief="flat", bd=0, cursor="hand2",
            padx=12, pady=7,
            command=comando
        )
        btn.pack(fill=tk.X, padx=15, pady=3)

    # ─────────────────────────────────────────
    #  MÉTODOS PÚBLICOS → llamados por el Controlador
    # ─────────────────────────────────────────
    def mostrar_mensaje(self, texto: str, color: str = None):
        """Muestra un mensaje de feedback en el panel de acciones."""
        self.lbl_mensaje.config(text=texto, fg=color or self.COLOR_MSG_OK)

    def actualizar_tabla(self, productos: list):
        """Refresca la tabla con la lista de productos recibida."""
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for p in productos:
            self.tabla.insert("", tk.END, values=(
                p["codigo"],
                p["nombre"],
                f"Bs. {p['precio']:.2f}",
                p["stock"],
                p["categoria"]
            ))

    def get_formulario(self) -> dict:
        """Retorna los valores actuales del formulario como diccionario."""
        return {
            "codigo"   : self.input_codigo.get().strip(),
            "nombre"   : self.input_nombre.get().strip(),
            "precio"   : self.input_precio.get().strip(),
            "stock"    : self.input_stock.get().strip(),
            "categoria": self.input_categoria.get().strip(),
        }

    def get_filtro(self) -> str:
        """Retorna el texto del campo de filtro por categoría."""
        return self.input_filtro.get().strip()

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        for attr in ("input_codigo", "input_nombre", "input_precio",
                     "input_stock", "input_categoria"):
            getattr(self, attr).delete(0, tk.END)

    def confirmar(self, mensaje: str) -> bool:
        """Muestra un diálogo de confirmación y retorna True/False."""
        return messagebox.askyesno("Confirmar", mensaje)