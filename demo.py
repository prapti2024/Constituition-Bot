from app.ingestion.loaders.pdfparser import parse_pdf
from app.logger import configure_logger

configure_logger()


file_path ="D:/Constituition-Bot/DATA/valid_data/constituition.pdf"

text = parse_pdf(file_path)

output_path = "D:/Constituition-Bot/DATA/valid_data/constitution_raw.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(text)

print("\n========== EXTRACTED TEXT ==========\n")
print(text[:200])

print("\n========== SUMMARY ==========\n")
print(f"Characters extracted: {len(text)}")
print(f"Words extracted: {len(text.split())}")

