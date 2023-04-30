from pydantic import BaseModel
from typing import List

from model.loja import Loja

class LojaSchema(BaseModel):
    """Define uma nova loja a ser adicionada"""
    compra_id: int = 1
    nome: str = "ASUS"
    endereco: str = "Rua Francisco, Solo, São Paulo"
    cep: int = 15025354
    telefone: int = 985642365

class LojaDelSchema(BaseModel):
    mesage: str
    nome: str


class LojaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca.
    """
    nome: str = "Teste"

class ListagemLojasSchema(BaseModel):
        lojas:List[LojaSchema]

def apresenta_lojas(lojas: List[Loja]):
        
        result = []
        for loja in lojas:
            result.append({
                "nome": loja.nome,
                "endereco": loja.endereco,
                "cep": loja.cep,
                "telefone": loja.telefone,
            })

        return {"lojas": result}

