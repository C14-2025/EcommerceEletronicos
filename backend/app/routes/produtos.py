from fastapi import APIRouter

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("/")
def listar_produtos():
    return [{"id": 1, "nome": "Notebook", "preco": 3500.00}]
