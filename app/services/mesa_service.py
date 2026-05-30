from app.repositories import mesa_repository

def list_mesas():
    return mesa_repository.obtener_mesas()

def register_mesa(numero_mesa, estado="libre"):
    return mesa_repository.crear_mesa(numero_mesa, estado)

def get_mesa_by_id(id_mesa):
    return mesa_repository.obtener_mesa_por_id(id_mesa)

def register_client_for_table(nombre, id_mesa):
    return mesa_repository.registrar_cliente_mesa(nombre, id_mesa)

def ocupar_mesa(id_mesa):
    mesa_repository.ocupar_mesa(id_mesa)

def delete_mesa(id_mesa):
    return mesa_repository.eliminar_mesa(id_mesa)
