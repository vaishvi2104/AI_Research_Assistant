import re
import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


def extract_arxiv_id(query):
    """
    Extracts clean arXiv identifier from a raw query, URL, or identifier string.
    Examples:
      - 1706.03762 -> 1706.03762
      - arxiv:1706.03762v5 -> 1706.03762
      - https://arxiv.org/abs/1706.03762 -> 1706.03762
      - https://arxiv.org/pdf/1706.03762.pdf -> 1706.03762
    """
    if not query:
        return None
    query = query.strip()
    match = re.search(r'(\d{4}\.\d{4,5})(?:v\d+)?', query)
    if match:
        return match.group(1)
    return None


def fetch_arxiv_metadata_and_pdf(arxiv_id_or_url, upload_folder):
    """
    Fetches official paper metadata from arXiv API and downloads the PDF directly.
    """
    arxiv_id = extract_arxiv_id(arxiv_id_or_url)
    if not arxiv_id:
        return None, "Invalid arXiv identifier or URL. Example format: 1706.03762 or https://arxiv.org/abs/1706.03762"

    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    
    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "AI-Research-Assistant/2.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read().decode('utf-8')

        root = ET.fromstring(xml_data)
        atom_ns = "{http://www.w3.org/2005/Atom}"
        entry = root.find(f"{atom_ns}entry")

        if entry is None:
            return None, f"Could not find arXiv publication with ID: {arxiv_id}"

        title_elem = entry.find(f"{atom_ns}title")
        summary_elem = entry.find(f"{atom_ns}summary")
        published_elem = entry.find(f"{atom_ns}published")

        title = " ".join(title_elem.text.split()) if title_elem is not None and title_elem.text else f"arXiv Paper {arxiv_id}"
        summary = " ".join(summary_elem.text.split()) if summary_elem is not None and summary_elem.text else ""
        published = published_elem.text[:10] if published_elem is not None and published_elem.text else "2026"
        year = published[:4] if published else "2026"

        authors = []
        for author_elem in entry.findall(f"{atom_ns}author"):
            name_elem = author_elem.find(f"{atom_ns}name")
            if name_elem is not None and name_elem.text:
                authors.append(name_elem.text.strip())
        authors_str = ", ".join(authors) if authors else "Unknown Authors"

        # Download official PDF
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        safe_title = re.sub(r'[^a-zA-Z0-9_\- ]', '', title)[:40].strip().replace(" ", "_")
        filename = f"arxiv_{arxiv_id}_{safe_title}.pdf"
        save_path = os.path.join(upload_folder, filename)

        pdf_req = urllib.request.Request(
            pdf_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(pdf_req, timeout=20) as pdf_resp:
            with open(save_path, "wb") as f:
                f.write(pdf_resp.read())

        return {
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors_str,
            "year": year,
            "abstract": summary,
            "filename": filename,
            "save_path": save_path
        }, None

    except Exception as e:
        print(f"Error fetching arXiv paper: {e}")
        return None, f"Failed to download arXiv paper ({arxiv_id}): {str(e)}"
