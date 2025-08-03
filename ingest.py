import os
import git
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document
from config import OPENAI_API_KEY, REPO_LOCAL_PATH, CHROMA_DB_DIR
from tqdm import tqdm

def clone_repo(github_url):
    if os.path.exists(REPO_LOCAL_PATH):
        print("Repo already cloned.")
    else:
        print("Cloning...")
        git.Repo.clone_from(github_url, REPO_LOCAL_PATH)

def load_code_files():
    docs = []
    for root, _, files in os.walk(REPO_LOCAL_PATH):
        for file in files:
            if file.endswith((".py", ".js", ".java", ".md")):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    docs.append(Document(page_content=content, metadata={"source": path}))
    return docs

def embed_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=CHROMA_DB_DIR)
    db.persist()
    print(f"Embedded {len(chunks)} chunks.")

if __name__ == "__main__":
    github_url = input("Enter GitHub repo URL: ")
    clone_repo(github_url)
    docs = load_code_files()
    embed_documents(docs)
