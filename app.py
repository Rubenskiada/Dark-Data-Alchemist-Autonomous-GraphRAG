import os
import streamlit as st
from google import genai
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Dark Data Alchemist",
    page_icon="⚡",
    layout="wide"
)

# Title & Branding
st.title("⚡ Dark Data Alchemist")
st.caption("Autonomous GraphRAG & Causal Knowledge Engine powered by Gemini 3.5")

# Sidebar Status
with st.sidebar:
    st.header("System Status")
    st.success("Watchdog Agent: ACTIVE")
    st.info("Graph Memory Bank: READY")
    st.markdown("---")
    st.markdown("**Model:** `gemini-3.5-flash`")
    st.markdown("**Architecture:** Autonomous Multi-Agent GraphRAG")

# Setup Connections
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else genai.Client()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am the Dark Data Alchemist. Ask me about server incident timelines, root cause analysis, or causal graph links."}
    ]

# Render Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask a question about incident root causes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing graph memory bank & causal chains..."):
            try:
                # 1. Translate question into Graph Query
                query_prompt = f"""
                You are a Neo4j database administrator.
                The database ONLY has nodes with the label `:Node` and relationships with the type `:LINKED_TO`.
                User Question: {prompt}
                Write a Cypher query that extracts the most important noun from the user's question. 
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
                
                # 2. Execute Query against Neo4j
                with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)) as driver:
                    records, summary, keys = driver.execute_query(cypher_query, database_="neo4j")
                    
                    raw_data = [str(record.data()) for record in records]
                    
                    if not raw_data:
                        answer = "I couldn't find an answer to that in the current graph."
                    else:
                        # 3. Synthesize the final answer
                        synthesis_prompt = f"""
                        You are a helpful AI assistant summarizing graph database results.
                        User Question: {prompt}
                        Raw Graph Data: {raw_data}
                        Read the raw graph data carefully. Trace the connections and answer the user's question clearly.
                        """
                        final_response = client.models.generate_content(
                            model='gemini-3.5-flash',
                            contents=synthesis_prompt
                        )
                        answer = final_response.text.strip()

                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                err_msg = f"**System Notice:** Query failed.\n\n*Error details:* `{str(e)}`"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})