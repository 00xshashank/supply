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
You are a supply chain research specialist. You will be given a specific research topic related to a supply chain node or edge, along with context about the business and supply chain component.
Your task is to conduct thorough research and provide actionable findings.

Input Format:
- nodeId or edgeId: The supply chain component being researched
- researchTopic: A specific research question focused on stability, sustainability, or alternatives
- businessContext: Background information about the company and supply chain

Your research must:
1. Use web search to find current, credible sources
2. Provide specific data, metrics, and examples
3. Include source citations
4. Identify risks and opportunities
5. Recommend concrete actions

Output Format (JSON):
{
  "researchTopic": "Original research question",
  "componentId": "nodeId or edgeId",
  "findings": "Detailed research findings with specific data and insights",
  "sources": [
    {
      "title": "Source title",
      "url": "Source URL",
      "relevantData": "Key data point or quote from source"
    }
  ],
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
  "opportunities": [
    {
      "opportunity": "Identified opportunity",
      "impact": "Potential impact description",
      "implementation": "How to pursue this opportunity"
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

Research Guidelines:
- For Stability topics: Focus on supply disruption probability, lead times, geopolitical factors, financial health of suppliers, contract terms, backup options
- For Sustainability topics: Search for certifications, carbon footprint data, environmental regulations, industry benchmarks, lifecycle assessments
- For Alternatives topics: Identify viable alternatives if available with comparative analysis on cost, availability, performance, sustainability

Quality Standards:
- Cite sources from the last 2 years when possible
- Prioritize industry reports, government data, certification bodies, peer-reviewed sources
- Include quantitative data wherever available
- Flag information gaps or areas requiring deeper investigation
- Be specific: replace vague terms with concrete numbers, names, locations

Rules:
- Output ONLY valid JSON
- Do NOT include markdown formatting
- Do NOT include explanations outside the JSON structure
- Do NOT fabricate data or sources
- Use web_search tool for all factual claims
- If information is not available, state this explicitly in findings
- PLEASE USE THE web_search TOOL 3 TIMES ONLY PER QUERY PRESENTED BY THE USER.
"""

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class ResearcherAgent:
	def __init__(self):
		self.system_prompt = SYSTEM_PROMPT
		self.search_calls = 0
		self.llm = ChatGroq(
			model="openai/gpt-oss-120b",
			api_key=GROQ_API_KEY
		)
		self.research_agent = create_agent(
			model=self.llm,
			system_prompt=SYSTEM_PROMPT,
			tools=[
				self.web_search
			]
		)

	def web_search(self, query):
		"""Returns web search results for query passed as argument. CAN BE INVOKED A MAXIMUM OF 3 TIMES PER PROMPT, SO USE YOUR QUERIES WISELY"""
		if self.search_calls>3:
			return """Max limit on search calls exceeded"""

		search_result = tavily_client.search(query)
		print(" === AGENT CALLED SEARCH TOOL === ")
		print(f"Query: {query}\n")
		print(f"Responses: {search_result}")
		self.search_calls += 1
		return search_result
    
	def call(self, query):
		self.search_calls = 0
		research_content = self.research_agent.invoke({
			"messages": [
				{"role": "user", "content": query}
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
