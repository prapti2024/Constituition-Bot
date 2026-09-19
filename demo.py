from app.logger import configure_logger
from app.ingestion.chunking.splitter import chunk_text,parse_clauses


configure_logger()
articles = chunk_text()


print(articles[:10])


