from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://9e818cf4.databases.neo4j.io"
NEO4J_USER = "9e818cf4"
NEO4J_PASS = "KkgQhYIvDeA3dCW9rowUaZyjZDnCvZw6-8XFZuYHzZM"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

def criar_cidade(nome, estado):
    with driver.session() as s:
        s.run("MERGE (:City {name: $nome, state: $estado})", nome=nome, estado=estado)

def listar_cidades():
    with driver.session() as s:
        result = s.run("MATCH (c:City) RETURN c.name AS nome, c.state AS estado")
        return [r.data() for r in result]

def deletar_cidade(nome):
    with driver.session() as s:
        s.run("MATCH (c:City {name: $nome}) DETACH DELETE c", nome=nome)

def criar_rota(origem, destino, distancia, tempo, custo):
    with driver.session() as s:
        s.run("""
            MATCH (a:City {name: $origem}), (b:City {name: $destino})
            MERGE (a)-[:ROAD_TO {distance: $distancia, time: $tempo, cost: $custo}]->(b)
        """, origem=origem, destino=destino, distancia=distancia, tempo=tempo, custo=custo)

def listar_rotas():
    with driver.session() as s:
        result = s.run("""
            MATCH (a:City)-[r:ROAD_TO]->(b:City)
            RETURN a.name AS origem, b.name AS destino, r.distance AS distancia, r.time AS tempo, r.cost AS custo
        """)
        return [r.data() for r in result]

def deletar_rota(origem, destino):
    with driver.session() as s:
        s.run("""
            MATCH (a:City {name: $origem})-[r:ROAD_TO]->(b:City {name: $destino})
            DELETE r
        """, origem=origem, destino=destino)

def menor_caminho(origem, destino):
    with driver.session() as s:
        result = s.run("""
            MATCH (a:City {name: $origem}), (b:City {name: $destino}),
            p = shortestPath((a)-[:ROAD_TO*]->(b))
            RETURN [n IN nodes(p) | n.name] AS caminho,
                   reduce(d=0, r IN relationships(p) | d + r.distance) AS distancia_total
        """, origem=origem, destino=destino)
        record = result.single()
        return record.data() if record else None
