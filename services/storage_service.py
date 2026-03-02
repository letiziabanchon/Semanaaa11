import json
from pathlib import Path
from typing import Optional
from services.inventory_service import InventoryService

class StorageService:
    """
    Persistencia sencilla en JSON (estándar de Python).
    Guarda/lee una lista de productos {id, nombre, cantidad, precio}.
    """
    def __init__(self, ruta_archivo: Optional[str] = None) -> None:
        self.ruta = Path(ruta_archivo or "data/inventario.json")
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def guardar(self, inventario: InventoryService) -> None:
        data = inventario.as_list_of_dicts()
        with self.ruta.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar(self, inventario: InventoryService) -> None:
        if not self.ruta.exists():
            # Si no hay archivo, se considera inventario vacío.
            inventario.load_from_list_of_dicts([])
            return
        with self.ruta.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("El archivo de inventario tiene un formato inválido.")
        inventario.load_from_list_of_dicts(data)