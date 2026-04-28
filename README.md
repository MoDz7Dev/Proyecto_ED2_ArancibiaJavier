# Inventario de Productos · Arbol Binario de Busqueda (ABB)

**Materia:** Estructura de Datos 2  
**Estudiante:** Raul Javier Arancibia Añez  
**Registro:** 223041556  

---

Sistema de inventario de productos implementado con un **Arbol Binario de Busqueda (ABB)** como estructura de datos central. Permite insertar, buscar, eliminar y listar productos de forma eficiente, ordenados alfabéticamente por nombre.

El proyecto sigue el patrón de arquitectura **MVC (Modelo - Vista - Controlador)** y utiliza **tkinter** como framework de interfaz gráfica, con **persistencia en JSON** para guardar y restaurar el estado del inventario.

---

## ¿Cómo se aplica el ABB?

Cada producto es un **nodo** del árbol. El árbol se ordena por el **nombre del producto**:

```
              [Leche]                ← Raíz
             /       \
         [Arroz]     [Pan]          ← Nivel 1
              \      /
          [Azúcar] [Mantequilla]    ← Nivel 2 (hojas)
```

- Todo nodo a la **izquierda** tiene nombre **menor** alfabéticamente
- Todo nodo a la **derecha** tiene nombre **mayor** alfabéticamente

### Operaciones implementadas

| Operación | Descripción |
|---|---|
| `insertar` | Agrega un producto en su posición correcta |
| `buscar` | Encuentra un producto por nombre |
| `eliminar` | Elimina un producto (3 casos) |
| `listar` | Recorrido inorden → orden alfabético |
| `buscar_por_categoria` | Filtra productos por categoría |
| `actualizar_stock` | Modifica el stock de un producto |

### Recorrido Inorden

El recorrido **inorden** (izquierda → raíz → derecha) produce la lista ordenada automáticamente:

```
inorden →  Arroz, Azúcar, Leche, Mantequilla, Pan
```

---

## Estructura del proyecto

```
src/
├── main.py                  ← Punto de entrada, instancia MVC
├── models/
│   ├── __init__.py
│   └── model.py             ← Nodo + ABBInventario (lógica pura)
├── views/
│   ├── __init__.py
│   └── view.py              ← Interfaz gráfica con tkinter
└── controllers/
    ├── __init__.py
    └── controller.py        ← Conecta modelo y vista
```

### Patrón MVC

```
Vista (view.py)
    │  el usuario hace clic en un botón
    ▼
Controlador (controller.py)
    │  valida datos y llama al modelo
    ▼
Modelo (model.py)
    │  ejecuta la operación en el ABB
    ▼
Controlador
    │  recibe el resultado
    ▼
Vista
    │  actualiza la tabla y muestra mensaje
```

---

## REQUERIMIENTOS

### 1. Requisitos

- Python 3.10 o superior
- tkinter (viene incluido con Python en Windows)

### 2. Clonar o descargar el repositorio

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO
```

### 3. Ejecutar

Desde la carpeta `src/`:

```bash
cd src
python main.py
```

### 4. Primera ejecución

Si no existe el archivo `datos/inventario.json`, el sistema crea automáticamente la carpeta `datos/` y arranca con el inventario vacío.

Si ya existe el archivo, carga el inventario guardado anteriormente.

---

## Persistencia JSON

El inventario se guarda en `src/inventario.json`. El Arbol se **aplana** con recorrido inorden antes de guardar, y se **reconstruye** insertando cada producto al cargar:

```json
[
  {
    "codigo": "P-001",
    "nombre": "Arroz",
    "precio": 12.50,
    "stock": 100,
    "categoria": "Alimentos"
  }
]
```