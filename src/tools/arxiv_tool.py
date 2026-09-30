import arxiv

def search_arxiv(query: str, n: int = 4) -> list[dict]:
    res = arxiv.Client().results(arxiv.Search(query=query, max_results=n))
    return [{"id": r.get_short_id().split("v")[0], "title": r.title,
             "pdf_url": r.pdf_url, "year": r.published.year} for r in res]