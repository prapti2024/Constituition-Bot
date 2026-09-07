
import logging
from pypdf import PdfReader


logger = logging.getLogger(__name__)

def parse_pdf(file_path:str)-> str:
    
    logger.info("PDF Parsing %s",file_path)
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        logger.info("Total number of pages %d",total_pages)
       
        text_parts: list[str] = []
        blank_pages:list[int] = []
       
        for i,page in enumerate(reader.pages):
           text = page.extract_text() or ""
           if text.strip():
                text_parts.append(text)
           else:
               blank_pages.append(i+1)
               
        if blank_pages:      
            logger.info(f"pypdf returned blank pages on pages:{len(blank_pages)}. Retrying again with pdfplumber.")
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for page_num in blank_pages:
                        page = pdf.pages[page_num - 1]
                        fallback_text = page.extract_text() or ""
                        if fallback_text.strip():
                            text_parts.append(fallback_text)
    
            except Exception as plumber_err:
                    logger.warning(f"Plumber Fallback failed:{plumber_err}")
               

        full_text= "\n".join(text_parts)
                
        if not full_text.strip():
            logger.info("Nothing is extracted via pdfplumber")
        else:
            logger.info(f"Extracted {len(full_text)} characters from {file_path}.")
            
        return full_text

    except Exception as e:
        logger.exception("Text Parsing Failed:%s", file_path)
        raise