from app.repositories.dashboard_repository import (
    contar_mesas, contar_pedidos, contar_productos,
    contar_usuarios, contar_categorias,
    obtener_ultimos_pedidos, ingresos_hoy
)

def obtener_resumen():
    return {
        "mesas": contar_mesas(),
        "pedidos_hoy": contar_pedidos(),
        "productos": contar_productos(),
        "usuarios": contar_usuarios(),
        "categorias": contar_categorias(),
        "ultimos_pedidos": obtener_ultimos_pedidos(),
        "ingresos_hoy": ingresos_hoy(),
    }
