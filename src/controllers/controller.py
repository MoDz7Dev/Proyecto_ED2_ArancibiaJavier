from models.model import ABBInventario


class Controller:
    def __init__(self, model: ABBInventario, view, archivo_estado: str):
        """
        Controlador MVC — conecta el modelo con la vista.

        Args:
            model (ABBInventario): Instancia del árbol de inventario.
            view: Instancia de la vista tkinter.
            archivo_estado (str): Ruta del archivo JSON de persistencia.
        """
        self.model          = model
        self.view           = view
        self.archivo_estado = archivo_estado
        self.view.set_controller(self)
        self._refrescar()

    # ─────────────────────────────────────────
    #  INSERTAR
    # ─────────────────────────────────────────
    def insertar(self):
        """Valida el formulario e inserta un producto en el ABB."""
        datos = self.view.get_formulario()

        if not datos["codigo"] or not datos["nombre"]:
            self.view.mostrar_mensaje("⚠ Código y nombre son obligatorios.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        try:
            precio = float(datos["precio"])
            stock  = int(datos["stock"])
        except ValueError:
            self.view.mostrar_mensaje("⚠ Precio debe ser número decimal y stock entero.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        try:
            self.model.insertar(
                datos["codigo"],
                datos["nombre"],
                precio,
                stock,
                datos["categoria"]
            )
            self.view.limpiar_formulario()
            self.view.mostrar_mensaje(f"✓ '{datos['nombre']}' insertado correctamente.",
                                      color=self.view.COLOR_MSG_OK)
            self._refrescar()
        except ValueError as e:
            self.view.mostrar_mensaje(f"⚠ {e}", color=self.view.COLOR_MSG_ERR)

    # ─────────────────────────────────────────
    #  BUSCAR
    # ─────────────────────────────────────────
    def buscar(self):
        """Busca un producto por nombre y lo resalta en la tabla."""
        datos = self.view.get_formulario()
        nombre = datos["nombre"]

        if not nombre:
            self.view.mostrar_mensaje("⚠ Escribe un nombre para buscar.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        nodo = self.model.buscar(nombre)
        if nodo:
            self.view.actualizar_tabla([nodo.to_dict()])
            self.view.mostrar_mensaje(f"✓ Producto '{nodo.nombre}' encontrado.",
                                      color=self.view.COLOR_MSG_INFO)
        else:
            self.view.mostrar_mensaje(f"⚠ No se encontró '{nombre}'.",
                                      color=self.view.COLOR_MSG_ERR)

    # ─────────────────────────────────────────
    #  ELIMINAR
    # ─────────────────────────────────────────
    def eliminar(self):
        """Elimina un producto del ABB previa confirmación."""
        datos = self.view.get_formulario()
        nombre = datos["nombre"]

        if not nombre:
            self.view.mostrar_mensaje("⚠ Escribe el nombre del producto a eliminar.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        if not self.view.confirmar(f"¿Eliminar el producto '{nombre}'?"):
            return

        eliminado = self.model.eliminar(nombre)
        if eliminado:
            self.view.limpiar_formulario()
            self.view.mostrar_mensaje(f"✓ '{nombre}' eliminado correctamente.",
                                      color=self.view.COLOR_MSG_OK)
            self._refrescar()
        else:
            self.view.mostrar_mensaje(f"⚠ No se encontró '{nombre}'.",
                                      color=self.view.COLOR_MSG_ERR)

    # ─────────────────────────────────────────
    #  ACTUALIZAR STOCK
    # ─────────────────────────────────────────
    def actualizar_stock(self):
        """Actualiza el stock de un producto existente."""
        datos = self.view.get_formulario()
        nombre = datos["nombre"]

        if not nombre:
            self.view.mostrar_mensaje("⚠ Escribe el nombre del producto.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        try:
            nuevo_stock = int(datos["stock"])
        except ValueError:
            self.view.mostrar_mensaje("⚠ El stock debe ser un número entero.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        actualizado = self.model.actualizar_stock(nombre, nuevo_stock)
        if actualizado:
            self.view.mostrar_mensaje(f"✓ Stock de '{nombre}' actualizado a {nuevo_stock}.",
                                      color=self.view.COLOR_MSG_OK)
            self._refrescar()
        else:
            self.view.mostrar_mensaje(f"⚠ No se encontró '{nombre}'.",
                                      color=self.view.COLOR_MSG_ERR)

    # ─────────────────────────────────────────
    #  FILTRAR POR CATEGORÍA
    # ─────────────────────────────────────────
    def filtrar_categoria(self):
        """Filtra y muestra productos de una categoría específica."""
        categoria = self.view.get_filtro()

        if not categoria:
            self.view.mostrar_mensaje("⚠ Escribe una categoría para filtrar.",
                                      color=self.view.COLOR_MSG_ERR)
            return

        productos = self.model.buscar_por_categoria(categoria)
        self.view.actualizar_tabla(productos)

        if productos:
            self.view.mostrar_mensaje(f"✓ {len(productos)} producto(s) en '{categoria}'.",
                                      color=self.view.COLOR_MSG_INFO)
        else:
            self.view.mostrar_mensaje(f"⚠ Sin productos en '{categoria}'.",
                                      color=self.view.COLOR_MSG_ERR)

    # ─────────────────────────────────────────
    #  LISTAR TODOS
    # ─────────────────────────────────────────
    def listar_todos(self):
        """Muestra todos los productos ordenados por nombre (inorden)."""
        self._refrescar()
        self.view.mostrar_mensaje("✓ Mostrando todos los productos.",
                                  color=self.view.COLOR_MSG_INFO)

    # ─────────────────────────────────────────
    #  GUARDAR ESTADO
    # ─────────────────────────────────────────
    def guardar_estado(self):
        """Persiste el inventario en el archivo JSON."""
        self.model.guardar_estado(self.archivo_estado)
        self.view.mostrar_mensaje("✓ Inventario guardado correctamente.",
                                  color=self.view.COLOR_MSG_OK)

    # ─────────────────────────────────────────
    #  PRIVADO
    # ─────────────────────────────────────────
    def _refrescar(self):
        """Actualiza la tabla con todos los productos en orden inorden."""
        self.view.actualizar_tabla(self.model.listar())