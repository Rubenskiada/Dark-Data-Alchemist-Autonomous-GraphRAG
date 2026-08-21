import os
import json
from google import genai
from neo4j import GraphDatabase
from dotenv import load_dotenv

# --- Load Hidden Environment Variables ---
load_dotenv()

# --- System Configurations ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
DATA_DIR = "data"

def build_graph(driver, entities, relationships):
    """Weaves the extracted JSON into the Neo4j Graph Database."""
    with driver.session() as session:
        # Create Nodes (Entities)
        for ent in entities:
            session.run(
                "MERGE (n:Node {name: $name}) SET n.type = $type",
                name=ent.get("name", "Unknown"),
                type=ent.get("type", "Entity")
            )
        # Create Edges (Relationships)
        for rel in relationships:
            session.run(
                """
                MATCH (source:Node {name: $source})
                MATCH (target:Node {name: $target})
                MERGE (source)-[r:LINKED_TO {action: $action}]->(target)
                """,
                source=rel.get("source"),
                target=rel.get("target"),
                action=rel.get("action", "LINKED_TO")
            )

def process_and_ingest():
    """Main Watchdog Loop: Reads files, Triages, Extracts, and Ingests."""
    print("\n[Watchdog] Awakening Dark Data Alchemist Pipeline...")
    
    # Initialize Client with explicitly loaded API Key
    client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else genai.Client()
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    if not os.path.exists(DATA_DIR):
        print(f"[Watchdog] Directory '{DATA_DIR}' not found. Please create it.")
        return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_DIR, filename)
            print(f"\n[Watchdog] Processing file: {filename}")
            
            with open(file_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            
            # ---------------------------------------------------------
            # BONUS PHASE 2: MULTI-AGENT SEVERITY TRIAGE
            # ---------------------------------------------------------
            print("[Watchdog] Initiating Severity Triage...")
            try:
                triage_prompt = f"You are a DevOps Triage Agent. Read this log and reply with ONLY ONE WORD (Critical, Warning, or Routine):\n\n{raw_text}"
                triage_response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=triage_prompt
                )
                severity = triage_response.text.strip().replace('*', '')
                print(f"[Triage Agent] Incident Classified as: **{severity}**")
            except Exception as e:
                print(f"[Triage Agent] Triage bypassed due to error: {e}")
            # ---------------------------------------------------------

            # --- GRAPH EXTRACTION ---
            print("[Gemini] Extracting Graph Nodes and Relationships...")
            extraction_prompt = f"""
            You are a Graph Extraction AI. Read the text below and extract entities and relationships.
            Format the output exactly as JSON:
            {{
                "entities": [{{"name": "...", "type": "..."}}],
                "relationships": [{{"source": "...", "target": "...", "action": "..."}}]
            }}
            Text: {raw_text}
            """
            
            try:
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=extraction_prompt
                )
                
                # Clean markdown formatting from Gemini response
                clean_json = response.text.replace('```json', '').replace('```', '').strip()
                graph_data = json.loads(clean_json)
                
                entities = graph_data.get('entities', [])
                relationships = graph_data.get('relationships', [])
                
                print(f"[Gemini Output] Extracted {len(entities)} entities and {len(relationships)} relationships.")
                
                # Ingest to Neo4j
                build_graph(driver, entities, relationships)
                print(f"[Neo4j] Knowledge Graph successfully woven for {filename}!")
                
            except Exception as e:
                print(f"[Error] Failed to process {filename}: {e}")

    driver.close()

if __name__ == "__main__":
    process_and_ingest()