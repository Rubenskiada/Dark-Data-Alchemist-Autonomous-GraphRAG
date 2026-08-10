# Dark-Data-Alchemist-Autonomous-GraphRAG
Dark Data Alchemist: Autonomous GraphRAG
# 🌌 Dark Data Alchemist: Autonomous GraphRAG Pipeline

**Built for the Google Gemini API Developer Competition (August 2026)**

Enterprise companies bleed millions of dollars during IT outages because engineers have to dig through disconnected, unstructured text logs and chat histories to find the root cause of an issue. The data is there, but the *connections* are missing.

The **Dark Data Alchemist** solves this. It is an autonomous, multi-agent pipeline that uses **Google Gemini 3.5 Flash** to ingest raw, chaotic text, mathematically extract the unbroken "causal chains," and weave them into a highly queryable **Neo4j Knowledge Graph**. 

We then close the loop with a custom **GraphRAG** (Retrieval-Augmented Generation) agent that utilizes "Fuzzy Net" querying to allow users to ask plain-English questions and instantly trace multi-hop root causes.

---

## 🏗 System Architecture

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
        DF[📁 ./data Directory Logs]:::data
        WD[Watchdog Agent watchdog.py]:::agent
    end
    
    subgraph Knowledge_Engine
        G1{Google Gemini 3.5 Flash Structuring}:::llm
        G2{Google Gemini 3.5 Flash Synthesis}:::llm
    end
    
    subgraph Storage
        N[(Neo4j Graph Database Memory Bank)]:::db
    end
    
    subgraph Retrieval_GraphRAG
        CA[Chat Agent chat.py]:::agent
    end

    DF -- 1. Drop new incident log --> WD
    WD -- 2. Pass raw text for structuring --> G1
    G1 -- 3. Return structured JSON Causal Chain --> WD
    WD -- 4. Weave Entities & Relationships --> N

    U -- A. Ask Natural Language Question --> CA
    CA -- B. Extract core entity Noun --> G2
    G2 -- C. Return Fuzzy Keyword --> CA
    CA -- D. Execute Multi-Hop Cypher Query --> N
    N -- E. Return raw causal path data --> CA
    CA -- F. Pass raw data for synthesis --> G2
    G2 -- G. Return English Root-Cause Summary --> CA
    CA -- H. Deliver Final Answer --> U
