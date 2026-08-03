## Vector Databases
- Pinecone
- Weaviate
- Qdrant
- FAISS
- ChromaDB
- MongoDB
- PGVector from PostGreSQL

## Workflow
```
                  PDF
                   │
                   ▼
            PyPDFLoader
                   │
                   ▼
      RecursiveCharacterTextSplitter
                   │
                   ▼
             Text Chunks
                   │
                   ▼
     OpenAI Embeddings (1536 dimensions)
                   │
                   ▼
           PostgreSQL + pgvector
           (stores vectors + metadata)
                   │
          User asks a question
                   │
                   ▼
     Embed the user question
                   │
                   ▼
      Similarity Search (Cosine/L2)
                   │
                   ▼
        Top 3 Relevant Chunks
                   │
                   ▼
              GPT-4o-mini
                   │
                   ▼
              Final Answer
```


## Create a database
```bash
docker exec -it pgvector-db psql -U postgres

CREATE DATABASE rag_demo;
CREATE DATABASE lauki_demo;

# connect to it
\c rag_demo

# enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

docker compose up -d

docker exec -it pgvector-db psql -U postgres -d rag_demo
docker exec -it pgvector-db psql -U postgres -c "\l"

\dx

docker compose down
```

## Typical PGVector Table
```
| id | document                              | embedding      | metadata     |
| -- | ------------------------------------- | -------------- | ------------ |
| 1  | Employees receive 20 vacation days... | `[0.123, ...]` | `{"page":1}` |
| 2  | Employees may work remotely...        | `[0.442, ...]` | `{"page":1}` |
```

## Lauki Demo
```
                lauki_faq.csv
                      │
                      ▼
                 pandas.read_csv()
                      │
                      ▼
              LangChain Documents
                      │
                      ▼
               OpenAI Embeddings
                      │
                      ▼
          PostgreSQL + pgvector
                      │
                      ▼
      similarity_search_with_score()
                      │
                      ▼
      Top-K FAQ Entries + Similarity
                      │
                      ▼
                GPT-4o-mini
                      │
                      ▼
             Final Customer Answer
```