from datetime import date, datetime
from pydantic import BaseModel
from typing import List
from model.compra import Compra

from schemas import LojaSchema


class CompraSchema(BaseModel):
    """ Define como um nova compra a ser adicionada deve ser representada
    """

    descricao: str = "Notebook - Nitro 5"
    valor: float = 5000.00
    data: date = datetime.strptime('27/04/2023', '%d/%m/%Y').date()


class CompraBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na descrição da compra.
    """
    descricao: str = "Teste"
    #id: int


class ListagemComprasSchema(BaseModel):
    """ Define como uma listagem de compras será retornada.
    """
    compras:List[CompraSchema]


def apresenta_compras(compras: List[Compra]):
    """ Retorna uma representação da compra seguindo o schema definido em
       CompraViewSchema.
    """
    result = []
    for compra in compras:
        result.append({
            "id": compra.id,
            "descricao": compra.descricao,
            "valor": compra.valor,
            "data": compra.data,
        })

    return {"compras": result}


class CompraViewSchema(BaseModel):
    """ Define como uma compra será retornada: compra 
    """
    id: int = 1
    descricao: str = "Notebook - Nitro 5"
    valor: float = 5000.00
    data: date = datetime.strptime('27/04/2023', '%d/%m/%Y').date()
    total_lojas: int = 1
    lojas:List[LojaSchema]


class CompraDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

def apresenta_compra(compra: Compra):
    """ Retorna uma representação da compra seguindo o schema definido em
        CompraViewSchema.
    """
    return {
        "id": compra.id,
        "descricao": compra.descricao,
        "valor": compra.valor,
        "data": compra.data,
        "total_lojas": len(compra.lojas),
        "lojas": [{"nome": l.nome} for l in compra.lojas]
        
    }
