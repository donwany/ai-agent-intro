import pandas as pd
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_postgres import PGVector


load_dotenv(".env")
LAUKI_DATABASE_URL = os.getenv("LAUKI_DATABASE_URL")


llm = ChatOpenAI(model="gpt-4o-mini")

# Load the CSV
df = pd.read_csv("lauki_qna.csv")

documents = []
for _, row in df.iterrows():
    documents.append(
        Document(
            page_content=f"""
            Question:
            {row['question']}

            Answer:
            {row['answer']}
        """,
            metadata={
                "source": "lauki_faq.csv",
                "question": row["question"],
            },
        )
    )

print(f"Loaded {len(documents)} documents.")

#########################################
# 2. Create embeddings
#########################################
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

#################################################
# 4. PGVector
#################################################

# Add the document chunks to the "vector store" using OpenAIEmbeddings
# vectorstore = InMemoryVectorStore.from_documents(
#     documents=chunks,
#     embedding=OpenAIEmbeddings(),
# )

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="lauki_faq",
    connection=LAUKI_DATABASE_URL,
    use_jsonb=True,
)

#################################################
# 5. Insert documents
#################################################
vectorstore.add_documents(documents)
print("Documents stored!")


if __name__ == "__main__":

    query = "Can I convert my SIM into an eSIM?"

    results = vectorstore.similarity_search_with_score(query=query, k=3,)
    # Cosine distance
    for doc, score in results:
        print("=" * 60)
        print(f"Cosine Distance: {score:.4f}")
        print(doc.page_content)
        # Convert Distance to Similarity
        similarity = 1 - score
        print(f"Similarity: {similarity:.2%}")
        print(doc.metadata["question"])


    context = "\n\n".join(doc.page_content for doc, _ in results)

    prompt = f"""
    You are a customer support assistant.

    Answer the question using only the provided context.

    Context:
    {context}

    Question:
    {query}
    """

    response = llm.invoke(prompt)

    print("\nAnswer:\n")
    print(response.content)