from redis_ops import wait_and_pop
from mongo import get_description
from cypher_agent import get_cypher_queries
from neo4j_ops import run_graphdb_query

while True:
    proj_id = wait_and_pop()
    print(f"Project ID: {proj_id}")
    proj_description = get_description(proj_id)
    cypher_queries = get_cypher_queries(proj_id, proj_description)
    print(cypher_queries)

    print("\n\n ==== Running Neo4j queries ==== ")
    run_graphdb_query(cypher_queries)

    break