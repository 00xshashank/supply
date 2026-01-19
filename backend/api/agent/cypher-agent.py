import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in environment variables.")

SYSTEM_PROMPT = f"""
You are a graph data engineer specializing in Neo4j.

You will be given a structured business description.
Your task is to generate executable Cypher queries that:
- Create nodes for all entities (Company, Factory, Supplier, Material, LogisticsProvider, Warehouse, Product, Market, etc.)
- Create relationships that accurately represent the business structure
- Use MERGE instead of CREATE where appropriate
- Use clear labels and relationship types
- Include relevant properties (name, location, role, material type, etc.)
- Assume the database is empty
- Produce Cypher that can be executed directly in Neo4j Browser or via a driver

Rules:
- Output ONLY Cypher queries
- Do NOT explain anything
- Do NOT wrap output in markdown
- Do NOT include comments
- Do NOT ask questions
"""

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

llm = ChatOpenAI(
    model="nex-agi/deepseek-v3.1-nex-n1:free",
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

response = llm.invoke([
    SystemMessage(SYSTEM_PROMPT),
    HumanMessage(BUSINESS_DESCRIPTION)
])

print(response.content)