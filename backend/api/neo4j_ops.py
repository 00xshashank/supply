from neo4j import GraphDatabase

import os
from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_UNAME = os.getenv("NEO4J_UNAME")
NEO4J_AUTH = (NEO4J_UNAME, NEO4J_PASSWORD)

required_env_vars = {
    "NEO4J_URI": NEO4J_URI,
    "NEO4J_UNAME": NEO4J_UNAME,
    "NEO4J_PASSWORD": NEO4J_PASSWORD,
}
for var in required_env_vars:
    if not var:
        raise ValueError(f"{required_env_vars[var]} not declared in environment variables.")

driver = GraphDatabase.driver(uri=NEO4J_URI, auth=(NEO4J_UNAME, NEO4J_PASSWORD))

def retrieve_graph(projectId: str):
    CYPHER_QUERY=f"""
    MATCH (n)-[r]->(m)
    WHERE r.projectId = '{projectId}'
    OR n:{projectId}
    OR m:{projectId}
    RETURN DISTINCT n, r, m
    """

    with driver.session() as session:
        result = session.run(CYPHER_QUERY)
        return [record.data() for record in result]
    
if __name__ == "__main__":
    print(retrieve_graph('aaaaaaaaaaa'))

