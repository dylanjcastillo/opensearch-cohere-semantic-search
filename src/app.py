import cohere
from fastapi import FastAPI

from config import (
    COHERE_API_KEY,
    NEWS_WITH_VECTORS_DATASET,
)

from opensearchpy import OpenSearch


app = FastAPI()

opensearch_client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "admin"),
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)

cohere_client = cohere.Client(COHERE_API_KEY)


@app.get("/")
def read_root():
    return {"message": "Make a post request to /search to search through news articles"}


@app.post("/ask")
def ask(query: str):
    query_embedding = cohere_client.embed(texts=[query], model="small").embeddings[0]

    open

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=250,
        temperature=0.2,
    )

    return {
        "response": response["choices"][0]["message"]["content"],
        "references": references,
    }
