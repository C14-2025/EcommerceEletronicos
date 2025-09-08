from fastapi import APIRouter

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/")
def listar_usuarios():
    return [{"id": 1, "nome": "João"}]
