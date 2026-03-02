from typing import Dict, List
from models.product import Producto

class InventoryService:
    """
    Servicio de dominio para gestionar el inventario en memoria.
    Implementación principal: dict[str, Producto] para O(1) promedio al
    acceder por ID. Se apoyan listas para búsquedas por nombre y total.
    """
    def __init__(self) -> None:
        self._productos: Dict[str, Producto] = {}

    # -------- Operaciones CRUD --------
    def agregar(self, producto: Producto) -> None:
        if producto.id in self._productos:
            raise ValueError(f"Ya existe un producto con id '{producto.id}'.")
        self._productos[producto.id] = producto

    def eliminar(self, product_id: str) -> bool:
        """Elimina por ID. Devuelve True si existía y se eliminó."""
        return self._productos.pop(product_id, None) is not None

    def actualizar_cantidad(self, product_id: str, nueva_cantidad: int) -> None:
        p = self._obtener_o_error(product_id)
        p.set_cantidad(nueva_cantidad)

    def actualizar_precio(self, product_id: str, nuevo_precio: float) -> None:
        p = self._obtener_o_error(product_id)
        p.set_precio(nuevo_precio)

    # -------- Consultas --------
    def buscar_por_nombre(self, texto: str) -> List[Producto]:
        """Búsqueda parcial y no sensible a mayúsculas/minúsculas."""
        q = (texto or "").strip().lower()
        if not q:
            return []
        return [p for p in self._productos.values() if q in p.nombre.lower()]

    def listar_todos(self) -> List[Producto]:
        """Devuelve una lista ordenada por nombre."""
        return sorted(self._productos.values(), key=lambda p: p.nombre.lower())

    # -------- Soporte para persistencia --------
    def as_list_of_dicts(self) -> List[dict]:
        return [p.to_dict() for p in self._productos.values()]

    def load_from_list_of_dicts(self, items: List[dict]) -> None:
        self._productos.clear()
        for d in items:
            p = Producto.from_dict(d)
            # Si hubiera duplicados en el archivo, el último gana.
            self._productos[p.id] = p

    # -------- Utilidad privada --------
    def _obtener_o_error(self, product_id: str) -> Producto:
        p = self._productos.get(product_id)
        if not p:
            raise KeyError(f"No existe producto con id '{product_id}'.")
        return p