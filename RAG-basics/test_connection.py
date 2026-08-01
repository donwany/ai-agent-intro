from sqlalchemy import create_engine
import os

DATABASE_URL="postgresql+psycopg://postgres:password@localhost:5432/rag_demo"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Connected successfully!")