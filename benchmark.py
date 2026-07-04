import ollama

from pdf_reader import PDFReader

MODELS = [
    "nomic-embed-text",
#    "embeddinggemma",
    "all-minilm"
]



models = ollama.list()
#print (dir(type(models)))
#print (dir(models))
#print(models)

def inspect_embedding(model, text):
    response = ollama.embed(model=model, input=text)
    emb = response["embeddings"][0]

    load_ns = response.get("load_duration") or 0
    eval_ns = response.get("eval_duration")
    if eval_ns is None:
        eval_ns = response.get("prompt_eval_duration") or 0
    total_ns = response.get("total_duration") or 0

    load_ms = load_ns / 1_000_000
    eval_ms = eval_ns / 1_000_000
    total_ms = total_ns / 1_000_000

    print("#========================================")
    print("#Embedding Inspector")
    print("##========================================")
    print(f"#Model           : {response.get('model')}")
    print(f"#Dimensions      : {len(emb)}")
    print(f"#Prompt Tokens   : {response.get('prompt_eval_count', response.get('eval_count'))}")
    print(f"#Load Time       : {load_ms:.2f} ms")
    print(f"#Eval Time       : {eval_ms:.2f} ms")
    print(f"#Total Time      : {total_ms:.2f} ms")
    print(f"#First 5 Values  : {emb[:5]}")
    print(" ")


extractor = PDFReader("data/Employee-Handbook.pdf")
text = extractor.read()


for i, model in enumerate(MODELS):
    inspect_embedding(model, "The cat sat on the mats")
