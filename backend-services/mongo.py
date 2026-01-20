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

def get_description(projId: str):
    description = desc_collection.find_one({
        "projectId": projId
    })
    return description['description']

if __name__=="__main__":
    print(get_description('aaaaaaaaaaa'))