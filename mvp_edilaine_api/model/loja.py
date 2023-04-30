from sqlalchemy import Column, String, Integer, ForeignKey

from model import Base

class Loja(Base):
    __tablename__ = 'loja'

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), unique=True)
    endereco = Column(String(300))
    cep = Column(Integer)
    telefone = Column(Integer)
    
    #Definição do relacionamento entre compra e loja

    compra = Column(Integer, ForeignKey("compra.pk_compra"), nullable=False)

    def __init__(self, nome:str, endereco:str, cep:int, telefone:int):
  
        """
        Cria uma loja

        Arguments:
            nome: nome da loja que foi efetuada a compra.
            endereço: endereço da loja que foi efetuada a compra.
            cep: o cep da loja
            telefone: contato da loja
        """
        self.nome = nome
        self.endereco = endereco
        self.cep = cep
        self.telefone = telefone


        
    