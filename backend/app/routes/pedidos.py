from fastapi import APIRouter

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.get("/")
def listar_pedidos():
    return [{"id": 1, "usuario_id": 1, "status": "pendente"}]
