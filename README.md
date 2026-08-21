# Dark-Data-Alchemist-Autonomous-GraphRAG

Dark Data Alchemist: Autonomous GraphRAG

## 🌌 Dark Data Alchemist: Autonomous GraphRAG Pipeline

**Built for the All Things Agentic Hackathon**

Enterprise companies bleed millions of dollars during IT outages because engineers have to dig through disconnected, unstructured text logs and chat histories to find the root cause of an issue. The data is there, but the *connections* are missing.

The **Dark Data Alchemist** solves this. It is an autonomous, multi-agent pipeline that uses **Google Gemini 3.5 Flash** to ingest raw, chaotic text, mathematically extract the unbroken "causal chains," and weave them into a highly queryable **Neo4j Knowledge Graph**.

We then close the loop with a custom **GraphRAG** (Retrieval-Augmented Generation) agent that utilizes "Fuzzy Net" querying to allow users to ask plain-English questions and instantly trace multi-hop root causes.

## Inspiration
In enterprise IT and Level 2 infrastructure support, teams bleed time and money during critical outages not because they lack data, but because they lack context. Incident reports, chat logs, and escalation tickets create mountains of "dark data"—unstructured text where the true root cause is buried across multiple disconnected systems.

We realized that standard chatbots and RAG (Retrieval-Augmented Generation) systems fail here. They just summarize symptoms. To find a root cause, you need to traverse the chain of events. That inspired us to build the Dark Data Alchemist: an autonomous pipeline that transforms chaotic IT logs into a mathematical, highly queryable Knowledge Graph.

## What it does
The Dark Data Alchemist is an asynchronous, multi-agent GraphRAG pipeline.

* **Autonomous Ingestion:** A Python "Watchdog" agent monitors a designated directory for incoming, unstructured incident reports.
* **Structuring:** It passes the raw text to Google Gemini 3.5 Flash, strictly prompting it to extract entities (People, Tech, Events) and weave them into an unbroken "Causal Chain" (JSON).
* **Storage:** The structured data is instantly injected into a Neo4j graph database, serving as the permanent corporate memory bank.
* **GraphRAG Retrieval:** When an engineer asks a plain-English question (e.g., "What caused the AWS Database crash?"), our Chat Agent queries the graph, traversing up to 4 hops deep to find the root cause, and uses Gemini to synthesize a perfect, human-readable summary.

## How we built it
We prioritized a decoupled, production-ready architecture over a brittle script.
* **Compute & Reasoning:** Google GenAI SDK (Gemini 3.5 Flash)
* **Storage & State:** Neo4j Database
* **Hosting & UI:** Google Cloud Run & Streamlit

## 🏗️ System Architecture

*The diagram below outlines the decoupled ingestion and retrieval flow.*

```mermaid
graph TD
    classDef user fill:#6c5ce7,stroke:#333,stroke-width:2px,color:white;
    classDef agent fill:#0984e3,stroke:#333,stroke-width:2px,color:white;
    classDef llm fill:#00b894,stroke:#333,stroke-width:2px,color:white;
    classDef db fill:#d63031,stroke:#333,stroke-width:2px,color:white;
    classDef data fill:#fdcb6e,stroke:#333,stroke-width:2px,color:black;

    U((User / Engineer)):::user

    subgraph Data_Ingestion
        DF[📂 ./data Directory Logs]:::data
        WD[Watchdog Agent watchdog.py]:::agent
    end

    subgraph Knowledge_Engine
        G1{Google Gemini 3.5 Flash Structuring}:::llm
        G2{Google Gemini 3.5 Flash Synthesis}:::llm
    end

    subgraph Storage
        N[(Neo4j Knowledge Graph)]:::db
    end

    subgraph Retrieval
        CA[Chat Agent chat.py]:::agent
    end

    DF --> WD
    WD --> G1
    G1 --> N
    U --> CA
    CA --> G2
    G2 --> N
    N -.->|Graph Context| G2
    G2 --> CA
    CA -->|Final Answer| U
⚙️ Reproducible Testing Instructions
To run the Dark Data Alchemist multi-agent pipeline locally, follow these steps:

1. Clone the Repository
git clone [https://github.com/Rubenskiada/Dark-Data-Alchemist-Autonomous-GraphRAG.git](https://github.com/Rubenskiada/Dark-Data-Alchemist-Autonomous-GraphRAG.git)
cd Dark-Data-Alchemist-Autonomous-GraphRAG

2. Install Dependencies
Ensure you have Python 3.9+ installed.
pip install google-genai neo4j streamlit

3. Environment Setup
Create a .env file in the root directory and add your credentials:
GEMINI_API_KEY="your_api_key_here"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="your_password"

4. Run the Pipeline

Step 1: Start the Watchdog extraction agent to ingest logs into Neo4j:
python watchdog.py

Step 2: Launch the interactive GraphRAG interface:
streamlit run chat.py
