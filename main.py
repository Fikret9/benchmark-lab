
from chunk import Chunk

import embedding
from RAGChatbot import RAGChatbot
from chunker import Chunker
from evaluate import evaluate
from ollama_embedding_provider import OllamaEmbeddingProvider
from ollama_llm_provider import OllamaLLMProvider
from pdf_reader import PDFReader
from record_store import RecordStore
from retriever import Retriever
from build_embeddings import build_embeddings
from test_cases import test_cases



"""    Read PDF Document     """
extractor = PDFReader("data/Employee-Handbook.pdf")
doc = extractor.read()
print(f"source: {doc.source} .. {doc.page_count} pages")

#model_id = "all-minilm"
model_id = "nomic-embed-text"
provider = OllamaEmbeddingProvider(model_id)


chunk_store = RecordStore(Chunk, "chunks.json")
if chunk_store.exists():
    chunks = chunk_store.load()
    print(f"Loaded {len(chunks)} records from cache")
else:
    chunker = Chunker()
    chunks = chunker.chunk(doc)
    chunk_store.save(chunks)

embeddings_store = RecordStore(embedding.Embedding, "embeddings.json")
if embeddings_store.exists():
    embeddings = embeddings_store.load()
    print(f"Loaded {len(embeddings)} embedding records from cache")
else:
    texts = [chunk.text for chunk in chunks]
    """    Create embeddings from Vectors """
    response = provider.embed(texts)
    embeddings: list[embedding.Embedding] = []
    embeddings = build_embeddings(chunks, response.embeddings, model_id) #"""    Build embeddings """
    embeddings_store.save(embeddings)

"""    Create Vector for the query """
response = provider.embed([" vacation policy"])
question_vector = response.embeddings[0] 

"""    Retrieve top results """
retriever = Retriever(embeddings,chunks)
results = retriever.find_relevant_context(question_vector)
print("------------------------------------------------------------")
print(results)

"""    Test a batch """
evaluate(test_cases, provider,retriever)

"""    Ask LLM """
chat_model="qwen2.5:1.5b"
llm_provider = OllamaLLMProvider(chat_model)
bot = RAGChatbot(provider=provider, retriever=retriever, llm_provider=llm_provider)
bot.chat_loop()


