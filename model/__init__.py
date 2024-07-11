from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from model.base import Base
from model.produto import Produto

# Define o caminho do diretório onde o banco de dados será armazenado
db_path = "database/"

# Verifica se o diretório não existe
if not os.path.exists(db_path):
   # Se não existir, cria o diretório
   os.makedirs(db_path)

# Cria a url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Verifica se o banco de dados não existe
if not database_exists(engine.url):
    # Se não existir, cria o banco 
    create_database(engine.url) 

# Cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)