from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool

from typing import List, Dict

import os

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in env variables")

SYSTEM_PROMPT = """
You are an expert business analyst.

You will be given a description of a company's operations.
Your task is to produce a detailed, structured business description covering (non-exhaustive):
- Company overview
- Manufacturing and operations
- Suppliers (materials, locations, purpose)
- Logistics and warehousing
- Sales and distribution
- Known uncertainties or evolving areas

Write clearly and comprehensively.
Ask questions whenever necessary. Do not commit without being absolutely sure of what the user wants.
Be sure to extract as much detail as possible, like shipping routes, company names etc.

**Example Complete Output**
Artisan Snacks Co. operates a small-scale specialty food manufacturing business focused on the production of packaged artisanal snack products. 
The business is centered around a single Primary Processing Facility, which handles ingredient preparation, cooking, seasoning, and packaging for all product lines. 
The company owns and manages this factory directly, using it as the operational core of its supply chain.

Raw agricultural inputs are sourced from a mix of domestic and international suppliers. 
Core staple ingredients such as grains and lentils are supplied by Local Grain Farmers, a network of domestic agricultural producers that provide food-grade wheat, lentils, and chickpeas. 
These supplies are subject to seasonal variability and are typically governed by short-term or flexible purchasing agreements. 
Complementary ingredients, including spices, are procured from Regional Spice Wholesalers, also based domestically, ensuring consistent availability for standard product formulations.

For premium product lines, the company relies on international specialty suppliers. 
Mediterranean Olive Oil Exporter, based in Southern Europe, supplies cold-pressed olive oil used in higher-end snack variants, 
while Middle Eastern Seasoning Supplier provides specialty seasoning blends that differentiate select offerings. 
These international suppliers ship ingredients through consolidated freight channels to the factory, often coordinated by third-party logistics providers handling customs clearance and inbound international transport.

Packaging materials are sourced domestically from Eco Packaging Ltd., which supplies biodegradable pouches and cardboard cartons aligned with the company’s sustainability objectives. 
These materials are delivered directly to the Primary Processing Facility and integrated into the final packaging stage.

Finished goods are transported from the Primary Processing Facility to the Central Distribution Hub, a warehouse owned by Artisan Snacks Co. 
This factory-to-warehouse movement is handled by Local Trucking Operators, who provide domestic freight services for palletized shipments on a regular schedule.

From the Central Distribution Hub, products are distributed onward through multiple outbound channels. 
Deliveries to brick-and-mortar outlets—such as Small Grocery Stores and Specialty Food Retailers—are managed by Regional Courier Services, which handle last-mile distribution across the domestic market. 
For direct-to-consumer orders placed through the company’s emerging online sales channel, as well as for limited export shipments, fulfillment is handled by a Third-Party Logistics Provider that manages order consolidation, international shipping, and customs documentation.

Demand forecasting for seasonal spikes—particularly during festivals and holiday periods—is still being refined, and long-term supplier contracts with both agricultural producers and international ingredient suppliers are under consideration but not yet in place.
**End of Example Output**

When you are done with your analysis and positive that your output comprehensively captures the user's description, please ask the user for confirmation once before committing to your final response.
You are given access to a tool: set_final_description. Call the tool with the final description inferred by you and the project id as inputs if you are sure.
The tool does not return anything. After calling the tool, you final text must end with the literal string, "THE END" to end the conversation. 
"""

USER_INPUT = """
Company Overview:
The company operates a small-to-medium-scale toy manufacturing business focused on the design and production of educational and play-oriented toys for children. Manufacturing activities are centralized at a single production facility, with an emphasis on safety compliance, cost efficiency, and scalable product lines.

Core Activities:
Design & Manufacturing:
Operates one primary toy manufacturing facility responsible for:
Product design finalization
Molding, assembly, finishing, and packaging
Quality assurance and safety testing
Produces a range of toys including:
Plastic toys
Wooden toys
Simple mechanical and educational playsets

Production processes combine automated machinery with manual assembly for quality-sensitive components.
Raw Material Sourcing:
Primary Materials:
Plastic resins (e.g., ABS, polypropylene) sourced from regional petrochemical suppliers within the same country.
Wood materials (e.g., rubberwood, plywood) sourced from domestic and nearby regional suppliers.
Metal components (screws, springs, fasteners) sourced from local hardware manufacturers.

Finishing & Safety Materials:
Non-toxic paints, dyes, and coatings sourced from certified suppliers to meet child safety standards.
Packaging materials such as printed boxes, inserts, and protective wraps sourced from domestic packaging manufacturers.

Supplier Network:
Majority of suppliers are located domestically to reduce lead times and ensure supply stability.
Select specialty components (e.g., electronic modules for interactive toys or specialty finishes) are imported from international suppliers.

Logistics & Distribution:
Inbound Logistics:
Raw materials and components are delivered to the manufacturing facility using regional transport and freight operators.

Outbound Logistics:
Finished toys are transported from the factory to one or more distribution warehouses using domestic logistics partners.
Regional deliveries to retailers are handled by last-mile logistics and courier services.
For international sales and bulk orders:
Third-party logistics providers manage freight forwarding, export documentation, and customs clearance.

Warehousing:
Central warehouses store finished goods and buffer inventory to support seasonal demand spikes.
Warehouses support order consolidation and distribution to multiple sales channels.

Sales & Distribution Channels:
Products are sold through:
Brick-and-mortar toy stores
Educational retailers
Online marketplaces
Direct-to-consumer (DTC) channels via the company’s website
Sales are concentrated in domestic markets, with limited but growing international reach.

Customers:
Primary customers include:
Retail chains
Independent toy retailers
Online consumers (aggregated, not individual profiles)

Compliance & Quality:
Products are designed to comply with:
National toy safety regulations
International standards (e.g., EN 71, ASTM F963 where applicable)
Regular quality inspections and batch testing are conducted at the factory level.

Operational Uncertainties & Evolving Areas:
Long-term sourcing agreements with raw material suppliers are still being negotiated.
Reverse logistics processes for defective or returned toys are not fully standardized.
Demand forecasting for peak seasons (festivals, holidays) is under continuous refinement.
Expansion of international distribution channels remains under evaluation.
"""

from api.mongo import insert_human_message, insert_model_message, insert_final_description
from api.mongo_models import AIModel

from api.redis_ops import queue_task

completed = False

class DescriptionAgentCaller:
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT
        self.llm = ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=GROQ_API_KEY
        )
        self.agent = create_agent(
            model=self.llm,
            tools=[
                self.set_final_description
            ]
        )

    @tool
    def set_final_description(proj_id, final_description: str) -> bool:
        """Use this tool to set the final business description of the user.
        Input: final_description: string: The final description as interpreted from the user's input
        """
        print("=== TOOL CALL ===")
        print(f"Project id: {proj_id}")
        insert_final_description(proj_id=proj_id, description=final_description)
        queue_task(proj_id)
        completed = True

    def call(self, message: str, project_id: str, message_history: List[Dict] = []):
        project_id = project_id
        completed = False
        insert_human_message(
            index=len(message_history),
            project_id=project_id,
            content=message,
            receiverAgent=AIModel.DESCRIPTION_AGENT
        )
        print(f" === USER MESSAGE === \n{message}")
        print(f" === MESSAGE HISTORY === \n{message_history}")
        agent_response = self.agent.invoke(
            {"messages": [{"role": "system", "content": f"{self.system_prompt}\nProject id: {project_id}"}] + message_history + [{"role": "system", "content": self.system_prompt}]}
        )
        print(f"===== Response ===== \nf{agent_response}")
        insert_model_message(
            index=len(message_history)+1,
            senderModel=AIModel.DESCRIPTION_AGENT,
            project_id=project_id,
            content=agent_response['messages'][-1].content
        )
        if completed == True:
            return "completed"
        return agent_response['messages'][-1].content


# if __name__ == "__main__":
#     while True:
#         user_response = input(">>> ")
#         if user_response == "exit":
#             break
#         conversation_history.append({"role": "user", "content": user_response})
#         response = description_agent.invoke({"messages": conversation_history})
#         print(response['messages'][-1].content)
#         conversation_history.append({"role": "assistant", "content": response['messages'][-1].content})