from fastapi.security import api_key
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from config import settings


def retrieve_context(prompt):
    # setup embedding function
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=settings.gemini_api_key
    )

    # Load vector database
    vectordb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_model,
        collection_name="chunk_vectors"
    )

    # Do similarity check
    retrieved_docs = vectordb.similarity_search(
        prompt,
        k=5
    )
    # return content
    context = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    return context

    pass


def generate_response(context, prompt):
    # create LLM chat obj
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        api_key=settings.gemini_api_key
    )
    # create system prompt
    system_prompt = f"""
    You are an AI assistant specializing in the World Anti-Doping Agency (WADA) Prohibited List.
    
    Answer the user's question using only the provided context.
    
    If the context contains the answer, provide a clear and concise response.
    If the context does not contain enough information to answer confidently, state that the information is not available in the provided context.
    
    Context:
    {context}
    Question:
    {prompt}
    """
    # send prompt to LLM API
    response = llm.invoke(system_prompt)
    # return response
    return {
        "Question": prompt,
        "Answer": response.text,
    }