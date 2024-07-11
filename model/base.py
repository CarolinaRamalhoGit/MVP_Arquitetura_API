"""
Criação de uma superclasse Base para o instanciamento de novos objetos/tabelas,
a partir de funcionalidades e convenções definidas pelo SQLAlchemy. 
As demais classes do modelo herdarão as propriedades desta superclasse.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()