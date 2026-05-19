from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

sys.path.append(os.path.dirname(__file__))

from database import supabase_db, mongo_db, neo4j_db

app = FastAPI()

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"],)

class Empresa(BaseModel):
    nome: str
    cnpj: str
    endereco: str

class Motorista(BaseModel):
    nome: str
    cnh: str
    empresa_id: str

class Usuario(BaseModel):
    email: str
    role: Optional[str] = "user"

class Pedido(BaseModel):
    origem: str
    destino: str
    motorista_id: str
    empresa_id: str
    itens: List[dict]

class Evento(BaseModel):
    status: str
    localizacao: str
    observacao: Optional[str] = ""

class Rastreamento(BaseModel):
    lat: float
    lng: float
    velocidade: Optional[float] = None

class Cidade(BaseModel):
    nome: str
    estado: str

class Rota(BaseModel):
    origem: str
    destino: str
    distancia: int
    tempo: int
    custo: float

@app.post("/empresas")
def criar_empresa(e: Empresa):
    return supabase_db.criar_empresa(e.nome, e.cnpj, e.endereco).data

@app.get("/empresas")
def listar_empresas():
    return supabase_db.listar_empresas().data

@app.put("/empresas/{id}")
def atualizar_empresa(id: str, dados: dict):
    return supabase_db.atualizar_empresa(id, dados).data

@app.delete("/empresas/{id}")
def deletar_empresa(id: str):
    return supabase_db.deletar_empresa(id).data



@app.post("/motoristas")
def criar_motorista(m: Motorista):
    return supabase_db.criar_motorista(m.nome, m.cnh, m.empresa_id).data

@app.get("/motoristas")
def listar_motoristas():
    return supabase_db.listar_motoristas().data

@app.delete("/motoristas/{id}")
def deletar_motorista(id: str):
    return supabase_db.deletar_motorista(id).data



@app.post("/usuarios")
def criar_usuario(u: Usuario):
    return supabase_db.criar_usuario(u.email, u.role).data

@app.get("/usuarios")
def listar_usuarios():
    return supabase_db.listar_usuarios().data

@app.delete("/usuarios/{id}")
def deletar_usuario(id: str):
    return supabase_db.deletar_usuario(id).data



@app.post("/pedidos")
def criar_pedido(p: Pedido):
    id = mongo_db.criar_pedido(p.origem, p.destino, p.motorista_id, p.empresa_id, p.itens)
    return {"id": id}

@app.get("/pedidos")
def listar_pedidos():
    pedidos = mongo_db.listar_pedidos()
    for p in pedidos:
        p["_id"] = str(p["_id"])
    return pedidos



@app.get("/pedidos/{id}")
def buscar_pedido(id: str):
    pedido = mongo_db.buscar_pedido(id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido["_id"] = str(pedido["_id"])
    return pedido

@app.delete("/pedidos/{id}")
def deletar_pedido(id: str):
    mongo_db.deletar_pedido(id)
    return {"ok": True}



@app.post("/pedidos/{id}/eventos")
def adicionar_evento(id: str, e: Evento):
    mongo_db.adicionar_evento(id, e.status, e.localizacao, e.observacao)
    return {"ok": True}

@app.get("/pedidos/{id}/eventos")
def listar_eventos(id: str):
    eventos = mongo_db.listar_eventos(id)
    for e in eventos:
        if "timestamp" in e:
            e["timestamp"] = str(e["timestamp"])
    return eventos

@app.post("/pedidos/{id}/rastreamento")
def registrar_rastreamento(id: str, r: Rastreamento):
    rid = mongo_db.registrar_rastreamento(id, r.lat, r.lng, r.velocidade)
    return {"id": rid}

@app.get("/pedidos/{id}/rastreamento")
def listar_rastreamento(id: str):
    docs = mongo_db.listar_rastreamento(id)
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs




@app.post("/cidades")
def criar_cidade(c: Cidade):
    neo4j_db.criar_cidade(c.nome, c.estado)
    return {"ok": True}

@app.get("/cidades")
def listar_cidades():
    return neo4j_db.listar_cidades()

@app.delete("/cidades/{nome}")
def deletar_cidade(nome: str):
    neo4j_db.deletar_cidade(nome)
    return {"ok": True}



@app.post("/rotas")
def criar_rota(r: Rota):
    neo4j_db.criar_rota(r.origem, r.destino, r.distancia, r.tempo, r.custo)
    return {"ok": True}

@app.get("/rotas")
def listar_rotas():
    return neo4j_db.listar_rotas()

@app.delete("/rotas/{origem}/{destino}")
def deletar_rota(origem: str, destino: str):
    neo4j_db.deletar_rota(origem, destino)
    return {"ok": True}

@app.get("/rotas/menor-caminho")
def menor_caminho(origem: str, destino: str):
    resultado = neo4j_db.menor_caminho(origem, destino)
    if not resultado:
        raise HTTPException(status_code=404, detail="Caminho não encontrado")
    return resultado