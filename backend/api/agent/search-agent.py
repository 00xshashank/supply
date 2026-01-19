import asyncio
import os
import requests
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

load_dotenv()

TAVILY_API_KEY = "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"

SYSTEM_PROMPT = """
You are a supply-chain compliance analyst.

You will be given:
- A logistics route (origin, destination, carrier)
- Web search results related to this route

Your task:
- Assess whether the route appears SAFE and COMPLIANT
- Consider sanctions, trade restrictions, logistics risks, regulatory issues, and geopolitical factors

Output format (strict):
Status: SAFE | RISKY | NON-COMPLIANT
Reasoning: Short, factual justification based only on provided search results

Do not speculate.
"""

def tavily_search(query: str):
    response = requests.post(
        "https://api.tavily.com/search",
        headers={
            "Authorization": f"Bearer {TAVILY_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "query": query,
            "max_results": 5,
            "search_depth": "basic"
        }
    )
    response.raise_for_status()
    return response.json()["results"]

ROUTE_INPUT = {
    "from": "India",
    "to": "France",
    "by": "DHL Global Forwarding"
}

search_query = (
    f"Shipping route compliance risks {ROUTE_INPUT['from']} to "
    f"{ROUTE_INPUT['to']} via {ROUTE_INPUT['by']} sanctions regulations"
)

search_results = tavily_search(search_query)

search_blob = "\n\n".join(
    f"Title: {r.get('title')}\nContent: {r.get('content')}"
    for r in search_results
)

USER_PROMPT = f"""
Route:
From: {ROUTE_INPUT['from']}
To: {ROUTE_INPUT['to']}
Carrier: {ROUTE_INPUT['by']}

Search Results:
{search_blob}
"""

agent = LlmAgent(
    name="route_compliance_agent",
    model=LiteLlm("openrouter/deepseek/deepseek-r1-0528:free"),
    instruction=SYSTEM_PROMPT,
    description="Evaluates logistics route safety and compliance using web context."
)

session_service = InMemorySessionService()
session = asyncio.run(
    session_service.create_session(
        app_name="SUPPLY",
        user_id="1234",
        session_id="33333"
    )
)

runner = Runner(
    app_name="SUPPLY",
    agent=agent,
    session_service=session_service
)

async def run():
    content = types.Content(
        role="user",
        parts=[types.Part(text=USER_PROMPT)]
    )

    for event in runner.run(
        user_id="1234",
        session_id="33333",
        new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                print(part.text)

if __name__ == "__main__":
    asyncio.run(run())
