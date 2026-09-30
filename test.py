from dotenv import load_dotenv
load_dotenv()
import langgraph, chromadb, pymupdf, arxiv, pydantic
print("imports OK")

from langchain_google_genai import GoogleGenerativeAIEmbeddings
emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("embedding dim:", len(emb.embed_query("hello")))

from langchain.chat_models import init_chat_model
llm = init_chat_model("google_genai:gemini-3.8-flash", temperature=0)
print(llm.invoke("Reply with the word OK").content)