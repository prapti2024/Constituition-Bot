from typing import List
from app.ingestion.chunking.cleaner import clean_text
from app.constants import CLEANED_FILENAME
import logging
import re 

logger = logging.getLogger(__name__)

def chunk_text():
            #    .txt file too 
            #    parent_size:int = 1500, 
            #    child_size:int = 400, 
            #    child_overlap:int = 50) -> List:
    
    try:
        logger.info("Reading the file")
        
        with open(CLEANED_FILENAME,"r",encoding="UTF-8") as f:
             text = f.read()
        logger.info("File read!")
    except Exception as file_error:
        logger.exception("Error while reading the file ")
        
    documents = clean_text(text)
    part_start = documents.find("Part-1")
    
    
    if part_start == -1:
        logger.error("Part-1 not found")
        return []
    
    article_text = documents[part_start:]
    article_pattern = r"(?ms)^(\d+)\.\s+(.+?):\s+"
    articles = list(re.finditer(article_pattern,article_text))
    
    structured_articles = []
    
    for i,article in enumerate(articles):
        article_number = article.group(1)
        article_title = article.group(2).strip()
        
         # Start of this article
        start = article.start()

        # End of this article = start of next article
        if i + 1 < len(articles):
            end = articles[i + 1].start()
        else:
            end = len(article_text)

        # Everything belonging to this article
        article_content = article_text[start:end].strip()
        
        article_content = re.sub(
            rf"^{re.escape(article_number)}\.\s+{re.escape(article_title)}:\s*",
            "",
            article_content,
            count=1
        ).strip()

        structured_articles.append({
            "article_number": int(article_number),
            "article_title": article_title,
            "text": article_content
        })

    return structured_articles