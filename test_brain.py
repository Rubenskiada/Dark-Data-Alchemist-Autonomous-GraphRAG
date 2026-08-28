import os
from dotenv import load_dotenv
from google import genai
from neo4j import GraphDatabase

# 1. Load your hidden passwords
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# 2. Wake up the Gemini AI
print("Waking up Gemini...")
client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model='gemini-3.5-flash',
    contents='Give me a one sentence summary of what a Knowledge Graph is.'
)
ai_answer = response.text
print(f"Gemini says: {ai_answer}")

# 3. Connect to your Graph Database
print("Connecting to Neo4j...")
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", NEO4J_PASSWORD)

def create_concept_node(driver, concept_name, description):
    query = """
    MERGE (c:Concept {name: $concept_name})
    SET c.description = $description
    RETURN c.name
    """
    driver.execute_query(query, concept_name=concept_name, description=description, database_="neo4j")

# 4. Save Gemini's answer as a node in the graph
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    create_concept_node(driver, "Knowledge Graph", ai_answer)
    print("Success! The AI's answer has been woven into your Graph Database.")