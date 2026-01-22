from pymongo import MongoClient

import os
from pydantic import ValidationError
from typing import Optional, List
from api.mongo_models import AIMessage, AIModel, HumanMessage, Source, Project

from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_CLUSTER_URI')
if MONGO_URI is None:
    raise ValueError("MONGO_URI not declared in environment variables.")

mongo_client = MongoClient(MONGO_URI)

db = mongo_client.get_database('supply')
chat_collection = db['Chats']
project_collection = db['Projects']
desc_collection = db['Descriptions']
research_collection = db['ResearchResults']

from api.utils import generate_random_id

def create_project(userPk: int, name: str) -> str:
    projectId = generate_random_id(10)
    try:
        proj = Project(
            id=projectId,
            userPk=userPk,
            name=name
        )
    except ValidationError as v:
        print(" === Validation Error in Project === ")
        print(v)
        return
    
    try:
        project_collection.insert_one(proj.model_dump())
        return projectId
    except Exception as E:
        print(" === Exception while inserting project === ")
        print(E)

def get_projects(
    user_pk: int
) -> List[str]:
    returned_cursor = project_collection.find({
        "userPk": user_pk
    })
    result = []
    for item in returned_cursor:
        result.append(item.get('name'))

    return result

def get_project_id(
    user_pk: int,
    name: str
) -> str:
    returned_cursor = project_collection.find({
        "userPk": user_pk,
        "name": name
    })
    result = ""
    for item in returned_cursor:
        result = str(item.get('id'))

    return result

def insert_human_message(
    index: int,
    project_id: str,
    content: str,
    receiverAgent: AIModel,
    attached: List[Source] = []
) -> None:
    try:
        mes = HumanMessage(
            index=index,
            projectId=project_id,
            content=content,
            receiverAgent=receiverAgent,
            attached=attached
        )
    except ValidationError as v:
        print(" === Error while inserting human message === ")
        print(v)
        return
    
    try:
        chat_collection.insert_one(mes.model_dump(mode="json"))
    except Exception as E:
        print(" === EXCEPTION WHILE INSERTING HUMAN MESSAGE === ")
        raise E

def insert_model_message(
    index: int,
    senderModel: AIModel,
    project_id: str,
    content: str,
    sources: List[Source] = []
):
    try:
        mes = AIMessage(
            index=index,
            senderModel=senderModel,
            projectId=project_id,
            content=content,
            sources=sources
        )
    except ValidationError as v:
        print(" === Error while validating model message === ")
        print(v)
        return
    
    try:
        chat_collection.insert_one(mes.model_dump(mode="json"))
    except Exception as E:
        print(" === EXCEPTION WHILE INSERTING HUMAN MESSAGE === ")
        raise E

def insert_final_description(proj_id: str, description: str):
    desc_collection.insert_one({
        "projectId": proj_id,
        "description": description
    })

def get_all_messages(project_id: str):
    returned_cursor = chat_collection.find({
        "projectId": project_id
    })
    chats_list = []
    for item in returned_cursor:
        if 'receiverAgent' in item.keys():
            chats_list.append({
                "index": item['index'],
                "role": "user",
                "content": item['content']
            })
        else:
            chats_list.append({
                "index": item['index'],
                "role": "assistant",
                "content": item['content']
            })

    sorted_messages = sorted(chats_list, key=lambda x: x.get('index', 2000000))
    return sorted_messages

def get_researched_content(project_id):
    returned_cursor = research_collection.find({
        "projectId": project_id
    })

    results = []
    for item in returned_cursor:
        results.append({
            "id": item['elementId'],
            "result": item['researchResult']
        })

    return results

if __name__ == "__main__":
    print(insert_human_message(
        index=1,
        senderPK=1,
        content="alalalala",
        receiverAgent=AIModel.CHAT_AGENT
    ))