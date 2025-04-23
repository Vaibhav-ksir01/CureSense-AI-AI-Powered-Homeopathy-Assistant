from pyvis.network import Network
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

default_cypher = "MATCH (s)-[r]->(t) RETURN s, r, t"

def showGraph(cypher: str = default_cypher, output_file="graph.html"):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    session = driver.session()

    result = session.run(cypher)
    net = Network(notebook=False, height="800px", width="100%", directed=True)

    node_ids = set() 

    for record in result:
        s = record["s"]["id"]
        t = record["t"]["id"]
        r = record["r"].type 

        if s not in node_ids:
            net.add_node(s, label=str(s), color="lightblue")
            node_ids.add(s)
        if t not in node_ids:
            net.add_node(t, label=str(t), color="lightgreen")
            node_ids.add(t)

        net.add_edge(s, t, label=r, color="gray")

    session.close()


    net.show(output_file, notebook=False)
    print(f"Graph saved to {output_file}. Open it in a browser to view.")

# Run the function
showGraph()
