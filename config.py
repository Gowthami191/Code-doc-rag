import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPO_LOCAL_PATH = "./repo"
CHROMA_DB_DIR = "./chroma_db"
