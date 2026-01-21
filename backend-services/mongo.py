import os
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_CLUSTER_URI')
if MONGO_URI is None:
    raise ValueError("MONGO_URI not declared in environment variables.")

mongo_client = MongoClient(MONGO_URI)

db = mongo_client.get_database('supply')
desc_collection = db['Descriptions']
cypher_collection = db['Cypher_Queries']
research_collection = db['ResearchResults']

def get_description(projId: str):
    description = desc_collection.find_one({
        "projectId": projId
    })
    return description['description']

def store_cypher_queries(proj_id: str, queries: str):
    cypher_collection.insert_one({
        "projectId": proj_id,
        "queries": [q for q in queries.split('\n') if len(q)>0]
    })

def store_research_results(i: int, proj_id: str, query: str, research_result: str):
    research_collection.insert_one({
        "index": i,
        "projectId": proj_id,
        "queryNode": query,
        "researchResult": research_result
    })

if __name__=="__main__":
    print(get_description('aaaaaaaaaaa'))