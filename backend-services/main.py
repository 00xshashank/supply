import json
import time

from redis_ops import wait_and_pop, set_status, redisClient
from mongo import get_description, store_cypher_queries, store_research_results
from cypher_agent import get_cypher_queries
from neo4j_ops import run_graphdb_query, get_all_nodes
from research_list_agent import get_research_list
from research_agent import ResearcherAgent

researcher_agent = ResearcherAgent()
# redisClient.lpush("task_queue", "8bhqfqn9yh")

while True:
    proj_id = wait_and_pop()
    print(f"Project ID: {proj_id}")
    set_status(proj_id, 'Queued')
    proj_description = get_description(proj_id)
    cypher_queries = get_cypher_queries(proj_id, proj_description)
    print(cypher_queries)

    print("Storing Cypher queries...")
    store_cypher_queries(proj_id=proj_id, queries=cypher_queries)
    print("Done.")

    set_status(proj_id, 'Creating graph')
    print("Running Cypher queries...")
    run_graphdb_query(cypher_queries)
    print("Done.")

    set_status(proj_id, 'Preparing for research')
    # print("Getting research list...")
    # research_list = get_research_list(proj_id, proj_description, cypher_queries)
    # print(f" === Research List === \n{research_list}\n\n")

    research_list = get_all_nodes(proj_id)
    
    set_status(proj_id, 'Researching')
    print("Now researching individual components...")
    for i, obj in enumerate(research_list):
        print(" === Now researching: === ")
        print(obj)
        print(" ==== ")
        research_response = researcher_agent.call(proj_description, str(obj))
        store_research_results(i, proj_id, obj.element_id, str(research_response))
        print("Waiting fro 60 seconds\n...")
        time.sleep(60)

    break