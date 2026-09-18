import re 
def clean_text(text: str)->str:  
    junk_pattern = r"www\.lawcommission\.g\s*ov\.np\s*\n\s*\d+"
    cleaned_text = re.sub(junk_pattern, "", text)
    return cleaned_text