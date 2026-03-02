from dataclasses import dataclass, asdict

@dataclass
class Producto:
    """
    Clase Producto
    Atributos:
      - id (str): identificador único.
      - nombre (str)
      - cantidad (int)
      - precio (float)
    Incluye getters/setters con validaciones y utilidades de serialización.
    """
    id: str
    nombre: str
    cantidad: int
    precio: float

    # -------- Getters --------
    def get_id(self) -> str:
        return self.id

    def get_nombre(self) -> str:
        return self.nombre

    def get_cantidad(self) -> int:
        return self.cantidad

    def get_precio(self) -> float:
        return self.precio

    # -------- Setters (con validaciones simples) --------
    def set_nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.nombre = nuevo_nombre.strip()

    def set_cantidad(self, nueva_cantidad: int) -> None:
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            raise ValueError("La cantidad debe ser un entero mayor o igual a 0.")
        self.cantidad = nueva_cantidad

    def set_precio(self, nuevo_precio: float) -> None:
        if not isinstance(nuevo_precio, (int, float)) or nuevo_precio < 0:
            raise ValueError("El precio debe ser un número mayor o igual a 0.")
        self.precio = float(nuevo_precio)

    # -------- Utilidades de (de)serialización --------
    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Producto":
        return Producto(
            id=str(d["id"]),
            nombre=str(d["nombre"]),
            cantidad=int(d["cantidad"]),
            precio=float(d["precio"]),
        )