import fitz

from services.pdf_service import extract_text
from services.statistics_service import get_statistics

pdf = "uploads/AML_NOTES_UNIT2.pdf"

text = extract_text(pdf)

stats = get_statistics(pdf, text)

print(stats)