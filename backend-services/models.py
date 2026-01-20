from pydantic import BaseModel
from enum import IntEnum

class FinalDescription(BaseModel):
    projectId: str
    description: str

class Source(BaseModel):
    projectId: str
    title: str
    content: str
    url: str

class AIModel(IntEnum):
    DESCRIPTION_AGENT = 0
    CYPHER_AGENT = 1
    RESEARCH_AGENT = 2
    CHAT_AGENT = 3