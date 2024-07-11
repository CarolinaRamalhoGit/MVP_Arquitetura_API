# Define a imagem base
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho 
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte para o diretório de trabalho
COPY . .

# Define o comando a ser executado quando o container for iniciado
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]