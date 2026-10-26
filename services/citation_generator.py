import re
from datetime import datetime


def extract_paper_metadata(text, filename="Paper"):
    """
    Extracts title, authors, year, and reference list from raw document text.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()] if text else []
    
    # 1. Title Extraction
    title = filename.rsplit(".", 1)[0].replace("_", " ").replace("-", " ").title()
    if lines:
        for line in lines[:5]:
            # Look for a clean line that looks like a title
            if 10 < len(line) < 160 and not line.lower().startswith(("http", "doi", "issn", "volume", "page", "arxiv", "accepted")):
                title = line
                break

    # 2. Year Extraction
    current_year = str(datetime.now().year)
    year = current_year
    year_match = re.search(r'\b(19\d\d|20[0-2]\d)\b', text[:2000] if text else "")
    if year_match:
        year = year_match.group(1)

    # 3. Authors Extraction
    authors = "Unknown Authors"
    # Look for author indicators
    author_line_match = re.search(r'(?:Authors?|By)[:\s]+([^\n\r]+)', text[:2500] if text else "", re.IGNORECASE)
    if author_line_match:
        authors = author_line_match.group(1).strip()
    elif len(lines) >= 3:
        # Often line 2 or 3 in academic papers contains author names
        for line in lines[1:4]:
            if any(c in line for c in [",", "and", "&"]) and len(line) < 140 and not any(k in line.lower() for k in ["university", "department", "abstract", "email", "@", "doi"]):
                authors = line
                break

    # 4. Extract References Section
    references = []
    ref_pattern = re.compile(r'(?:\n|\r\n)(?:References|Bibliography|REFERENCES|BIBLIOGRAPHY)\s*[\n\r]+([\s\S]+)', re.IGNORECASE)
    ref_match = ref_pattern.search(text) if text else None
    
    if ref_match:
        ref_text_block = ref_match.group(1).strip()
        # Split by reference markers like [1], (1), 1., or double newlines
        raw_refs = re.split(r'(?:\n\s*\[\d+\]|\n\s*\d+\.|\n\n+)', ref_text_block)
        for r in raw_refs:
            cleaned = " ".join(r.split()).strip()
            if len(cleaned) > 25:
                references.append(cleaned)
    
    # Limit references to top 25
    references = references[:25]
    
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "references": references
    }


def generate_citations(title, authors="Unknown Authors", year="2026", journal="AI Research Assistant Repository"):
    """
    Generates standard academic citations in BibTeX, APA 7, IEEE, and MLA 9 formats.
    """
    title = title.strip()
    authors = authors.strip() if authors else "Unknown Authors"
    year = str(year).strip() if year else "2026"
    
    # First Author Key for BibTeX
    first_author_token = re.sub(r'[^a-zA-Z]', '', authors.split(',')[0].split(' and ')[0].split()[-1] if authors.split() else "author").lower()
    bibtex_key = f"{first_author_token}{year}{re.sub(r'[^a-zA-Z]', '', title)[:8].lower()}"

    # BibTeX
    bibtex = f"""@article{{{bibtex_key},
  title = {{{title}}},
  author = {{{authors}}},
  year = {{{year}}},
  journal = {{{journal}}},
  note = {{Indexed via AI Research Assistant}}
}}"""

    # APA 7th Edition: Author, A. A. (Year). Title. Journal.
    apa = f"{authors} ({year}). {title}. {journal}."

    # IEEE: [1] A. A. Author, "Title," Journal, Year.
    ieee = f'[1] {authors}, "{title}," {journal}, {year}.'

    # MLA 9th Edition: Author. "Title." Journal, Year.
    mla = f'{authors}. "{title}." {journal}, {year}.'

    return {
        "bibtex": bibtex,
        "apa": apa,
        "ieee": ieee,
        "mla": mla
    }
