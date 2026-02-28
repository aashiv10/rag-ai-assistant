# RAG AI Assistant

A Retrieval-Augmented Generation (RAG) powered AI assistant that performs contextual question-answering over uploaded documents. It uses LangChain for orchestration, FAISS for vector storage, OpenAI for embeddings and LLM responses, and FastAPI for backend deployment.

------------------------------------------------------------

FEATURES

- Upload PDF or TXT documents
- Convert documents into embeddings
- Store embeddings using FAISS
- Retrieve relevant chunks based on user query
- Generate context-aware answers using an LLM
- FastAPI-based backend for real-time interaction

------------------------------------------------------------

TECH STACK

- Python
- FastAPI
- LangChain
- FAISS
- OpenAI API
- Uvicorn

------------------------------------------------------------

PROJECT STRUCTURE

rag-ai-assistant/
│
├── app.py              # Main FastAPI application
├── index.html          # Simple frontend UI
├── requirements.txt    # Dependencies
├── .gitignore

------------------------------------------------------------

PREREQUISITES

- Python 3.9 or higher
- pip installed
- OpenAI API key

------------------------------------------------------------

INSTALLATION STEPS

1. Clone the Repository

git clone https://github.com/aashiv10/rag-ai-assistant.git
cd rag-ai-assistant

2. Create Virtual Environment (Recommended)

Windows:
python -m venv venv
venv\Scripts\activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

------------------------------------------------------------

SET ENVIRONMENT VARIABLE

You must set your OpenAI API key.

Windows (PowerShell):
setx OPENAI_API_KEY "your_api_key_here"

Mac/Linux:
export OPENAI_API_KEY="your_api_key_here"

Or create a .env file (if dotenv is used):

OPENAI_API_KEY=your_api_key_here

------------------------------------------------------------

RUN THE APPLICATION

Start the FastAPI server using Uvicorn:

uvicorn app:app --reload

The server will start at:
http://127.0.0.1:8000

------------------------------------------------------------

ACCESS THE APPLICATION

API docs:
http://127.0.0.1:8000/docs

If index.html is served through FastAPI:
http://127.0.0.1:8000

------------------------------------------------------------

HOW IT WORKS

1. Upload a document.
2. The document is split into chunks.
3. Chunks are converted into embeddings.
4. Embeddings are stored in FAISS.
5. User asks a question.
6. Relevant chunks are retrieved.
7. LLM generates an answer using retrieved context.

------------------------------------------------------------

EXAMPLE API REQUEST

POST /ask
{
    "question": "What is this document about?"
}

Example Response:
{
    "answer": "Generated contextual response here."
}

------------------------------------------------------------
