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

### 📂 Repository Structure
* **`alchemist_watchdog.py`**: Autonomous file system observer and severity triage agent.
* **`chat.py`**: CLI-based Fuzzy Net query generator and GraphRAG retrieval logic.
* **`app.py`**: Interactive Streamlit user interface for the GraphRAG chat.
* **`test_brain.py`**: Graph database connectivity and Gemini extraction testing.
* **`data/`**: Target directory for unstructured incident logs.

### ☁️ Technical Insights & Google Cloud Integration
* **Google Cloud Usage:** The core reasoning engine is powered by the Google GenAI SDK (Gemini 3.5 Flash), handling high-speed extraction and synthesis of the graph-retrieved context. 
* **State Management:** Instead of writing to vulnerable flat files, multiple agents interact seamlessly by utilizing Neo4j as the persistent "memory bank," naturally resolving state update conflicts through transactional Cypher queries.

### ⚙️ Reproducible Testing Instructions

**1. Clone the Repository**
```bash
git clone [https://github.com/Rubenskiada/Dark-Data-Alchemist-Autonomous-GraphRAG.git](https://github.com/Rubenskiada/Dark-Data-Alchemist-Autonomous-GraphRAG.git)
cd Dark-Data-Alchemist-Autonomous-GraphRAG