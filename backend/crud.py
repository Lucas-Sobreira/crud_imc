from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from schemas import AvalicaoUpdate, AvaliacaoCreate
from models import AvaliacaoModel
from utils import resultado_avaliacao

def get_avaliacoes(db: Session):
    """
    Função que retorna todas as avaliações [SELECT * FROM]
    """
    return db.query(AvaliacaoModel).order_by(text('id asc')).all()

def get_avaliacao(db: Session, avaliacao_id: int):
    """
    Função que retorna a avaliacao filtrada
    """
    return db.query(AvaliacaoModel).filter(AvaliacaoModel.id == avaliacao_id).first()

def create_avaliacao(db: Session, avaliacao: AvaliacaoCreate):
    """
    Função de criação de avaliação [Insert into]
    """
    # transformar minha view para ORM
    db_avaliacao = AvaliacaoModel(**avaliacao.model_dump())

    # Calculando o IMC e a Avaliação do Paciente
    db_avaliacao.imc = round((db_avaliacao.wheight / (db_avaliacao.height**2)), 2)    
    db_avaliacao.result = resultado_avaliacao(db_avaliacao.imc)

    # adicionar na tabela 
    db.add(db_avaliacao)

    # commitar na minha tabela 
    db.commit()

    # fazer o refresh do banco de dados
    db.refresh(db_avaliacao)

    # retornar pro usuario o item criado
    return db_avaliacao

def delete_avaliacao(db: Session, avaliacao_id: int):
    """
    Função que deleta o produto desejado
    """
    # Fitra o produto à ser deletado
    db_avaliacao =  db.query(AvaliacaoModel).filter(AvaliacaoModel.id == avaliacao_id).first()

    # Deleta o produto
    db.delete(db_avaliacao)
    
    # Commita a deleção do produto
    db.commit()

    # retornar pro usuario o item criado
    return db_avaliacao

def update_avaliacao(db: Session, avaliacao_id: int, avaliacao: AvalicaoUpdate):
    """
    Função que atualiza o produto desejado
    """
    db_avaliacao = db.query(AvaliacaoModel).filter(AvaliacaoModel.id == avaliacao_id).first()

    # Verifica se tem alguma avaliação com o ID selecionado
    if db_avaliacao is None: 
        return None
    
    if avaliacao.name is not None: 
        db_avaliacao.name = avaliacao.name
    if avaliacao.height is not None: 
        db_avaliacao.height = avaliacao.height
    if avaliacao.wheight is not None: 
        db_avaliacao.wheight = avaliacao.wheight
    if avaliacao.client_email is not None: 
        db_avaliacao.client_email = avaliacao.client_email

    # Se passar ambas as medidas calcula com os novos valores de peso e altura 
    if (avaliacao.height is not None) and (avaliacao.wheight is not None):
        db_avaliacao.imc = round((avaliacao.wheight / (avaliacao.height**2)), 2)
        db_avaliacao.result = resultado_avaliacao(db_avaliacao.imc)

    # Se passar apenas o peso, então o IMC é calculado utilizando a altura previamente armazenada
    if (avaliacao.height is None) and (avaliacao.wheight is not None):
        db_avaliacao.imc = round((avaliacao.wheight / (db_avaliacao.height**2)), 2)
        db_avaliacao.result = resultado_avaliacao(db_avaliacao.imc)

    # Se passar apenas a altura, então o IMC é calculado utilizando o peso previamente armazenado
    if (avaliacao.height is not None) and (avaliacao.wheight is None):
        db_avaliacao.imc = round((db_avaliacao.wheight / (avaliacao.height**2)), 2)
        db_avaliacao.result = resultado_avaliacao(db_avaliacao.imc)

    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao
    