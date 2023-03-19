import pandas as pd
from opensearchpy import OpenSearch, NotFoundError
from config import NEWS_DATASET


def main():
    client = OpenSearch(
        hosts=[{"host": "localhost", "port": 9200}],
        http_auth=("admin", "admin"),
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
    )

    df = (
        pd.read_csv(NEWS_DATASET, index_col=0)
        .dropna()
        .sample(1000, random_state=42)
        .reset_index(drop=True)
    )

    body = {
        "settings": {
            "index": {"knn": True, "knn.algo_param.ef_search": 100},
        },
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "keyword"},
                "description": {"type": "text"},
                "embedding": {"type": "knn_vector", "dimension": 1024},
            }
        },
    }

    for i, row in df.iterrows():
        client.index(
            index="news",
            body={
                "source_id": i,
                "title": row["title"],
                "description": row["description"],
                "embedding": [
                    float(x)
                    for x in row["vector"].replace("[", "").replace("]", "").split()
                ],
            },
        )

    try:
        client.indices.delete(index="news-semantic-search")
    except NotFoundError:
        pass
    client.indices.create("news-semantic-search", body=body)

    client.indices.refresh(index="news-semantic-search")
    print("Done", client.cat.count(index="news-semantic-search", format="json"))


if __name__ == "__main__":
    main()
