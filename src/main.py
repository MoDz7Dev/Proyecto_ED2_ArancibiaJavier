import tkinter as tk
import os
from models.model import ABBInventario
from views.view import View
from controllers.controller import Controller

# ── Ruta del archivo JSON (siempre en src/datos/) ──────────────────────
ARCHIVO_ESTADO = os.path.join(os.path.dirname(__file__), "datos", "inventario.json")


def main():
    # Crea la carpeta datos/ si no existe
    os.makedirs(os.path.dirname(ARCHIVO_ESTADO), exist_ok=True)

    # ── Ventana raíz ──────────────────────────────────────────────────
    root = tk.Tk()
    root.title("Inventario de Productos - ABB")
    root.geometry("1000x650")
    root.minsize(800, 500)
    root.configure(bg="#ffffff")

    # ── MVC ───────────────────────────────────────────────────────────
    # 1. Modelo: carga estado si existe, si no crea ABB vacío
    if os.path.exists(ARCHIVO_ESTADO):
        model = ABBInventario.cargar_estado(ARCHIVO_ESTADO)
    else:
        model = ABBInventario()

    # 2. Vista
    view = View(root)

    # 3. Controlador: conecta modelo y vista
    controller = Controller(model, view, ARCHIVO_ESTADO)

    root.mainloop()


if __name__ == "__main__":
    main()