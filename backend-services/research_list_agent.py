import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables.")

SYSTEM_PROMPT = f"""
You are a supply chain research analyst specializing in stability, sustainability, and alternative sourcing strategies. You will be given a business description and a set of Cypher queries representing the supply chain knowledge graph.

Your task is to generate a comprehensive list of research topics that assess supply chain stability, sustainability, and alternatives. Each research topic must be mapped to specific nodes and edges from the Cypher queries.

Output Format:
For line of Cypher used to create the graph, generate relevant research topics in the following JSON structure:

{{
  "nodeId": "NodeLabel:nodeName",
  "edgeId": "SourceNode-[RELATIONSHIP_TYPE]->TargetNode",
  "researchTopics": [
    "Research topic 1",
    "Research topic 2"
  ]
}}

Research Topic Categories:
1. Stability: Supply disruption risks, geopolitical risks, single points of failure, backup capacity, contract terms, lead times, quality consistency
2. Sustainability: Environmental impact, carbon footprint, waste management, certifications (FSC, ISO), ethical sourcing, circular economy practices, emissions
3. Alternatives: Alternative suppliers, substitute materials, diversification opportunities, nearshoring/reshoring options, emerging technologies

Rules:
- Output ONLY valid JSON array
- Do NOT include explanations
- Do NOT wrap output in markdown
- Do NOT include comments
- Generate 2-5 research topics per node/edge depending on criticality
- Focus on actionable, specific research questions
- Cover all three categories (stability, sustainability, alternatives) where applicable
- Map research to the exact node/edge identifiers from the Cypher queries
- For Supplier nodes: research alternative suppliers, risk profiles, certifications
- For Material nodes: research substitutes, environmental impact, sourcing alternatives
- For LogisticsProvider edges: research route alternatives, carbon emissions, reliability metrics
- For Factory nodes: research capacity constraints, energy sources, compliance
- For Market/Customer edges: research demand volatility, geographic expansion, channel alternatives
- Prioritize critical supply chain components (raw materials, tier-1 suppliers, single-source dependencies)
- Make sure your queries list has a 1:1 correspondence with the Cypher queries list passed to you in terms of nodes and edges.
"""

llm = ChatGroq(
	model="openai/gpt-oss-120b",
	api_key=GROQ_API_KEY
)

def get_research_list(proj_id: str, description: str, cypher_queries: str) -> str:
    research_content = llm.invoke([
        SystemMessage(SYSTEM_PROMPT),
        HumanMessage(f"""Business Description: {description}\nProject Id: {proj_id}\nCypher queries: {cypher_queries}""")
    ])

    response_str = research_content.content
    response_json = json.loads(response_str)

    return response_json

BUSINESS_DESCRIPTION = """
Business Description:
Company: A mid-sized toy and puzzle manufacturing business
Headquarters: Not specified

Core Activities:
Manufacturing: Operates a primary factory.
The factory manufactures: Toys, puzzles (wooden).
Factories require: Hardwood (teak, rubberwood), Engineered wood (plywood), Eco-friendly paints, Cost-effective pigments.

Suppliers:
**Wood Suppliers:**
- Hardwood (Teak and Rubberwood):
  - Suppliers: Regional suppliers; Location: India; Used for: Durable toy components.
- Engineered Wood (Plywood):
  - Suppliers: Vendors; Location: Indonesia; Used for: Structural puzzle boards and toy bases.

**Paint & Coating Suppliers:**
- Eco-Friendly Paints:
  - Suppliers: Imported from Germany; Used for: Safety-compliant, non-toxic finishes.
- Cost-Effective Pigments:
  - Suppliers: Suppliers; Location: India; Used for: Economical production runs.

Logistics:
Domestic transport: Uses partners like Blue Dart for Factory → Warehouse transfers.
International shipments: Uses global freight providers (e.g., DHL Global Forwarding) for bulk/international movements.
Warehouses: One or more (locations not specified).

Sales:
Products distributed to: Retailers, Distributors.

Known Uncertainties or Evolving Areas:
- Retail mix, geographic reach, and downstream sales channels are not finalized.
- Reverse logistics (returns) strategy undefined.
- Approach for seasonal demand spikes unestablished.
- Long-term supplier contracts undecided.
"""

CYPHER_QUERIES_LIST = """
MERGE (c:Company:Project_aaaaaaaaaaa {name: 'ToyCo', location: 'CountryX', projectId: 'aaaaaaaaaaa'})
MERGE (f:Factory:Project_aaaaaaaaaaa {name: 'Main Toy Manufacturing Facility', location: 'CityY', projectId: 'aaaaaaaaaaa'})
MERGE (c)-[:OWNS {projectId: 'aaaaaaaaaaa'}]->(f)
MERGE (p1:Product:Project_aaaaaaaaaaa {name: 'Educational Toy', category: 'Educational', material: 'Plastic/Wood', projectId: 'aaaaaaaaaaa'})
MERGE (p2:Product:Project_aaaaaaaaaaa {name: 'Mechanical Playset', category: 'Mechanical', material: 'Metal/Wood', projectId: 'aaaaaaaaaaa'})
MERGE (p3:Product:Project_aaaaaaaaaaa {name: 'Simple Plastic Toy', category: 'Plastic', material: 'Plastic', projectId: 'aaaaaaaaaaa'})
MERGE (f)-[:PRODUCES {projectId: 'aaaaaaaaaaa'}]->(p1)
MERGE (f)-[:PRODUCES {projectId: 'aaaaaaaaaaa'}]->(p2)
MERGE (f)-[:PRODUCES {projectId: 'aaaaaaaaaaa'}]->(p3)
MERGE (m1:Material:Project_aaaaaaaaaaa {type: 'Plastic Resin', subtype: 'ABS', projectId: 'aaaaaaaaaaa'})
MERGE (m2:Material:Project_aaaaaaaaaaa {type: 'Plastic Resin', subtype: 'Polypropylene', projectId: 'aaaaaaaaaaa'})
MERGE (m3:Material:Project_aaaaaaaaaaa {type: 'Wood', subtype: 'Rubberwood', projectId: 'aaaaaaaaaaa'})
MERGE (m4:Material:Project_aaaaaaaaaaa {type: 'Wood', subtype: 'Plywood', projectId: 'aaaaaaaaaaa'})
MERGE (m5:Material:Project_aaaaaaaaaaa {type: 'Metal Component', subtype: 'Screws', projectId: 'aaaaaaaaaaa'})
MERGE (m6:Material:Project_aaaaaaaaaaa {type: 'Metal Component', subtype: 'Springs', projectId: 'aaaaaaaaaaa'})
MERGE (m7:Material:Project_aaaaaaaaaaa {type: 'Paint', subtype: 'Non-toxic', projectId: 'aaaaaaaaaaa'})
MERGE (m8:Material:Project_aaaaaaaaaaa {type: 'Packaging', subtype: 'Printed Box', projectId: 'aaaaaaaaaaa'})
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m1)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m2)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m3)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m4)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m5)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m6)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m7)
MERGE (f)-[:USES_MATERIAL {projectId: 'aaaaaaaaaaa'}]->(m8)
MERGE (s1:Supplier:Project_aaaaaaaaaaa {name: 'Regional Petrochemical Supplier', country: 'CountryX', materialType: 'Plastic Resin', projectId: 'aaaaaaaaaaa'})
MERGE (s2:Supplier:Project_aaaaaaaaaaa {name: 'Domestic Wood Supplier', country: 'CountryX', materialType: 'Wood', projectId: 'aaaaaaaaaaa'})
MERGE (s3:Supplier:Project_aaaaaaaaaaa {name: 'Local Hardware Manufacturer', country: 'CountryX', materialType: 'Metal Component', projectId: 'aaaaaaaaaaa'})
MERGE (s4:Supplier:Project_aaaaaaaaaaa {name: 'Certified Paint Supplier', country: 'CountryX', materialType: 'Paint', projectId: 'aaaaaaaaaaa'})
MERGE (s5:Supplier:Project_aaaaaaaaaaa {name: 'Domestic Packaging Manufacturer', country: 'CountryX', materialType: 'Packaging', projectId: 'aaaaaaaaaaa'})
MERGE (s6:Supplier:Project_aaaaaaaaaaa {name: 'International Electronics Supplier', country: 'CountryZ', materialType: 'Electronic Module', projectId: 'aaaaaaaaaaa'})
MERGE (s1)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m1)
MERGE (s1)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m2)
MERGE (s2)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m3)
MERGE (s2)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m4)
MERGE (s3)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m5)
MERGE (s3)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m6)
MERGE (s4)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m7)
MERGE (s5)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m8)
MERGE (s6)-[:SUPPLIES {projectId: 'aaaaaaaaaaa'}]->(m9:Material:Project_aaaaaaaaaaa {type: 'Electronic Module', projectId: 'aaaaaaaaaaa'})
MERGE (f)-[:RECEIVES_FROM {projectId: 'aaaaaaaaaaa'}]->(s1)
MERGE (f)-[:RECEIVES_FROM {projectId: 'aaaaaaaaaaa'}]->(s2)
MERGE (f)-[:RECEIVES_FROM {projectId: 'aaaaaaaaaaa'}]->(s3)
MERGE (f)-[:RECEIVES_FROM {projectId: 'aaaaaaaaaaa'}]->(s4)
MERGE (f)-[:RECEIVES_FROM {projectId: 'aaaaaaaaaaa'}]->(s5)
MERGE (f)-[:RECEIVES_FROM {projectId: 'aaaaaaaaaaa'}]->(s6)
MERGE (lp1:LogisticsProvider:Project_aaaaaaaaaaa {name: 'Regional Transport Co.', type: 'Inbound', projectId: 'aaaaaaaaaaa'})
MERGE (lp2:LogisticsProvider:Project_aaaaaaaaaaa {name: 'Domestic Freight Partner', type: 'Outbound', projectId: 'aaaaaaaaaaa'})
MERGE (lp3:LogisticsProvider:Project_aaaaaaaaaaa {name: 'Last-Mile Courier', type: 'LastMile', projectId: 'aaaaaaaaaaa'})
MERGE (lp4:LogisticsProvider:Project_aaaaaaaaaaa {name: 'International Freight Forwarder', type: 'Export', projectId: 'aaaaaaaaaaa'})
MERGE (f)-[:USES_LOGISTICS {direction: 'Inbound', projectId: 'aaaaaaaaaaa'}]->(lp1)
MERGE (f)-[:USES_LOGISTICS {direction: 'Outbound', projectId: 'aaaaaaaaaaa'}]->(lp2)
MERGE (lp2)-[:DELIVERS_TO {projectId: 'aaaaaaaaaaa'}]->(w:Warehouse:Project_aaaaaaaaaaa {name: 'Central Distribution Warehouse', location: 'CityZ', projectId: 'aaaaaaaaaaa'})
MERGE (lp3)-[:DELIVERS_TO {projectId: 'aaaaaaaaaaa'}]->(w)
MERGE (lp4)-[:HANDLES_EXPORT {projectId: 'aaaaaaaaaaa'}]->(w)
MERGE (w)-[:STORES {projectId: 'aaaaaaaaaaa'}]->(p1)
MERGE (w)-[:STORES {projectId: 'aaaaaaaaaaa'}]->(p2)
MERGE (w)-[:STORES {projectId: 'aaaaaaaaaaa'}]->(p3)
MERGE (mkt1:Market:Project_aaaaaaaaaaa {name: 'Brick-and-Mortar Toy Stores', channel: 'Retail', projectId: 'aaaaaaaaaaa'})
MERGE (mkt2:Market:Project_aaaaaaaaaaa {name: 'Educational Retailers', channel: 'Retail', projectId: 'aaaaaaaaaaa'})
MERGE (mkt3:Market:Project_aaaaaaaaaaa {name: 'Online Marketplace', channel: 'E-commerce', projectId: 'aaaaaaaaaaa'})
MERGE (mkt4:Market:Project_aaaaaaaaaaa {name: 'Direct-to-Consumer Website', channel: 'Direct', projectId: 'aaaaaaaaaaa'})
MERGE (c)-[:SELLS_VIA {projectId: 'aaaaaaaaaaa'}]->(mkt1)
MERGE (c)-[:SELLS_VIA {projectId: 'aaaaaaaaaaa'}]->(mkt2)
MERGE (c)-[:SELLS_VIA {projectId: 'aaaaaaaaaaa'}]->(mkt3)
MERGE (c)-[:SELLS_VIA {projectId: 'aaaaaaaaaaa'}]->(mkt4)
MERGE (cust1:Customer:Project_aaaaaaaaaaa {type: 'Retail Chain', name: 'National Toy Chain', projectId: 'aaaaaaaaaaa'})
MERGE (cust2:Customer:Project_aaaaaaaaaaa {type: 'Independent Retailer', name: 'Local Toy Shop', projectId: 'aaaaaaaaaaa'})
MERGE (cust3:Customer:Project_aaaaaaaaaaa {type: 'Online Consumer', name: 'Individual Buyer', projectId: 'aaaaaaaaaaa'})
MERGE (mkt1)-[:SERVES {projectId: 'aaaaaaaaaaa'}]->(cust1)
MERGE (mkt2)-[:SERVES {projectId: 'aaaaaaaaaaa'}]->(cust2)
MERGE (mkt3)-[:SERVES {projectId: 'aaaaaaaaaaa'}]->(cust3)
MERGE (mkt4)-[:SERVES {projectId: 'aaaaaaaaaaa'}]->(cust3)
"""

if __name__ == "__main__":
    response = get_research_list("aaaaaaaaaaa", BUSINESS_DESCRIPTION, CYPHER_QUERIES_LIST)
    print(response)