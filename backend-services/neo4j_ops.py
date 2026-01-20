from neo4j import GraphDatabase
import os

from dotenv import load_dotenv
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_UNAME = os.getenv("NEO4J_UNAME")
NEO4J_AUTH = (NEO4J_URI, NEO4J_PASSWORD)

env_vars = [NEO4J_UNAME, NEO4J_PASSWORD, NEO4J_URI]
for var in env_vars:
    if not var:
        raise ValueError(f"{var} not declared in environment variables.")

driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)

def run_graphdb_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]
