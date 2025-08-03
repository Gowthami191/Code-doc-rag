# Code-doc-rag
Project Overview
Title: Code Documentation RAG (Retrieval-Augmented Generation)
Goal: Build an AI-powered system that:
Accepts a GitHub repo (as a ZIP)
Processes code in multiple languages
Answers natural language questions about the code
Explains API usage, logic, and implementation
Technologies Used:
   Frontend: Streamlit
   Backend: Python (LangChain, ChromaDB, GROQ or OpenAI)
   Embeddings & LLM: GROQ (Mixtral, LLaMA), or OpenAI (GPT-3.5/4)
   Vector DB: Chroma
 1.Clone the Repository
```bash
git clone https://github.com/Gowthami191/code-doc-rag.git
cd code-doc-rag
2.  Create Virtual Environment (Optional but Recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
3.  Install Dependencies
        pip install -r requirements.txt
API Key Setup
We use GROQ's LLaMA 3 as the LLM backend.
4. Get a GROQ API Key
Sign up at https://console.groq.com
Copy your API key.
5. Add Your API Key to .env
Create a .env file in the project root:
    GROQ_API_KEY=your_actual_groq_api_key
Use the command to run the App:
      streamlit run app.py
How It Works
Upload ZIP repo
1.Streamlit extracts and reads all code files.
2.Chunking & Embedding
   RecursiveCharacterTextSplitter splits files into manageable pieces.
   Embeddings generated via HuggingFace.
3.Storage in ChromaDB
   Vector representations are stored locally in chroma_db/.
4.Question Answering
   Your query is embedded, relevant chunks retrieved, LLaMA 3 generates the answer.
Deployment link:https://code-doc-rag.streamlit.app/
