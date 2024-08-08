from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import SessionLocal, get_db
from schemas import AvaliacaoResponse, AvalicaoUpdate, AvaliacaoCreate
from typing import List
from crud import (
    create_avaliacao, 
    get_avaliacoes,
    get_avaliacao,
    delete_avaliacao,
    update_avaliacao
)

router = APIRouter()

### criar minha rota de buscar todas as avaliações
@router.get("/avaliacoes/", response_model=List[AvaliacaoResponse])
def read_all_avaliacoes(db: Session = Depends(get_db)):
    """
    Rota para buscar todos os itens
    """
    avaliacoes = get_avaliacoes(db)
    return avaliacoes

### criar minha rota de buscar 1 avaliação
@router.get("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoResponse)
def read_one_avaliacao(avaliacao_id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar 1 item
    """
    db_avaliacao = get_avaliacao(db, avaliacao_id=avaliacao_id)
    if db_avaliacao is None: 
        raise HTTPException(status_code=4004, detail="voce está querendo buscar uma avaliação inexistente")
    return db_avaliacao

### criar minha rota de adicionar uma avaliação
@router.post("/avaliacoes/", response_model=AvaliacaoResponse)
def create_avaliacao_route(avaliacao: AvaliacaoCreate, db: Session = Depends(get_db)):
    """
    Rota para adicionar 1 item
    """
    return create_avaliacao(avaliacao=avaliacao, db=db)

### criar minha rota de deletar uma avaliacao
@router.delete("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoResponse)
def delete_avaliacao_router(avaliacao_id: int, db: Session = Depends(get_db)):
    """
    Rota para deletar 1 item
    """
    db_avaliacao = delete_avaliacao(avaliacao_id=avaliacao_id, db=db)
    if db_avaliacao is None: 
        raise HTTPException(status_code=4004, detail="voce está querendo deletar um produto inexistente")
    return db_avaliacao

### criar minha rota de fazer update nas avaliações
@router.put("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoResponse)
def atualizar_avaliacao(avaliacao_id: int, avaliacao: AvalicaoUpdate, db: Session = Depends(get_db)): 
    """
    Rota para realizar update das avaliações
    """
    db_avaliacao = update_avaliacao(db=db, avaliacao_id=avaliacao_id, avaliacao=avaliacao)
    if db_avaliacao is None: 
        raise HTTPException(status_code=4004, detail="voce está querendo realizar Update de uma avaliação inexistente")
    return db_avaliacao