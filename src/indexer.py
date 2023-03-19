import numpy as np
import pandas as pd
from opensearchpy import OpenSearch, NotFoundError
from config import NEWS_WITH_VECTORS_DATASET

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

    try:
        client.indices.delete(index="news-semantic-search")
    except NotFoundError:
        pass
    client.indices.create("news-semantic-search", body=body)

    for i, row in tqdm(df.iterrows()):
        client.index(
            index="news-semantic-search",
            body={
                "source_id": i,
                "title": row["title"],
                "description": row["description"],
                "embedding": [
                    float(x)
                    for x in row["vector"].replace("[", "").replace("]", "").split(",")
                ],
            },
        )

    client.indices.refresh(index="news-semantic-search")
    print("Done", client.cat.count(index="news-semantic-search", format="json"))


if __name__ == "__main__":
    main()
