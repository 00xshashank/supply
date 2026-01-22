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

driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

def run_graphdb_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]

def get_all_nodes(project_id: str):
    with driver.session() as session:
        result = session.run(f"MATCH (n:id_{project_id}) RETURN n")
        return [record["n"] for record in result]
    
# print(get_all_nodes("8bhqfqn9yh"))
