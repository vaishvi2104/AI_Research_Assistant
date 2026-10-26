import os
import fitz


def extract_text(file_path):
    """
    Extracts text from PDF, TXT, or Markdown files.
    """
    if not os.path.exists(file_path):
        return ""

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        try:
            document = fitz.open(file_path)
            full_text = []
            for page in document:
                full_text.append(page.get_text())
            document.close()
            return "\n".join(full_text)
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""

    elif ext in [".txt", ".md"]:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return ""

    return ""