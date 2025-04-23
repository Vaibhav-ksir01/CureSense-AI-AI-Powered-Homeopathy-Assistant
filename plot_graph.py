from data_extraction import raw_document
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import AzureChatOpenAI
from langchain_neo4j import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from config import NEO4J_URI,NEO4J_PASSWORD,NEO4J_USERNAME
from config import AZURE_API_KEY, AZURE_MODEL_NAME, AZURE_API_VERSION, AZURE_ENDPOINT

text_splitter = TokenTextSplitter(chunk_size = 1024, chunk_overlap = 48)
documents = {key: sorted(text_splitter.split_documents(value), key=lambda doc: doc.metadata['source']) for key, value in raw_document.items()}

for key, value in raw_document.items():
    for doc in value:
        doc.metadata.clear()
        doc.metadata['producer'] = key

# Initialize Language Model
llm = AzureChatOpenAI(
    azure_deployment=AZURE_MODEL_NAME,
    model=AZURE_MODEL_NAME,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY
)

llm_transformer = LLMGraphTransformer(llm = llm) #Transformer that transform data to graph

#Transforming the Data in a form that can be plotted as a Knowledge graph
graph_document = {}
for key, value in raw_document.items():
    print("start",key)
    graph_document[key]=llm_transformer.convert_to_graph_documents(value)
    print("complete\n")

# Establish connection to Neo4j
graph = Neo4jGraph(url = NEO4J_URI, username = NEO4J_USERNAME, password = NEO4J_PASSWORD)

#Plotting the Knowledge Graph
for key, value in graph_document.items():
    print(key)
    graph.add_graph_documents(
        value,
        baseEntityLabel=True,
        include_source=True
    )