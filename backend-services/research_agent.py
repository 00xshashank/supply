import os
from dotenv import load_dotenv
import json

from langchain_groq import ChatGroq
from langchain.agents import create_agent

from tavily import TavilyClient

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables.")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not set in environment variables.")

SYSTEM_PROMPT = """
You are a supply chain research specialist. You will be given a Neo4j node related to a supply chain node or edge, along with context about the business and supply chain component.
Your task is to provide actionable findings.

Input Format:
- nodeId or edgeId: The supply chain component being researched
- researchTopic: A specific research question focused on stability, sustainability, or alternatives
- businessContext: Background information about the company and supply chain

Your research must:
1. Provide specific data, metrics, and examples
2. Identify risks and opportunities
3. Recommend concrete actions

Output Format (JSON):
{
  "findings": "Detailed research findings with specific data and insights",
  "keyMetrics": [
    {
      "metric": "Metric name",
      "value": "Metric value with units",
      "context": "Why this metric matters"
    }
  ],
  "risks": [
    {
      "risk": "Identified risk",
      "severity": "High/Medium/Low",
      "mitigation": "Suggested mitigation strategy"
    }
  ],
  "recommendations": [
    {
      "action": "Specific recommended action",
      "priority": "High/Medium/Low",
      "timeframe": "Immediate/Short-term/Long-term",
      "rationale": "Why this action is recommended"
    }
  ],
  "confidence": "High/Medium/Low",
  "lastUpdated": "ISO 8601 timestamp"
}

Quality Standards:
- Be specific: replace vague terms with concrete numbers, names, locations

Rules:
- Output ONLY valid JSON
- Do NOT include explanations outside the JSON structure
- If information is not available, state this explicitly in findings
"""

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class ResearcherAgent:
	def __init__(self):
		self.system_prompt = SYSTEM_PROMPT
		self.search_calls = 0
		self.llm = ChatGroq(
			model="openai/gpt-oss-120b",
			reasoning_effort='medium',
			api_key=GROQ_API_KEY
		)
		self.research_agent = create_agent(
			model=self.llm,
			system_prompt=SYSTEM_PROMPT,
			tools=[
				# self.web_search
			]
		)

	def web_search(self, query="", *args):
		"""Returns web search results for query passed as argument. CAN BE INVOKED A MAXIMUM OF 3 TIMES PER PROMPT, SO USE YOUR QUERIES WISELY"""
		if not isinstance(query, str):
			return "Error: query must be a string"
		if query == "":
			return "Sorry, wrong arguments, you just wasted a turn"
		if self.search_calls>2:
			return """Max limit exceeded"""

		search_result = tavily_client.search(query)
		print(" === AGENT CALLED SEARCH TOOL === ")
		print(f"Query: {query}\n")
		print(f"Responses: {search_result}")
		self.search_calls += 1
		return search_result
    
	def call(self, proj_description, query):
		self.search_calls = 0
		research_content = self.research_agent.invoke({
			"messages": [
				{"role": "user", "content": f"Context:{proj_description}\nQueryNode:{query}"}
			]
		})

		print(" === Raw Response === ")
		print(research_content)

		# Extract the final message content from the agent
		messages = research_content.get('messages', [])
		if not messages:
			return {"error": "No response from agent"}

		# Get the last message (should be the assistant's response)
		final_message = messages[-1]

		# Extract content from the message
		if hasattr(final_message, 'content'):
			content = final_message.content
		elif isinstance(final_message, dict):
			content = final_message.get('content', '')
		else:
			content = str(final_message)

		print(" === Extracted Content === ")
		print(content)

		# Try to extract JSON from the content
		try:
			# Remove markdown code blocks if present
			clean_content = content.strip()
			if clean_content.startswith('```'):
				# Remove opening ```json or ```
				clean_content = clean_content.split('\n', 1)[1] if '\n' in clean_content else clean_content[3:]
				# Remove closing ```
				if clean_content.endswith('```'):
					clean_content = clean_content.rsplit('```', 1)[0]
			
			# Try to find JSON object in the content
			start_idx = clean_content.find('{')
			end_idx = clean_content.rfind('}')
			
			if start_idx != -1 and end_idx != -1:
				json_str = clean_content[start_idx:end_idx + 1]
				parsed_json = json.loads(json_str)
				return parsed_json
			else:
				# If no curly braces found, try parsing the whole thing
				parsed_json = json.loads(clean_content)
				return parsed_json
				
		except json.JSONDecodeError as e:
			print(f" === JSON Parse Error === ")
			print(f"Error: {e}")
			print(f"Attempted to parse: {clean_content[:500]}...")
			return {
				"error": "Failed to parse JSON from agent response",
				"raw_content": content,
				"parse_error": str(e)
			}
		except Exception as e:
			print(f" === Unexpected Error === ")
			print(f"Error: {e}")
			return {
				"error": "Unexpected error parsing response",
				"raw_content": content,
				"exception": str(e)
			}

if __name__ == "__main__":
    query = """
    {
      "nodeId": "Material:Springs",
      "edgeId": null,
      "researchTopics": [
        "Stability: Map lead‑time variability for spring components during peak production periods.",
        "Sustainability: Assess the environmental impact of spring steel manufacturing processes.",
        "Alternatives: Explore spring‑less design concepts or use of recycled spring steel."
      ]
    }
    """
    agent = ResearcherAgent()
    final_res = agent.call(query)
    print(" === Final Response === ")
    print(final_res)
