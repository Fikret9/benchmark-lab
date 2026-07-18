import os

from DocumentMetadataStore import DocumentMetadataStore
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

metadata_store = DocumentMetadataStore()
metadata_store.load()
model_id = "nomic-embed-text"
provider = OllamaEmbeddingProvider(model_id)
all_chunks =[]
all_embeddings = []

for file_path in os.listdir("data"):
    full_path = os.path.join("data", file_path)
    filename = file_path
    sha256, last_modified = DocumentMetadataStore.compute_file_info(full_path)
    chunk_file = f"cache/chunks/{filename}.json"
    chunk_file = chunk_file.replace(".pdf", "")
    embedding_file = f"cache/embeddings/{model_id}/{filename}.json"
    embedding_file = embedding_file.replace(".pdf","")

    chunk_store = RecordStore(Chunk, chunk_file)
    embedding_store = RecordStore(embedding.Embedding, embedding_file)


    if filename not in metadata_store.data:
        extractor = PDFReader(full_path)
        doc = extractor.read()
        """    Create chunks """
        chunker = Chunker()
        chunks = chunker.chunk(doc)
        chunk_store.save(chunks)
        metadata_store.update_document(filename,sha256,last_modified)
        texts = [chunk.text for chunk in chunks]
        """    Create embeddings from Vectors """
        response = provider.embed(texts)
        embeddings: list[embedding.Embedding] = []
        embeddings = build_embeddings(chunks, response.embeddings, model_id) #"""    Build embeddings """
        embedding_store.save(embeddings)
        metadata_store.add_embedding_model(filename,model_id)
        metadata_store.save()
        all_chunks.extend(chunks)
        all_embeddings.extend(embeddings)
    elif metadata_store.has_changed(filename, sha256):
        print ("Store changed")
    else:
        print ("Store unchanged")
        all_chunks.extend(chunk_store.load())
        all_embeddings.extend(embedding_store.load())



"""    Create Vector for the query """
response = provider.embed([" vacation policy"])
question_vector = response.embeddings[0] 

"""    Retrieve top results """
retriever = Retriever(all_embeddings,all_chunks)

print(len(all_chunks))
print(len(all_embeddings))


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


