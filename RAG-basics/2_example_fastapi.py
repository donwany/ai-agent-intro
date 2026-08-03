import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

DATABASE_URL = os.getenv("LAUKI_DATABASE_URL")

app = FastAPI(
    title="Lauki Phones RAG API",
    version="1.0.0",
)

#################################################
# Global objects
#################################################

llm = ChatOpenAI(model="gpt-4o-mini")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="lauki_faq",
    connection=DATABASE_URL,
    use_jsonb=True,
)

#################################################
# Request Models
#################################################

class QuestionRequest(BaseModel):
    question: str


#################################################
# Startup
#################################################

@app.on_event("startup")
def startup():

    df = pd.read_csv("lauki_qna.csv")

    documents = []

    for _, row in df.iterrows():

        documents.append(
            Document(
                page_content=f"""
Question:
{row["question"]}

Answer:
{row["answer"]}
""",
                metadata={
                    "question": row["question"],
                    "source": "lauki_qna.csv",
                },
            )
        )

    # Avoid duplicate inserts every restart
    existing = vectorstore.similarity_search(
        "SIM",
        k=1,
    )

    if len(existing) == 0:
        vectorstore.add_documents(documents)
        print(f"Inserted {len(documents)} documents.")
    else:
        print("Vector store already populated.")


#################################################
# Health Check
#################################################

@app.get("/")
def home():

    return {
        "message": "Lauki Phones RAG API"
    }


#################################################
# Search Endpoint
#################################################

@app.post("/search")
def search(request: QuestionRequest):

    results = vectorstore.similarity_search_with_score(
        request.question,
        k=3,
    )

    response = []

    for doc, distance in results:

        response.append(
            {
                "question": doc.metadata["question"],
                "answer": doc.page_content,
                "distance": float(distance),
                "similarity": round(1 - distance, 4),
            }
        )

    return response


#################################################
# Ask Endpoint (RAG)
#################################################

@app.post("/ask")
def ask(request: QuestionRequest):

    results = vectorstore.similarity_search_with_score(
        request.question,
        k=3,
    )

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail="No matching documents found.",
        )

    context = "\n\n".join(
        doc.page_content
        for doc, _ in results
    )

    prompt = f"""
You are a customer support assistant.

Answer ONLY from the supplied context.

If the answer is not in the context,
say you don't know.

Context:

{context}

Question:

{request.question}
"""

    answer = llm.invoke(prompt)

    sources = []

    for doc, distance in results:

        sources.append(
            {
                "question": doc.metadata["question"],
                "similarity": round(1 - distance, 4),
            }
        )

    return {
        "question": request.question,
        "answer": answer.content,
        "sources": sources,
    }