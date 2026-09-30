import pymupdf, httpx, hashlib, pathlib
from src.config import CFG

CACHE = pathlib.Path("cache"); CACHE.mkdir(exist_ok=True)

def pdf_to_chunks(pdf_url: str, paper_id: str) -> list[dict]:
    f = CACHE / (hashlib.md5(pdf_url.encode()).hexdigest() + ".pdf")
    try:
        if not f.exists():
            f.write_bytes(httpx.get(pdf_url, follow_redirects=True, timeout=60).content)
        doc = pymupdf.open(f)
    except Exception:
        return []
    size, ov = CFG["chunk_size"], CFG["chunk_overlap"]
    chunks = []
    for pno, page in enumerate(doc, start=1):
        text = page.get_text()
        for i in range(0, len(text), size - ov):
            piece = text[i:i + size].strip()
            if len(piece) > 100:
                chunks.append({"id": f"{paper_id}_p{pno}_{i}", "paper_id": paper_id,
                               "page": pno, "text": piece})
    return chunks