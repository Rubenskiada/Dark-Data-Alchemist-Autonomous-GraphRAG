# ⚡ Dark Data Alchemist: Autonomous GraphRAG Pipeline

**Built for the All Things Agentic Hackathon**

In enterprise IT, managing front office escalations and troubleshooting hardware infrastructure usually comes down to one thing: context. Teams bleed time and money during critical outages because the true root cause is buried across disconnected tickets, incident reports, and chat logs. Standard RAG (Retrieval-Augmented Generation) chatbots fail here because they only summarize symptoms. To actually solve a failure, you must traverse the chain of events.

That is where **Neo4j** changes the game. We built the Dark Data Alchemist to autonomously transform chaotic "dark data" into a permanent, highly queryable Knowledge Graph. It does not just read logs; it mathematically connects the dots.

### 📖 How It Works
The system operates as a decoupled, asynchronous multi-agent pipeline:
*   **Autonomous Triage:** A Python Watchdog monitors directories for unstructured logs, instantly triaging the severity of the incident.
*   **Causal Extraction:** Google Gemini 3.5 Flash parses the text to extract technical entities and their direct relationships into JSON format.
*   **Graph Storage (Neo4j):** These extracted chains are injected directly into a Neo4j database, building an unbroken map of the IT infrastructure's history.
*   **Fuzzy Net GraphRAG:** Using a Streamlit UI, engineers ask plain-English questions. The agent writes a custom Cypher query, pulls the multi-hop root cause from Neo4j, and synthesizes a human-readable solution.

### 🛠️ Tech Stack
*   **Compute & Reasoning:** Google GenAI SDK (Gemini 3.5 Flash)
*   **State & Storage:** Neo4j Graph Database
*   **User Interface:** Streamlit

### ⚙️ Reproducible Testing Instructions

**1. Clone the Repository**
`git clone https://github.com/Rubenskiada/Dark-Data-Alchemist-Autonomous-GraphRAG.git`
`cd Dark-Data-Alchemist-Autonomous-GraphRAG`

**2. Install Dependencies** 
Ensure you have Python 3.9+ installed. It is highly recommended to use a virtual environment.
`pip install -r requirements.txt`

**3. Environment Setup** 
Create a `.env` file in the root directory and add your credentials (you can use `.env.example` as a template):
`GEMINI_API_KEY="your_api_key_here"`
`NEO4J_URI="bolt://localhost:7687"`
`NEO4J_USER="neo4j"`
`NEO4J_PASSWORD="your_password"`

**4. Run the Pipeline**
First, start the Watchdog extraction agent to ingest your unstructured logs into Neo4j:
`python alchemist_watchdog.py`

Next, open a new terminal tab and launch the interactive GraphRAG interface:
`streamlit run app.py`
