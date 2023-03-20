import cohere
from fastapi import FastAPI

from config import COHERE_API_KEY, INDEX_NAME

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


@app.post("/search")
def ask(query: str):
    query_embedding = cohere_client.embed(texts=[query], model="small").embeddings[0]

    similar_news = opensearch_client.search(
        index=INDEX_NAME,
        body={
            "query": {"knn": {"embedding": {"vector": query_embedding, "k": 10}}},
        },
    )
    response = [
        {"title": r["_source"]["title"], "description": r["_source"]["description"]}
        for r in similar_news["hits"]["hits"]
    ]

    return {
        "response": response,
    }
