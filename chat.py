import os
from dotenv import load_dotenv
from google import genai
from neo4j import GraphDatabase

# 1. Setup Connections
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", NEO4J_PASSWORD)

client = genai.Client(api_key=GEMINI_API_KEY)

def chat_with_graph(question):
    print(f"\n[You]: {question}")
    
    print("[Agent] Translating your question into a Graph Query...")
    
    # The "Fuzzy Net" Query Generator
    query_prompt = f"""
    You are a Neo4j database administrator.
    
    The database ONLY has nodes with the label `:Node` and relationships with the type `:LINKED_TO`.
    
    User Question: {question}
    
    Write a Cypher query that extracts the most important noun from the user's question (e.g. if the question is "What caused the AWS Database crash?", the noun is "AWS"). 
    Then, find ANY node where the name CONTAINS that noun (case-insensitive), and return all nodes and relationships connected to it up to 4 hops away.
    
    Example Query Structure to follow exactly:
    MATCH path = (n:Node)-[:LINKED_TO*1..4]-(m:Node)
    WHERE toLower(n.name) CONTAINS toLower('noun_from_question')
    RETURN path
    
    Write ONLY the raw Cypher query. Do not include markdown formatting like ```cypher.
    """
    
    cypher_response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=query_prompt
    )
    cypher_query = cypher_response.text.strip().replace('```cypher', '').replace('```', '')
    
    print(f"[Agent] Running Query: {cypher_query}")
    
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            records, summary, keys = driver.execute_query(cypher_query, database_="neo4j")
            
            raw_data = []
            for record in records:
                raw_data.append(str(record.data()))
            
            if not raw_data:
                print("\n[Dark Data Alchemist]: I couldn't find an answer to that in the current graph.")
                return
            
            print("[Agent] Synthesizing the final answer...")
            synthesis_prompt = f"""
            You are a helpful AI assistant summarizing graph database results.
            
            User Question: {question}
            Raw Graph Data: {raw_data}
            
            Read the raw graph data carefully. Trace the connections and answer the user's question clearly. If it's a chain of events, explain the full chain from start to finish.
            """
            
            final_response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=synthesis_prompt
            )
            
            print(f"\n[Dark Data Alchemist]: {final_response.text.strip()}")
            
        except Exception as e:
            print(f"\n[Error] The query failed to execute: {e}")

if __name__ == "__main__":
    print("Welcome to the Dark Data Alchemist Chat! Type 'exit' to quit.")
    while True:
        user_input = input("\nAsk the Graph: ")
        if user_input.lower() == 'exit':
            break
        chat_with_graph(user_input)