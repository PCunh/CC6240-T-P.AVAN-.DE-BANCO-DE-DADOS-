# CC6240 - Tópicos avançados de banco de dados
Projeto de banco de dados

Para o banco de dados, segue o tema:

- Logística inteligente

Supabase (relacional)
  - Dados estruturais e relacionais
  - usuários
  - motoristas
  - empresas
  - autenticação
  - permissões
  - estoque básico

mongoDB (não-relacional)
  - Documentos flexíveis e pedidos
  - pedidos
  - rastreamento
  - histórico de transporte
  - eventos de entrega
    
neo4j (não-relacional)
  - Relacionamentos complexos e cálculos de rota
  - cálculo de rotas
  - conexões entre cidades
  - análise logística
  - menor caminho

# RELATÓRIO SOBRE O PROJETO
### Os requisitos para rodar o projeto são:
- Python 3.10+
- Conta no [Supabase](https://supabase.com)
- Conta no [MongoDB Atlas](https://cloud.mongodb.com)
- Conta no [Neo4j AuraDB](https://console.neo4j.io)

### instalação:
bash
pip install fastapi uvicorn "supabase==2.10.0" pymongo neo4j

### Configuração

Em cada arquivo de banco, preencha as credenciais:

*supabase_db.py*
python
SUPABASE_URL = "https://<seu-projeto>.supabase.co"
SUPABASE_KEY = "<sua-anon-key>"

*mongo_db.py*
python
MONGO_URI = "mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/"

*neo4j_db.py*
python
NEO4J_URI = "neo4j+s://<id>.databases.neo4j.io"
NEO4J_USER = "<usuario>"
NEO4J_PASS = "<senha>"

### Executar o backend

bash
cd PJBancos/backend
uvicorn Main:app --reload

### Executar o frontend

Abra o arquivo PJBancos/frontend/index.html diretamente no navegador.
