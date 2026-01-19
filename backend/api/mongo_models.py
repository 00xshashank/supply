from enum import IntEnum
from pydantic import BaseModel
from typing import Optional, List

class AIModel(IntEnum):
    DESCRIPTION_AGENT = 0
    CYPHER_AGENT = 1
    RESEARCH_AGENT = 2
    CHAT_AGENT = 3

class Source(BaseModel):
    projectId: str
    title: str
    content: str
    url: str

class HumanMessage(BaseModel):
    projectId: str
    index: int
    senderPK: int
    content: str
    receiverAgent: AIModel
    attached: Optional[List[Source]] = []

class AIMessage(BaseModel):
    projectId: str
    index: int
    senderModel: AIModel
    content: str
    sources: Optional[List[Source]] = []

class Project(BaseModel):
    id: str
    userPk: int
    name: str

class FinalDescription(BaseModel):
    projectId: str
    description: str