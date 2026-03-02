from models.product import Producto
from services.inventory_service import InventoryService
from services.storage_service import StorageService

def input_no_vacio(msg: str) -> str:
    while True:
        s = input(msg).strip()
        if s:
            return s
        print("Entrada vacía. Intenta de nuevo.")

def input_entero(msg: str, minimo: int = 0) -> int:
    while True:
        try:
            v = int(input(msg))
            if v < minimo:
                print(f"Debe ser un entero >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Ingresa un número entero válido.")

def input_flotante(msg: str, minimo: float = 0.0) -> float:
    while True:
        try:
            v = float(input(msg))
            if v < minimo:
                print(f"Debe ser un número >= {minimo}.")
                continue
            return v
        except ValueError:
            print("Ingresa un número válido (usa punto decimal si aplica).")

def mostrar(p: Producto) -> None:
    print(f"- [ID: {p.id}] {p.nombre} | Cant: {p.cantidad} | Precio: ${p.precio:,.2f}")

def menu() -> None:
    inv = InventoryService()
    store = StorageService()

    # Carga inicial (si existe archivo).
    try:
        store.cargar(inv)
        print("Inventario cargado correctamente.")
    except Exception as e:
        print(f"No se pudo cargar inventario: {e}")

    while True:
        print("\n===== MENÚ INVENTARIO =====")
        print("1) Añadir producto")
        print("2) Eliminar producto por ID")
        print("3) Actualizar CANTIDAD de un producto")
        print("4) Actualizar PRECIO de un producto")
        print("5) Buscar productos por NOMBRE")
        print("6) Mostrar TODOS los productos")
        print("7) Guardar inventario en archivo")
        print("8) Cargar inventario desde archivo")
        print("0) Salir")
        op = input("Selecciona una opción: ").strip()

        try:
            if op == "1":
                pid = input_no_vacio("ID único: ")
                nombre = input_no_vacio("Nombre: ")
                cant = input_entero("Cantidad (>=0): ", 0)
                precio = input_flotante("Precio (>=0): ", 0.0)
                inv.agregar(Producto(id=pid, nombre=nombre, cantidad=cant, precio=precio))
                print("Producto añadido.")

            elif op == "2":
                pid = input_no_vacio("ID a eliminar: ")
                if inv.eliminar(pid):
                    print("Producto eliminado.")
                else:
                    print("No se encontró un producto con ese ID.")

            elif op == "3":
                pid = input_no_vacio("ID a actualizar cantidad: ")
                cant = input_entero("Nueva cantidad (>=0): ", 0)
                inv.actualizar_cantidad(pid, cant)
                print("Cantidad actualizada.")

            elif op == "4":
                pid = input_no_vacio("ID a actualizar precio: ")
                precio = input_flotante("Nuevo precio (>=0): ", 0.0)
                inv.actualizar_precio(pid, precio)
                print("Precio actualizado.")

            elif op == "5":
                q = input_no_vacio("Texto a buscar en el nombre: ")
                res = inv.buscar_por_nombre(q)
                if not res:
                    print("Sin resultados.")
                else:
                    print(f"Resultados ({len(res)}):")
                    for p in res:
                        mostrar(p)

            elif op == "6":
                todos = inv.listar_todos()
                if not todos:
                    print("Inventario vacío.")
                else:
                    print(f"Listado de productos ({len(todos)}):")
                    for p in todos:
                        mostrar(p)

            elif op == "7":
                store.guardar(inv)
                print(f"Inventario guardado en '{store.ruta}'.")
            
            elif op == "8":
                store.cargar(inv)
                print("Inventario cargado desde archivo.")
            
            elif op == "0":
                # Guardado opcional al salir
                try:
                    store.guardar(inv)
                    print("Cambios guardados. ¡Hasta luego!")
                except Exception as e:
                    print(f"No se pudo guardar al salir: {e}")
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    menu()