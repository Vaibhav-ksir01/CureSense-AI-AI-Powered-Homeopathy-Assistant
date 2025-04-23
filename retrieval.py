from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE

# Neo4j Connection Class
class Neo4jConnector:
    def __init__(self, uri, user, password, database):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database
        try:
            # Test connection
            with self._driver.session(database=self._database) as session:
                session.run("RETURN 1")
        except Exception as e:
            print(f"Connection failed: {e}")

    def query(self, cypher_query, parameters=None):
        with self._driver.session(database=self._database) as session:
            result = session.run(cypher_query, parameters)
            return [record.data() for record in result]

    def close(self):
        self._driver.close()

def store_query(word):
    cypher_query = f"""
        MATCH p=(n:Document)-[]->(related)
        WHERE n.text CONTAINS '{word}'
        RETURN related LIMIT 25
        UNION
        MATCH p=(related)-[]->(n:Document)
        WHERE n.text CONTAINS '{word}'
        RETURN related LIMIT 25
        """
    return cypher_query

# Function to Retrieve Data from Neo4j
def retrieve_knowledge(words):
    neo4j_connector = Neo4jConnector(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, NEO4J_DATABASE)
    results = []
    for word in words:
        cypher_query = store_query(word)
        results.extend(neo4j_connector.query(cypher_query))
    neo4j_connector.close()
    return results