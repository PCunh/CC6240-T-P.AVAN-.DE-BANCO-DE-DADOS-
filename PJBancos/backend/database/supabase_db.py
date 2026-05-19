from supabase import create_client

SUPABASE_URL = "https://kfwvgxloghjcbqphbnhq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtmd3ZneGxvZ2hqY2JxcGhibmhxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg5NDYxNTAsImV4cCI6MjA5NDUyMjE1MH0.Qzr95P26ig9hqRWc2jilwIKCgoRbrvZcJI6eRcHXq20"

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def criar_empresa(nome, cnpj, endereco):
    return client.table("empresas").insert({"nome": nome, "cnpj": cnpj, "endereco": endereco}).execute()

def listar_empresas():
    return client.table("empresas").select("*").execute()

def atualizar_empresa(id, dados):
    return client.table("empresas").update(dados).eq("id", id).execute()

def deletar_empresa(id):
    return client.table("empresas").delete().eq("id", id).execute()

def criar_motorista(nome, cnh, empresa_id):
    return client.table("motoristas").insert({"nome": nome, "cnh": cnh, "empresa_id": empresa_id}).execute()

def listar_motoristas():
    return client.table("motoristas").select("*").execute()

def atualizar_motorista(id, dados):
    return client.table("motoristas").update(dados).eq("id", id).execute()

def deletar_motorista(id):
    return client.table("motoristas").delete().eq("id", id).execute()

def criar_usuario(email, role="user"):
    return client.table("usuarios").insert({"email": email, "role": role}).execute()

def listar_usuarios():
    return client.table("usuarios").select("*").execute()

def atualizar_usuario(id, dados):
    return client.table("usuarios").update(dados).eq("id", id).execute()

def deletar_usuario(id):
    return client.table("usuarios").delete().eq("id", id).execute()
