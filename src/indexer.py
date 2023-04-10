import pandas as pd
from opensearchpy import OpenSearch, NotFoundError
from config import NEWS_WITH_VECTORS_DATASET, INDEX_NAME

from tqdm import tqdm


def main():
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "admin"),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    df = pd.read_csv(NEWS_WITH_VECTORS_DATASET)

    body = {
        "settings": {
            "index": {"knn": True},
        },
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "keyword"},
                "content": {"type": "keyword"},
                "description": {"type": "keyword"},
                "embedding": {"type": "knn_vector", "dimension": 1024},
            }
        },
    }

    try:
        client.indices.delete(index=INDEX_NAME)
    except NotFoundError:
        pass
    client.indices.create(INDEX_NAME, body=body)

    for i, row in tqdm(df.iterrows(), total=len(df)):
        embedding = [
            float(x) for x in row["vector"].replace("[", "").replace("]", "").split(",")
        ]
        client.index(
            index=INDEX_NAME,
            body={
                "id": i,
                "title": row["title"],
                "content": row["content"],
                "description": row["description"],
                "embedding": embedding,
            },
        )

    client.indices.refresh(index=INDEX_NAME)
    print("Done", client.cat.count(index=INDEX_NAME, format="json"))


if __name__ == "__main__":
    main()
