import os
import traceback
from openai import OpenAI
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables from .env file
load_dotenv()

# Set GROQ API Key and Model
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY environment variable not set.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

GROQ_MODEL = "llama3-70b-8192"

# Supported file extensions
SUPPORTED_EXTENSIONS = (
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs",
    ".go", ".rs", ".rb", ".php", ".html", ".css", ".json", ".md"
)

def process_code_files(folder_path):
    """Extract and chunk supported code files from a folder."""
    documents = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    chunks = splitter.split_text(content)
                    for chunk in chunks:
                        documents.append(f"File: {file}\n{chunk}")
                except Exception as e:
                    print(f"⚠️ Error reading {file}: {e}")
    return documents


def answer_query(query, documents, top_k=20):
    """Generate a response to a query using retrieved document context."""
    try:
        if not documents:
            return "⚠️ No documents processed. Please upload a codebase first."

        context = "\n\n".join(documents[:top_k])
        prompt = (
            "You are a helpful AI assistant specialized in understanding and explaining software codebases.\n\n"
            f"Context from code files:\n{context}\n\n"
            f"User's Question: {query}\n\n"
            "Please provide a concise and clear explanation or code example if applicable."
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are a code expert and helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        error_msg = traceback.format_exc()
        print("❌ Error in answer_query():\n", error_msg)
        return f"⚠️ An error occurred while answering the query:\n```\n{error_msg}\n```"
