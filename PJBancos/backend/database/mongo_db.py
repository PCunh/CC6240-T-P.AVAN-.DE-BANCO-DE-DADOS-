from pymongo import MongoClient
from bson import ObjectId

MONGO_URI = "mongodb+srv://unifcfonseca_db_user:UH43jqZLTMsiz2dX@pj-tpa-banco-de-dados.oqjdivy.mongodb.net/?appName=PJ-TPA-BANCO-DE-DADOS"

client = MongoClient(MONGO_URI)
db = client["logistica"]

def criar_pedido(origem, destino, motorista_id, empresa_id, itens):
    pedido = {
        "origem": origem,
        "destino": destino,
        "motorista_id": motorista_id,
        "empresa_id": empresa_id,
        "itens": itens,
        "status": "pendente",
        "eventos": []
    }
    result = db.pedidos.insert_one(pedido)
    return str(result.inserted_id)

def listar_pedidos():
    return list(db.pedidos.find({}, {"_id": 1, "origem": 1, "destino": 1, "status": 1}))

def buscar_pedido(id):
    return db.pedidos.find_one({"_id": ObjectId(id)})

def atualizar_pedido(id, dados):
    return db.pedidos.update_one({"_id": ObjectId(id)}, {"$set": dados})

def deletar_pedido(id):
    return db.pedidos.delete_one({"_id": ObjectId(id)})

def adicionar_evento(pedido_id, status, localizacao, observacao=""):
    from datetime import datetime
    evento = {"status": status, "localizacao": localizacao, "observacao": observacao, "timestamp": datetime.now()}
    db.pedidos.update_one({"_id": ObjectId(pedido_id)},{"$push": {"eventos": evento},"$set": {"status": status}}
    )
def listar_eventos(pedido_id):
    pedido = db.pedidos.find_one({"_id": ObjectId(pedido_id)}, {"eventos": 1})
    if not pedido:
        return []
    return pedido.get("eventos", [])

def registrar_rastreamento(pedido_id, lat, lng, velocidade=None):
    from datetime import datetime
    doc = {"pedido_id": pedido_id, "lat": lat, "lng": lng, "velocidade": velocidade, "timestamp": datetime.now()}
    result = db.rastreamento.insert_one(doc)
    return str(result.inserted_id)

def listar_rastreamento(pedido_id):
    return list(db.rastreamento.find({"pedido_id": pedido_id}))
