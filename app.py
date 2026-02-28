import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vector store (for demo purpose)
vector_store = None

class QuestionRequest(BaseModel):
    question: str


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store

    try:
        # Save file temporarily
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Load PDF
        loader = PyPDFLoader(file_location)
        documents = loader.load()

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        docs = text_splitter.split_documents(documents)

        # Create embeddings
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Store in FAISS
        vector_store = FAISS.from_documents(docs, embeddings)

        return {
            "message": "PDF uploaded and processed successfully.",
            "chunks": len(docs)
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    global vector_store

    try:
        if vector_store is None:
            return {"error": "No PDF has been uploaded yet. Please upload a PDF first."}

        # Create retrieval chain
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )

        # Get answer
        answer = qa_chain.run(request.question)

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()


@app.get("/endpoints")
async def endpoints():
    return {
        "message": "RAG AI Assistant API",
        "endpoints": {
            "GET /": "Frontend HTML page",
            "POST /upload": "Upload a PDF file",
            "POST /ask": "Ask a question about the uploaded PDF"
        }
    }
