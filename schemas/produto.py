from pydantic import BaseModel, validator
from typing import Optional, List
from model.produto import Produto
from datetime import datetime, date


class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Presunto Fatiado"
    quantidade: int = 6
    validade: str = datetime.now().date().strftime("%d/%m/%Y")

    @validator('validade')
    def parse_validade(cls, v):
        try:
            return datetime.strptime(v, "%d/%m/%Y").date()  # Converte de dd/mm/aaaa para date
        except ValueError:
            raise ValueError("Formato de data inválido. Use dd/mm/aaaa")


class ProdutoUpdateSchema(BaseModel):
    """ Define como um produto a ser editado deve ser representado
    """
    quantidade: int = 6
    validade: str = datetime.now().date().strftime("%d/%m/%Y")

    @validator('validade')
    def parse_validade(cls, v):
        try:
            return datetime.strptime(v, "%d/%m/%Y").date()  # Converte de dd/mm/aaaa para date
        except ValueError:
            raise ValueError("Formato de data inválido. Use dd/mm/aaaa")


class ProdutoDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mensagem: str
    id: int = 1


class ProdutoBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por Id.
        A busca será feita com base apenas no Id do produto.
    """
    id: int = 1


class ProdutoBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por Id.
        A busca será feita com base apenas no Id do produto.
    """
    nome: str = "Presunto Fatiado"


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos: List[ProdutoSchema]


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado
    """
    id: int = 1
    nome: str = "Presunto Fatiado"
    quantidade: int = 6
    validade: str = datetime.now().date().strftime("%d/%m/%Y")

    @validator('validade')
    def parse_validade(cls, v):
        try:
            return datetime.strptime(v, "%d/%m/%Y").date()  # Converte de dd/mm/aaaa para date
        except ValueError:
            raise ValueError("Formato de data inválido. Use dd/mm/aaaa")


# Função auxiliar para apresentar um produto
def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em ProdutoViewSchema
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "validade": produto.validade
    }

# Função auxiliar para apresentar uma lista de produtos
def apresenta_lista_produtos(lista_produtos: List[Produto]):
    """ Retorna uma representação da lista de produtos seguindo 
        seguindo, para cada produto, o schema definido em ProdutoViewSchema.
    """
    result = []
    for produto in lista_produtos:
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "validade": produto.validade
        })
    return {"Lista de produtos": result}