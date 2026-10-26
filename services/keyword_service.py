import os
from keybert import KeyBERT

_kw_model = None


def get_keyword_model():
    """
    Lazy loader for KeyBERT.
    """
    global _kw_model
    if _kw_model is None:
        try:
            _kw_model = KeyBERT(model="all-MiniLM-L6-v2")
        except Exception:
            _kw_model = KeyBERT()
    return _kw_model


def extract_keywords(text):
    if not text or len(text.strip()) < 50:
        return ""

    try:
        model = get_keyword_model()
        # Focus on first 1500 characters for high-speed, relevant concept extraction
        sample_text = text[:1500]
        keywords = model.extract_keywords(
            sample_text,
            keyphrase_ngram_range=(1, 2),
            stop_words="english",
            top_n=8
        )

        keyword_list = [kw for kw, _ in keywords]
        return ", ".join(keyword_list)
    except Exception as e:
        print(f"Warning in keyword extraction: {e}")
        return ""