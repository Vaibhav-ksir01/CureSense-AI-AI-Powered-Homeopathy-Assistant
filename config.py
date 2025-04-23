import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure OpenAI Credentials
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_MODEL_NAME = os.getenv("AZURE_MODEL_NAME")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

# Neo4j Credentials
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
