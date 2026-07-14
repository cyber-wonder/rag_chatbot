from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings



def load_document(file_path):
    print("Loading Document ...")
    document = PyPDFLoader(file_path)
    pages = document.load()
    print("Document Loaded successfully.")
    return pages

def create_chunks(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_documents(pages)
    return chunks


def embed_and_store(chunks):
    # embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        api_key=settings.gemini_api_key
    )
    vector_store = Chroma.from_documents(
        collection_name="chunk_vectors", # Like a table in a SQL DB
        persist_directory="./chroma_db",
        embedding=embedding_model,
        documents=chunks
    )



