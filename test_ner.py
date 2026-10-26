from services.ner_service import extract_entities

text = """
Google developed BERT.
Researchers from Stanford University created many AI models.
The research was conducted in California.
"""

entities = extract_entities(text)

for entity in entities:
    print(entity)