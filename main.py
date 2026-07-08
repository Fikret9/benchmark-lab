import embedding
from chunker import Chunker
from ollama_embedding_provider import OllamaEmbeddingProvider
from pdf_reader import PDFReader
from retriever import Retriever
from build_embeddings import build_embeddings

def embed_query(provider, query: str):
    response = provider.embed([query])
    return response.embeddings[0]

"""    Read PDF Document     """
extractor = PDFReader("data/Employee-Handbook.pdf")
doc = extractor.read()
print(f"source: {doc.source} .. {doc.page_count} pages")

"""    Chunk the document    """
chunker = Chunker()
chunks = chunker.chunk(doc)

"""    Create Vectors """
model_id = "all-minilm"
provider = OllamaEmbeddingProvider(model_id)
texts = [chunk.text for chunk in chunks]

"""    Create embeddings from Vectors """
response = provider.embed(texts)
embeddings: list[embedding.Embedding] = []

"""    Build embeddings """
embeddings = build_embeddings(chunks, response.embeddings, model_id)

"""    Create Vector for the query """
response = provider.embed([" vacation policy"])
question_vector = response.embeddings[0] 

"""    Retrieve top results """
retriever = Retriever(embeddings,chunks)
results = retriever.find_relevant_context(question_vector)
print(results)


