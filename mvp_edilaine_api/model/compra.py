from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Loja

class Compra(Base):
    __tablename__ = 'compra'

    id = Column("pk_compra", Integer, primary_key=True)
    descricao = Column(String(300), unique=True)
    valor = Column(Float)
    data = Column(DateTime, default=datetime.now())

    #Definição do relacionamento entre compra e loja, 
    # o Sqlalchemy tem a responsabilidade de reconstruir esse relacionamento
    lojas = relationship("Loja")

    def __init__(self, descricao:str, valor:float, 
                 data:Union[DateTime, None] = None):
  
        """
        Cria uma Compra

        Argumentos:
            descricao: descricao da compra que foi efetuada
            valor: valor que foi pago na compra
            data: data da compra
        """

        self.descricao = descricao
        self.valor = valor

        # se não for informada, será a data exata da inserção no banco
        if data:
            self.data = data
        
        """
        Adiciona uma loja

        Argumentos:
            nome: nome da loja que foi efetuada a compra.
            endereço: endereço da loja que foi efetuada a compra.
            cep: o cep da loja
            telefone: contato da loja
        """
    def adiciona_loja(self, loja:Loja):
        self.lojas.append(loja)
    