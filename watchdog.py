import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from neo4j import GraphDatabase

# 1. Load Environment Variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", NEO4J_PASSWORD)
DATA_DIR = Path("./data")

def build_graph(driver, entities, relationships):
    """Takes the structured data from Gemini and draws the circles and lines in Neo4j."""
    
    # Draw the Nodes
    for ent in entities:
        query = """
        MERGE (n:Node {name: $name})
        SET n.type = $type
        """
        driver.execute_query(query, name=ent["name"], type=ent["type"], database_="neo4j")
        
    # Draw the Relationships
    for rel in relationships:
        query = """
        MATCH (a:Node {name: $source})
        MATCH (b:Node {name: $target})
        MERGE (a)-[r:LINKED_TO]->(b)
        SET r.action = $action
        """
        driver.execute_query(query, source=rel["source"], target=rel["target"], action=rel["action"], database_="neo4j")

def process_and_ingest():
    files = list(DATA_DIR.glob("*.txt"))
    if not files:
        print("No files found to process.")
        return

    client = genai.Client(api_key=GEMINI_API_KEY)

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        for file_path in files:
            print(f"\n[Watchdog] Processing file: {file_path.name}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            print("[Gemini] Extracting Graph Nodes and Relationships...")
            
            # The Causal Chain Prompt
            prompt = f"""
            You are an enterprise Root Cause Analysis AI. Read the incident report below.
            Extract the entities (People, Technology, Events) and map the unbroken chain of events.
            
            CRITICAL INSTRUCTION: You MUST connect the root cause all the way to the final symptom. Do not leave disconnected clusters. If A caused B, and B affected C, you must extract a single continuous path connecting A to C.
            
            Format your response as EXACTLY this JSON structure, nothing else:
            {{
              "entities": [
                {{"name": "Entity Name", "type": "Person/Technology/Event"}}
              ],
              "relationships": [
                {{"source": "Entity 1", "action": "CAUSED_OR_AFFECTED", "target": "Entity 2"}}
              ]
            }}
            
            Text to analyze:
            {content}
            """
            
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt
            )
            
            raw_text = response.text.replace('```json', '').replace('```', '').strip()
            
            try:
                graph_data = json.loads(raw_text)
                print(f"[Gemini Output] Extracted {len(graph_data['entities'])} entities and {len(graph_data['relationships'])} relationships.")
                
                build_graph(driver, graph_data["entities"], graph_data["relationships"])
                print(f"[Neo4j] Knowledge Graph successfully woven for {file_path.name}!")
                
            except Exception as e:
                print(f"Error parsing Gemini's output: {e}")
                print(f"Raw output was:\n{raw_text}")

if __name__ == "__main__":
    process_and_ingest()