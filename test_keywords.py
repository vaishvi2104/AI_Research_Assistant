from services.keyword_service import extract_keywords

text = """
Artificial Intelligence is transforming industries.
Machine Learning enables computers to learn from data.
Deep Learning uses neural networks.
Natural Language Processing helps computers understand human language.
"""

keywords = extract_keywords(text)

print("\n===== KEYWORDS =====\n")
print(keywords)