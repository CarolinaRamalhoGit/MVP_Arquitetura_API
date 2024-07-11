# Importação das bibliotecas necessárias
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify
from urllib.parse import unquote
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from model import Session, Produto
from schemas import *
from flask_cors import CORS
import sqlite3

# Conexão com o banco de dados
conn = sqlite3.connect('./database/db.sqlite3')

# Configuração da aplicação
info = Info(title="MVP_CGR_API", version="2.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Definição das Tags
home_tag = Tag(name="Documentação", description="Documentação em Swagger")
produto_tag = Tag(
    name="Produto", description="Visualização, inserção, edição e remoção de produtos")


# Rota de Redirecionamento à raiz da documentação
@app.get('/', tags=[home_tag])
def home():
    """ Redireciona para a tela inicial da documentação em Swagger.
    """
    return redirect('/openapi/swagger')


# Rota de Busca de Produtos cadastrados
@app.get('/lista_produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_lista_produtos():
    """Faz a busca por todos os Produtos cadastrados.
    Retorna uma representação da listagem de produtos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    lista_produtos = session.query(Produto).all()

    if not lista_produtos:
        # se o produto não foi encontrado
        return {"Não há produtos cadastrados": []}, 200
    else:
        # se o produto for encontrado, retorna a representação de produto
        print(lista_produtos)
        return apresenta_lista_produtos(lista_produtos), 200


# Rota de busca de Produto por ID
@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaIdSchema):
    """Faz a busca por um produto a partir de seu ID.
    Retorna uma representação do produto.
    """
    produto_id = query.id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base."
        return {"mensagem": error_msg}, 404
    else:
        # se for encontrado, retorna a representação de produto
        return apresenta_produto(produto), 200


# Rota de Adição de Produto
@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados.
    Retorna uma representação do produto.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        validade=form.validade)
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        return apresenta_produto(produto), 200
    except Exception as e:
        # caso ocorra um erro fora do previsto
        print(e)
        error_msg = "Não foi possível salvar novo item."
        return {"mensagem": error_msg}, 400


# Rota de Remoção de Produto
@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDeleteSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaIdSchema):
    """Deleta um Produto a partir de seu ID.
    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        produto_id = query.dict().get("id")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        produto = session.query(Produto).filter(
            Produto.id == produto_id).first()
        if not produto:
            # se o produto não for encontrado:
            return {"mensagem": "Produto não Encontrado!"}, 404

        # Salvando os dados do produto, antes de excluí-lo:
        produto_data = {
            "id": produto.id,
            "nome": produto.nome,
            "validade": produto.validade
        }

        # Fazendo a remoção:
        count = session.query(Produto).filter(
            Produto.id == produto_id).delete()

        # Commit para efetivar a atualização no banco
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            return {"mesage": "Produto removido!", "Produto": produto_data}
        else:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base"
            return {"mensagem": error_msg}, 404

    except Exception as e:
        print(e)
        return {"mensagem": "Erro interno ao excluir o produto."}, 500


# Rota de Atualização de quantidade e/ou validade do Produto
@app.put('/produto', tags=[produto_tag],
            responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def update_produto(query: ProdutoBuscaIdSchema, form: ProdutoUpdateSchema):
    """Atualiza um Produto a partir de seu ID.
    Retorna uma representação do produto atualizado.
    """
    try:
        produto_id = query.dict().get("id")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        produto = session.query(Produto).filter(
            Produto.id == produto_id).first()
        if not produto:
            # se o produto não for encontrado:
            return {"mensagem": "Produto não Encontrado!"}, 404

        # Salvando os dados do produto, antes de atualizá-lo:
        produto_data = {
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "validade": produto.validade
        }

        # Atualizando os dados do produto:
        produto.quantidade = form.quantidade
        produto.validade = form.validade

        # Commit para efetivar a atualização no banco
        session.commit()

        # retorna a representação do produto atualizado
        return apresenta_produto(produto), 200

    except Exception as e:
        print(e)
        return {"mensagem": "Erro interno ao atualizar o produto."}, 500


# Rota de Busca de produtos por nome
"""Rota temporariamente desabilitada, por não possui implementação no front-end.
Será objeto de futura atualização da aplicação.
"""

'''
@app.get('/lista_produtos_por_nome', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_lista_produtos_por_nome(query: ProdutoBuscaNomeSchema):
    """Faz a busca por todos os Produtos cadastrados.
    Retorna uma representação da listagem de produtos de acordo com o filtro de nome.
    """
    produto_nome = query.nome
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo nome completo ou por parte do nome
    produtos = session.query(Produto).filter(Produto.nome.like(f'%{produto_nome}%')).all()


    if not produtos:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base."
        return {"mensagem": error_msg}, 404
    else:
        # retorna a representação de produto
        # ordenando a lista de produtos pela validade
        produtos.sort(key=lambda x: x.validade)
        return apresenta_lista_produtos(produtos), 200
'''


