FROM python:3.11-slim

# Criar diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor porta da aplicação Flask
EXPOSE 5005

# Executar o app
CMD ["python", "app.py"]
