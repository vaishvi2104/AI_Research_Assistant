import os
import fitz


def get_statistics(file_path, text):
    """
    Computes page count, word count, and estimated reading time.
    """
    words = text.split() if text else []
    word_count = len(words)
    reading_time = max(1, round(word_count / 200))  # 200 words per min

    page_count = 1
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf" and os.path.exists(file_path):
        try:
            doc = fitz.open(file_path)
            page_count = len(doc)
            doc.close()
        except Exception:
            page_count = max(1, round(word_count / 500))
    else:
        # For txt/md files, estimate pages at ~500 words per academic page
        page_count = max(1, round(word_count / 500))

    return {
        "page_count": page_count,
        "word_count": word_count,
        "reading_time": reading_time
    }