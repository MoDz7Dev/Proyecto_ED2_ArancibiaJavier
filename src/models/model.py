import json


# ─────────────────────────────────────────────
#  NODO DEL ABB
# ─────────────────────────────────────────────
class Nodo:
    def __init__(self, codigo: str, nombre: str, precio: float, stock: int, categoria: str):
        """
        Nodo del Arbol Binario de Busqueda.

        Args:
            codigo (str): Código único del producto. Ej: 'P-001'.
            nombre (str): Nombre del producto (clave del ABB).
            precio (float): Precio del producto.
            stock (int): Cantidad en inventario.
            categoria (str): Categoría del producto.
        """
        self.codigo    = codigo
        self.nombre    = nombre
        self.precio    = precio
        self.stock     = stock
        self.categoria = categoria
        self.izq       = None  # hijo izquierdo (nombre menor)
        self.der       = None  # hijo derecho  (nombre mayor)

    def to_dict(self) -> dict:
        """Convierte el nodo a diccionario para serializar en JSON."""
        return {
            "codigo"   : self.codigo,
            "nombre"   : self.nombre,
            "precio"   : self.precio,
            "stock"    : self.stock,
            "categoria": self.categoria
        }


# ─────────────────────────────────────────────
#  ÁRBOL BINARIO DE BÚSQUEDA
# ─────────────────────────────────────────────
class ABBInventario:
    def __init__(self):
        """Inicializa el ABB vacío."""
        self.raiz = None

    # ─────────────────────────────────────────
    #  INSERTAR
    # ─────────────────────────────────────────
    def insertar(self, codigo: str, nombre: str, precio: float, stock: int, categoria: str) -> None:
        """
        Inserta un producto en el ABB ordenado por nombre.

        Args:
            codigo (str): Código único del producto.
            nombre (str): Nombre del producto (clave de ordenamiento).
            precio (float): Precio del producto.
            stock (int): Cantidad en inventario.
            categoria (str): Categoría del producto.

        Raises:
            ValueError: Si ya existe un producto con el mismo nombre.
        """
        nuevo = Nodo(codigo, nombre, precio, stock, categoria)
        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar_recursivo(self.raiz, nuevo)

    def _insertar_recursivo(self, actual: Nodo, nuevo: Nodo) -> None:
        """Recorre el árbol recursivamente para insertar en la posición correcta."""
        if nuevo.nombre.lower() < actual.nombre.lower():
            if actual.izq is None:
                actual.izq = nuevo
            else:
                self._insertar_recursivo(actual.izq, nuevo)
        elif nuevo.nombre.lower() > actual.nombre.lower():
            if actual.der is None:
                actual.der = nuevo
            else:
                self._insertar_recursivo(actual.der, nuevo)
        else:
            raise ValueError(f"Ya existe un producto con el nombre '{nuevo.nombre}'.")

    # ─────────────────────────────────────────
    #  BUSCAR
    # ─────────────────────────────────────────
    def buscar(self, nombre: str) -> Nodo | None:
        """
        Busca un producto por nombre en el ABB. O(log n).

        Args:
            nombre (str): Nombre del producto a buscar.

        Returns:
            Nodo: El nodo encontrado, o None si no existe.
        """
        return self._buscar_recursivo(self.raiz, nombre.lower())

    def _buscar_recursivo(self, actual: Nodo, nombre: str) -> Nodo | None:
        """Recorre el árbol recursivamente para encontrar el nodo."""
        if actual is None:
            return None
        if nombre == actual.nombre.lower():
            return actual
        if nombre < actual.nombre.lower():
            return self._buscar_recursivo(actual.izq, nombre)
        return self._buscar_recursivo(actual.der, nombre)

    # ─────────────────────────────────────────
    #  ELIMINAR
    # ─────────────────────────────────────────
    def eliminar(self, nombre: str) -> bool:
        """
        Elimina un producto del ABB por nombre.

        Args:
            nombre (str): Nombre del producto a eliminar.

        Returns:
            bool: True si fue eliminado, False si no existía.
        """
        self.raiz, eliminado = self._eliminar_recursivo(self.raiz, nombre.lower())
        return eliminado

    def _eliminar_recursivo(self, actual: Nodo, nombre: str):
        """Recorre el árbol y elimina el nodo, reubicando hijos si es necesario."""
        if actual is None:
            return None, False

        if nombre < actual.nombre.lower():
            actual.izq, eliminado = self._eliminar_recursivo(actual.izq, nombre)
        elif nombre > actual.nombre.lower():
            actual.der, eliminado = self._eliminar_recursivo(actual.der, nombre)
        else:
            # Caso 1: sin hijos
            if actual.izq is None and actual.der is None:
                return None, True
            # Caso 2: un solo hijo
            if actual.izq is None:
                return actual.der, True
            if actual.der is None:
                return actual.izq, True
            # Caso 3: dos hijos → reemplazar con sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._minimo(actual.der)
            actual.codigo    = sucesor.codigo
            actual.nombre    = sucesor.nombre
            actual.precio    = sucesor.precio
            actual.stock     = sucesor.stock
            actual.categoria = sucesor.categoria
            actual.der, _    = self._eliminar_recursivo(actual.der, sucesor.nombre.lower())
            return actual, True

        return actual, eliminado

    def _minimo(self, nodo: Nodo) -> Nodo:
        """Retorna el nodo con el nombre mínimo (más a la izquierda)."""
        while nodo.izq is not None:
            nodo = nodo.izq
        return nodo

    # ─────────────────────────────────────────
    #  LISTAR EN ORDEN (inorden)
    # ─────────────────────────────────────────
    def listar(self) -> list:
        """
        Retorna todos los productos ordenados por nombre. O(n).

        Returns:
            list: Lista de dicts con los datos de cada producto.
        """
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(self, nodo: Nodo, resultado: list) -> None:
        """Recorrido inorden: izquierda → raíz → derecha."""
        if nodo is not None:
            self._inorden(nodo.izq, resultado)
            resultado.append(nodo.to_dict())
            self._inorden(nodo.der, resultado)

    # ─────────────────────────────────────────
    #  BUSCAR POR CATEGORÍA
    # ─────────────────────────────────────────
    def buscar_por_categoria(self, categoria: str) -> list:
        """
        Retorna todos los productos de una categoría. O(n).

        Args:
            categoria (str): Categoría a filtrar.

        Returns:
            list: Lista de dicts de productos en esa categoría.
        """
        resultado = []
        self._filtrar_categoria(self.raiz, categoria.lower(), resultado)
        return resultado

    def _filtrar_categoria(self, nodo: Nodo, categoria: str, resultado: list) -> None:
        """Recorre todo el árbol filtrando por categoría."""
        if nodo is not None:
            self._filtrar_categoria(nodo.izq, categoria, resultado)
            if nodo.categoria.lower() == categoria:
                resultado.append(nodo.to_dict())
            self._filtrar_categoria(nodo.der, categoria, resultado)

    # ─────────────────────────────────────────
    #  ACTUALIZAR STOCK
    # ─────────────────────────────────────────
    def actualizar_stock(self, nombre: str, nuevo_stock: int) -> bool:
        """
        Actualiza el stock de un producto por nombre.

        Args:
            nombre (str): Nombre del producto.
            nuevo_stock (int): Nuevo valor de stock.

        Returns:
            bool: True si fue actualizado, False si no existe.
        """
        nodo = self.buscar(nombre)
        if nodo:
            nodo.stock = nuevo_stock
            return True
        return False

    # ─────────────────────────────────────────
    #  PERSISTENCIA JSON
    # ─────────────────────────────────────────
    def guardar_estado(self, archivo: str) -> None:
        """
        Persiste el inventario completo en un archivo JSON.

        Args:
            archivo (str): Ruta del archivo JSON.
        """
        productos = self.listar()
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(productos, f, ensure_ascii=False, indent=2)

    @classmethod
    def cargar_estado(cls, archivo: str) -> "ABBInventario":
        """
        Restaura el inventario desde un archivo JSON.

        Args:
            archivo (str): Ruta del archivo JSON.

        Returns:
            ABBInventario: Nueva instancia con los datos cargados.
        """
        with open(archivo, "r", encoding="utf-8") as f:
            productos = json.load(f)
        abb = cls()
        for p in productos:
            abb.insertar(p["codigo"], p["nombre"], p["precio"], p["stock"], p["categoria"])
        return abb