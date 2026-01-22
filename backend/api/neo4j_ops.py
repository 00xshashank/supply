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

def get_all_nodes(project_id: str):
    with driver.session() as session:
        result = session.run(f"""
            MATCH (n:{project_id})-[r]-(m:{project_id})
            RETURN 
                elementId(n) AS n_id,
                labels(n) AS n_labels,
                properties(n) AS n_props,

                elementId(m) AS m_id,
                labels(m) AS m_labels,
                properties(m) AS m_props,

                elementId(r) AS r_id,
                type(r) AS r_type,
                properties(r) AS r_props
        """)

        nodes = {}
        edges = {}

        for record in result:
            nodes[record["n_id"]] = {
                "id": record["n_id"],
                "labels": record["n_labels"],
                **record["n_props"]
            }

            nodes[record["m_id"]] = {
                "id": record["m_id"],
                "labels": record["m_labels"],
                **record["m_props"]
            }

            edges[record["r_id"]] = {
                "id": record["r_id"],
                "source": record["n_id"],
                "target": record["m_id"],
                "type": record["r_type"],
                **record["r_props"]
            }

        return {
            "nodes": list(nodes.values()),
            "edges": list(edges.values())
        }


if __name__ == "__main__":
    print(get_all_nodes("id_8bhqfqn9yh"))
