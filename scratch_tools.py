from src.tools.arxiv_tool import search_arxiv
from src.tools.pdf_tool import pdf_to_chunks
from src.tools import store
from src.tools.s2_tool import paper_exists

papers = search_arxiv("drone swarm search and rescue", 2)
print([p["title"] for p in papers])
for p in papers:
    chunks = pdf_to_chunks(p["pdf_url"], p["id"])
    print(p["id"], len(chunks), "chunks", "| exists:", paper_exists(p["id"]))
    store.add_chunks(chunks)

for hit in store.search("how do drones coordinate", k=3):
    print(hit["id"], "|", hit["text"][:150].replace("\n", " "))