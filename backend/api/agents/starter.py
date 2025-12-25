from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from google.genai.types import GenerateContentConfig, ThinkingConfig

import asyncio

from dotenv import load_dotenv
load_dotenv()

graph_extraction_instruction = """
You are an agent responsible for extracting the structural graphs of businesses.
You are given as input, the user describing their business's structure. 
Your job is to extract a graph containing all contents and relationships as part of their business, 
and gives a set of Cypher queries that describes this data. 
"""

graph_extractor_agent = LlmAgent(
    name="structural_graph_extractor_agent",
    model=LiteLlm("openrouter/deepseek/deepseek-r1-0528:free"),
    instruction=graph_extraction_instruction,
    # planner=BuiltInPlanner(),
    description="Extract graph structure from business description"
)

session_service = InMemorySessionService()
session = asyncio.run(session_service.create_session(
    app_name="SUPPLY",
    user_id="1234",
    session_id="11111"
))
runner = Runner(
    app_name="SUPPLY",
    agent=graph_extractor_agent,
    session_service=session_service
)

async def call_agent(query):
    content = types.Content(role="user", parts=[types.Part(query)])
    print(f" --- Running query --- ")
    final_response_text = "No final response captured."
    try:
        async for event in runner.run_async(
            user_id="1234",
            session_id="11111",
            new_message=content
        ):
            print(f"Event id: {event.id}, Event author: {event.author}")
            has_specific_part = False
            if event.content and event.content.parts:
                for part in event.content.parts:
                    print(part)

            if not has_specific_part and event.is_final_response():
                if (
                    event.content and
                    event.content.parts and
                    event.content.parts[0].text
                ):
                    final_response_text = event.content.parts[0].text

        print(f"Final response text is: {final_response_text}")

    except RuntimeError as E:
        print(f"Error during agent run: {E}")

async def main():
    await(call_agent("Good morning!"))
    # await(call_agent("Please give me a business idea and its graph."))

try:
    asyncio.run(main())
except RuntimeError as e:
    print("Error while calling main(): \n\n{e}")
