from typing import List
from app.ingestion.chunking.cleaner import clean_text
from app.constants import CLEANED_FILENAME
import logging
import re 

logger = logging.getLogger(__name__)


def parse_clauses(article_text: dict) -> List[dict]:

    clause_pattern = r"(?m)^\s*\((\d+)\)\s*"
    
    clauses = list(re.finditer(clause_pattern, article_text))


    structured_clauses = []

    for i, clause in enumerate(clauses):

        clause_number = int(clause.group(1))

        start = clause.end()

        if i + 1 < len(clauses):
            end = clauses[i + 1].start()
        else:
            end = len(article_text)

        clause_text = article_text[start:end].strip()

        
        structured_clauses.append({
            "clause_number": clause_number,
            "text": clause_text
        })

    return structured_clauses

def chunk_text() -> List[dict]:
    try:
        logger.info("Starting Constitution parsing")
        try:
            logger.info("Reading the file")
            
            with open(CLEANED_FILENAME,"r",encoding="UTF-8") as f:
                text = f.read()
            logger.info("File read!")
        except Exception as file_error:
            logger.exception("Error while reading the file ")
            
            
        documents = clean_text(text)
        logger.info(
                "Text cleaning completed (%d characters)",
                len(documents)
            )
        
        part_start = documents.find("Part-1")
        if part_start == -1:
            logger.error("Part-1 not found")
            return []
        
        article_text = documents[part_start:]
        article_pattern = r"(?ms)^(\d+)\.\s+(.+?):\s+"
        articles = list(re.finditer(article_pattern,article_text))
        
        if not articles:
                logger.error("No articles found in Constitution text")
                return []

        logger.info("Found %d articles", len(articles))
        
        structured_articles = []
        
        for i,article in enumerate(articles):
            article_number = int(article.group(1))
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
                rf"^{article_number}\.\s+{re.escape(article_title)}:\s*",
                "",
                article_content,
                count=1
            ).strip()
            
            clauses = parse_clauses(article_content)
            
            if not clauses:
                clauses = [
            {
                "clause_number": None,
                "text": article_content
            }
        ]

            structured_articles.append({
                "article_number": int(article_number),
                "article_title": article_title,
                "clauses": clauses
            })
            
            logger.debug(
                    "Parsed Article %d: '%s' (%d clauses)",
                    article_number,
                    article_title,
                    len(clauses)
                )
            
            logger.info(
                "Constitution parsing completed successfully: %d articles",
                len(structured_articles)
            )

        return structured_articles

    except Exception:
        logger.exception("Unexpected error during Constitution parsing")
        return []

