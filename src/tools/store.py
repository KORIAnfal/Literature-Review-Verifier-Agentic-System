import time
import chromadb
from langchain_google_genai import GoogleGenerativeAIEmbeddings

_emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
_col = chromadb.PersistentClient("./db").get_or_create_collection(
    "chunks", embedding_function=None)          # we supply embeddings ourselves

def _embed_docs(texts, batch=50):
    out = []
    for i in range(0, len(texts), batch):
        for attempt in range(5):                # retry on free-tier rate limits
            try:
                out += _emb.embed_documents(texts[i:i + batch])
                break
            except Exception:
                time.sleep(2 ** attempt)
        else:
            raise RuntimeError("embedding failed after retries")
        time.sleep(1)
    return out

def add_chunks(chunks):
    if not chunks:
        return
    texts = [c["text"] for c in chunks]
    _col.upsert(ids=[c["id"] for c in chunks],
                documents=texts,
                embeddings=_embed_docs(texts),
                metadatas=[{"paper_id": c["paper_id"], "page": c["page"]} for c in chunks])

def search(query, k=12, paper_ids=None):
    where = {"paper_id": {"$in": paper_ids}} if paper_ids else None
    r = _col.query(query_embeddings=[_emb.embed_query(query)], n_results=k, where=where)
    return [{"id": i, "text": t, "paper_id": m["paper_id"], "page": m["page"]}
            for i, t, m in zip(r["ids"][0], r["documents"][0], r["metadatas"][0])]

def get_text(chunk_ids):
    return "\n".join(_col.get(ids=chunk_ids)["documents"]) if chunk_ids else ""

def existing_ids(chunk_ids):
    return set(_col.get(ids=chunk_ids)["ids"]) if chunk_ids else set()