from app.logger import configure_logger
from app.ingestion.chunking.splitter import chunk_text


configure_logger()

articles = chunk_text()

for article in articles[:3]:
    print(article)


