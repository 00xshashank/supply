from pymongo import MongoClient

import os
from pydantic import ValidationError
from typing import Optional, List
from api.mongo_models import AIMessage, AIModel, HumanMessage, Source, FinalDescription, Project

from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_CLUSTER_URI')
if MONGO_URI is None:
    raise ValueError("MONGO_URI not declared in environment variables.")

mongo_client = MongoClient(MONGO_URI)

db = mongo_client.get_database('supply')
chat_collection = db['Chats']
project_collection = db['Projects']

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
    
    try:
        project_collection.insert_one(proj.model_dump())
        return projectId
    except Exception as E:
        print(" === Exception while inserting project === ")
        print(E)


def insert_human_message(
    index: int,
    senderPK: int,
    content: str,
    receiverAgent: AIModel,
    attached: List[Source] = []
) -> None:
    try:
        mes = HumanMessage(
            index=index,
            senderPK=senderPK,
            content=content,
            receiverAgent=receiverAgent,
            attached=attached
        )
    except ValidationError as v:
        print(" === Error while inserting human message === ")
        print(v)
    
    try:
        chat_collection.insert_one(mes.model_dump(mode="json"))
    except Exception as E:
        print(" === EXCEPTION WHILE INSERTING HUMAN MESSAGE === ")
        raise E

def insert_model_message(
    index: int,
    senderModel: AIModel,
    receiverUser: int,
    content: str,
    sources: List[Source] = []
):
    try:
        mes = AIMessage(
            index=index,
            senderModel=senderModel,
            receiverUser=receiverUser,
            content=content,
            sources=sources
        )
    except ValidationError as v:
        return v
    
    try:
        chat_collection.insert_one(mes.model_dump(mode="json"))
    except Exception as E:
        print(" === EXCEPTION WHILE INSERTING HUMAN MESSAGE === ")
        raise E

def insert_final_description():
    pass

def get_all_messages():
    pass

if __name__ == "__main__":
    print(insert_human_message(
        index=1,
        senderPK=1,
        content="alalalala",
        receiverAgent=AIModel.CHAT_AGENT
    ))