import spacy

_nlp = None


def get_nlp_model():
    """
    Lazy loader for spaCy NER model with parser and tagger disabled for 10x faster execution.
    """
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm", disable=["parser", "tagger", "lemmatizer"])
    return _nlp


def extract_entities(text):
    if not text or len(text.strip()) < 10:
        return []

    try:
        nlp_model = get_nlp_model()
        # Limit text length to first 12,000 characters for sub-second processing
        doc = nlp_model(text[:12000])

        entities = []
        seen = set()

        # Prioritize informative entity types (Organizations, People, Tech, Locations)
        relevant_labels = {
            "ORG", "PERSON", "GPE", "PRODUCT", "EVENT",
            "WORK_OF_ART", "LAW", "NORP", "FAC"
        }

        for ent in doc.ents:
            cleaned_text = ent.text.strip()
            if (
                cleaned_text
                and len(cleaned_text) > 1
                and cleaned_text.lower() not in seen
                and ent.label_ in relevant_labels
            ):
                seen.add(cleaned_text.lower())
                entities.append({
                    "text": cleaned_text,
                    "label": ent.label_
                })

        return entities[:30]
    except Exception as e:
        print(f"Warning in NER extraction: {e}")
        return []