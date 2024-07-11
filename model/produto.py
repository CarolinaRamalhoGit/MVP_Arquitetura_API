from sqlalchemy import Column, String, Integer, Date, DateTime, Float
from datetime import datetime
from typing import Union
from model import Base


class Produto(Base):
    __tablename__ = 'produto'

    id = Column("pk_produto", Integer, primary_key=True)
    nome = Column(String(140))
    quantidade = Column(Integer)
    validade = Column(Date)  
    data_insercao = Column(DateTime, default=datetime.now())  

    def __init__(self, nome: str, quantidade: int, validade: str,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Produto com os seguintes argumentos:
            nome: nome do produto.
            quantidade: quantidade daquele produto para uma data de vencimento específica
            validade: data de vencimento do produto
            data_insercao: data de quando o produto foi inserido à base
        """
        self.nome = nome
        self.quantidade = quantidade
        self.validade = validade
        if data_insercao:
            # se não for informada, será a data exata da inserção no banco
            self.data_insercao = data_insercao