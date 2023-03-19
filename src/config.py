import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA = Path(__file__).parent.parent / "data"
NEWS_DATASET = DATA / "news.csv"
NEWS_SAMPLE_DATASET = DATA / "news_sample.csv"
NEWS_WITH_VECTORS_DATASET = DATA / "news_sample_with_vectors.csv"

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
