import os, httpx

def paper_exists(arxiv_id: str) -> bool:
    headers = {"x-api-key": os.environ["S2_API_KEY"]} if os.getenv("S2_API_KEY") else {}
    r = httpx.get(f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}",
                  params={"fields": "title"}, headers=headers, timeout=20)
    return r.status_code == 200