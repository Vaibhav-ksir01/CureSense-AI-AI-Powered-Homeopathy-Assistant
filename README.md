# Intellex: AI-Powered Knowledge Assistant

This project demonstrates a **versatile AI chatbot** using **Retrieval-Augmented Generation (RAG)** and **Neo4j as a Knowledge Graph**, built with **LangChain** and **OpenAI LLMs**. The model efficiently retrieves, structures, and understands domain-specific data for **accurate, context-aware responses**. It is scalable for various applications, including **education, finance, healthcare, legal, research, and enterprise use**.

## Features
- **Knowledge Graph** integration with **Neo4j** for structured data storage
- **PDF-based document ingestion** (Processes multiple PDFs stored in a folder)
- **LangChain-powered RAG implementation** for enhanced retrieval
- **OpenAI LLMs (GPT-4/GPT-3.5-turbo) for intelligent query handling**
- **Token-based document splitting** for efficient processing
- **Graph visualization using yFiles Jupyter Graphs**
- **Environment variable-based credential handling**

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Vaibhav-ksir01/Intellex-AI-Powered-Knowledge-Assistant.git
cd Intellex-AI-Powered-Knowledge-Assistant
```

### 2. Install Dependencies
Ensure you have Python 3.8+ installed. Then, run:
```bash
pip install -r requirements.txt
```

### 3. Setup Neo4j Database
#### **Option 1: Using Neo4j Desktop**
1. Download and install **Neo4j Desktop** from [Neo4j Official Site](https://neo4j.com/download/).
2. Create a **New Project** and **New Database**.
3. Set a **username** and **password** (store them for later use).
4. Start the database and note the **Bolt URI** (usually `bolt://localhost:7687`).

#### **Option 2: Using Neo4j AuraDB (Cloud)**
1. Go to [Neo4j AuraDB](https://neo4j.com/cloud/aura/).
2. Sign up and create a **free database**.
3. Note the **connection credentials** (Bolt URI, username, password).

### 4. Configure Environment Variables
Create a `.env` file in the project root and add:
```ini
OPENAI_API_KEY=your_openai_api_key
NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=your_database_name
```

### 5. Run the Application
```bash
jupyter notebook
```
Open `QA_KG_RAG.ipynb` and run the cells in order.

## Usage
- Store multiple **PDFs** in a specified folder.
- The system processes and indexes the PDFs into a **Neo4j Knowledge Graph**.
- **Graph-based AI retrieval** enhances accuracy and structure in responses.
- Query the system, and **OpenAI LLMs** generate precise, context-aware answers.
- **Graph visualization** provides insights into relationships within the data.

## Contributions
Feel free to contribute via pull requests.

## Future Enhancements
- **Integration of Agentic AI** for autonomous reasoning and workflow automation.
- **Support for real-time data ingestion and knowledge updates.**
- **Enhancing multi-modal retrieval (images, videos, and structured databases).**

