# Order to Cash Graph & Chat System

## Overview
This repository contains a full-stack context graph system with an LLM-powered query interface. It unifies a fragmented SAP Order to Cash dataset into a graph representation and enables users to intuitively explore the data through a visual graph node interface and a conversational chat module.

## Architecture

The system is designed with a modern dual-pane web application architecture paired with a modular python microservice.

### Frontend
- **Framework**: React via Vite
- **Visuals**: Modern responsive UI with vanilla CSS, inspired by enterprise neo-morphism aesthetics.
- **Graph Visualization**: `react-force-graph-2d` utilizing a D3-based physics engine to render dynamic, color-coded interconnected entities.
- **Component State**: Data retrieval occurs over REST API pulling context graph elements (Nodes/Edges) dynamically as well as conversational capabilities.

### Backend
- **Framework**: Python with FastAPI for high performance asynchronous request handling.
- **Data Engine**: SQLite backend with data transformation pipeline.
- **LLM Integration**: Integrated with Google Gemini APIs for Text-to-SQL synthesis and analytical text generation.

## Database Choice
**SQLite** was strictly chosen for the core implementation.
While native graph databases like Neo4j can represent entities very well, mapping massive datasets into a traditional local machine for an assignment involves significant infrastructure overhead. 
We approached graph abstraction dynamically over relational data:
- The data models were mapped into relational structures.
- A dynamic connection engine builds nodes and edges natively via SQL joins, acting as a functional knowledge graph.
- This allows translating natural language queries efficiently into structured SQL requests without compromising the data graph integrity, resulting in rapid responses.

## LLM Prompts & Querying Strategy

The system relies on a two-pass LLM querying proxy method (The Text-To-SQL methodology):
1. **The Translation Pass**: Ingests the Natural Language query and feeds it to the LLM alongside the automatically extracted schema (metadata) of the relational database. The instruction strictly demands an executable SQL Query back.
2. **The Execution Engine**: The system safely runs the validated `SELECT` queries across the SQLite interface and retrieves row-based information.
3. **The Data-backed Synthesis Pass**: The resulting data is subsequently fed back into a secondary LLM pipeline with instructions to generate a human-readable, context-aware answer grounded *solely* in the retrieved dataset.

*Note: For the LLM to process live questions, please export the `GEMINI_API_KEY` in the environment running the backend.*

## Guardrails
The system protects domain integrity and dataset containment using multiple layers of guardrails against off-topic or hazardous queries:
1. **Static Rules**: The python backend runs keyword validation and denies system modifications (`UPDATE`, `DROP`, `INSERT`) pre-emptively on SQL generation.
2. **LLM Prompts**: The prompt injection for generating queries mandates `"If it's unrelated to the domain, write OUT_OF_DOMAIN"`. The system captures this and forces a compliant default response: *"This system is designed to answer questions related to the provided dataset only."*
3. **Conversational Scoping**: Purely conversational interactions (e.g., standard greetings not yielding SQL components) are cleanly handled with introductory welcoming texts, declining requests to write creative texts or answer general knowledge outside of Order to Cash dynamics.
