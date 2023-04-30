from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Compra, Loja
from logger import logger
from schemas import *
from flask_cors import CORS
from datetime import datetime

info = Info(title="Edilaine MVP", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger da API Compras")
compra_tag = Tag(name="Compra", description="Adição, visualização e remoção de compras da base")
loja_tag = Tag(name="Loja", description="Adição de loja onde a compra foi efetuada")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para a documentação em Swagger.
    """
    return redirect('/openapi/swagger')
    

@app.post('/compra', tags=[compra_tag],
          responses={"200": CompraViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_compra(form: CompraSchema):
     """Adiciona uma nova compra à base de dados

    Retorna uma representação das compras.
    """
     compra = Compra(
        descricao=form.descricao,
        valor=form.valor,
        data=form.data)
     logger.debug(f"Adicionando compra de descrição: '{compra.descricao}'")
     try:
        #criar conexão com a base
        session = Session()
        #adiciona compra
        session.add(compra)
        #efetivando a ativação de uma nova compra
        session.commit()
        logger.debug(f"Adicionada compra de descrição: '{compra.descricao}'")
        return apresenta_compra(compra), 200

     except IntegrityError as e:
            # como a duplicidade da descrição é a provável razão do IntegrityError
            error_msg = "Compra com a mesma descrição, já salva na base :/"
            logger.warning(f"Erro ao adicionar compra '{compra.descricao}', {error_msg}")
            return {"mesage": error_msg}, 409

     except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar a nova compra:/"
            logger.warning(f"Erro ao adicionar a compra '{compra.descricao}', {error_msg}")
            return {"mesage": error_msg}, 400
    

@app.get('/compras', tags=[compra_tag],
         responses={"200": ListagemComprasSchema, "404": ErrorSchema})
def get_compras():
    """Faz a busca por todos as Compras cadastradas

    Retorna uma representação da listagem de compras.
    """

    logger.debug(f"Coletando compras ")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    compras = session.query(Compra).all()

    if not compras:
        
        return {"compras": []}, 200
    else:
       logger.debug(f"%d compras encontradas" % len(compras))
       #retorna a apresentação de compras
       print(compras)
       return apresenta_compras(compras), 200
    
@app.get('/compra', tags=[compra_tag],
         responses={"200": CompraViewSchema, "404": ErrorSchema})
def get_compra(query: CompraBuscaSchema):
    """Faz a busca por um Compra a partir da descrição da compra

    Retorna uma representação das compras e lojas associadas.
    """
    compra_descricao = query.descricao
    logger.debug(f"Coletando dados sobre a compra #{compra_descricao}")

    session = Session()

    compra = session.query(Compra).filter(Compra.descricao == compra_descricao).first()

    if not compra:
        # se o compra não foi encontrado
        error_msg = "compra não encontrada na base :/"
        logger.warning(f"Erro ao buscar compra '{compra_descricao}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"compra econtrada: '{compra.descricao}'")
        # retorna a representação de produto
        return apresenta_compra(compra), 200
    
@app.delete('/compra', tags=[compra_tag],
            responses={"200": CompraDelSchema, "404": ErrorSchema})
def del_compra(query: CompraBuscaSchema):

        """Deleta uma Compra a partir da descrição informada

        Retorna uma mensagem de confirmação da remoção.
        """
        compra_descricao = unquote(unquote(query.descricao))
        print(compra_descricao)
        logger.debug(f"Deletando dados sobre compra #{compra_descricao}")
        session = Session()
        count = session.query(Compra).filter(Compra.descricao == compra_descricao).delete()
        session.commit()

        if count:
            logger.debug(f"Deletada compra #{compra_descricao}")
            return{"mesage": "Compra removida", "id": compra_descricao}
        else:
            error_msg = "Compra não encontrada na base :/"
            logger.warning(f"Erro ao deletar compra #'{compra_descricao}', {error_msg}")
            return {"mesage": error_msg}, 404
        
@app.post('/loja', tags=[loja_tag],
          responses={"200": CompraViewSchema, "404": ErrorSchema})
def add_loja(form: LojaSchema):
     """Adiciona uma nova loja á uma compra cadastrada na base identificada pelo id
     Retorna uma representação das compras e lojas"""

     compra_id = form.compra_id
     logger.debug(f"Adicionando loja a compra #{compra_id}")
     session = Session()
     compra = session.query(Compra).filter(Compra.id == compra_id).first()

     if not compra:
          error_msg = "Compra não encontrada na base:/"
          logger.warning(f"Erro ao adicionar loja a compra efetuada '{compra_id}', {error_msg}")
          return {"mesage": error_msg}, 404
     
     # criando a loja
     nome = form.nome
     endereco = form.endereco
     cep = form.cep
     telefone = form.telefone
     loja = Loja(nome, endereco, cep, telefone)

     #adicionando loja a compra
     compra.adiciona_loja(loja)
     session.commit()

     logger.debug(f"Adicionando loja a compra #{compra_id}")

     #retorna a representação de compra
     return apresenta_compra(compra), 200

@app.delete('/loja', tags=[loja_tag],
            responses={"200": LojaDelSchema, "404": ErrorSchema})
def del_loja(query: LojaBuscaSchema):

        """Deleta uma Loja a partir do nome informado

        Retorna uma mensagem de confirmação da remoção.
        """
        loja_nome = unquote(unquote(query.nome))
        print(loja_nome)
        logger.debug(f"Deletando dados sobre a loja #{loja_nome}")
        session = Session()
        count = session.query(Loja).filter(Loja.nome == loja_nome).delete()
        session.commit()

        if count:
            logger.debug(f"Deletado loja #{loja_nome}")
            return{"mesage": "Loja removida", "id": loja_nome}
        else:
            error_msg = "Loja não encontrada na base :/"
            logger.warning(f"Erro ao deletar loja #'{loja_nome}', {error_msg}")
            return {"mesage": error_msg}, 404
        
@app.get('/lojas', tags=[loja_tag],
         responses={"200": ListagemLojasSchema, "404": ErrorSchema})
def get_lojas():
    """Faz a busca por todos as Lojas cadastradas

    Retorna uma representação da listagem de lojas.
    """

    logger.debug(f"Coletando lojas ")

    # criando conexão com a base
    session = Session()
    # fazendo a busca
    lojas = session.query(Loja).all()

    if not lojas:
        
        return {"lojas": []}, 200
    else:
       logger.debug(f"%d lojas encontradas" % len(lojas))
       #retorna a apresentação das lojas
       print(lojas)
       return apresenta_lojas(lojas), 200