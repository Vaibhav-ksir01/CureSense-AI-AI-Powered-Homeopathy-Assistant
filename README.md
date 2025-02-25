# QA Model using Knowledge Graph and RAG

This project demonstrates a **Retrieval-Augmented Generation (RAG) model** using **Neo4j as a knowledge graph** and **LangChain** for intelligent query handling. The model allows users to extract insights from structured and unstructured data sources, including Wikipedia and PDF documents.

## Features
- **Knowledge Graph** integration with **Neo4j**
- **Multi-source document ingestion** (Wikipedia, PDFs)
- **LangChain-powered RAG implementation**
- **GPT-3.5-turbo for conversational AI**
- **Token-based document splitting** for efficient processing
- **Environment variable-based credential handling**

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Vaibhav-ksir01/QA-Application-Using-Knowledge-Graph-and-RAG.git
cd QA-Application-Using-Knowledge-Graph-and-RAG
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
Open `space.ipynb` and run the cells in order.

## Usage
- Enter a topic to train the model.
- The model fetches **Wikipedia articles** and/or **PDF content**.
- **Chunk-based text processing** is applied for efficient indexing.
- Neo4j stores structured knowledge for better retrieval.

## Contributions
Feel free to contribute via pull requests.
