import ollama

from chunker import Chunker
from pdf_reader import PDFReader

extractor = PDFReader("data/Employee-Handbook.pdf")
doc = extractor.read()

print(doc.source)
print(doc.page_count)

chunker = Chunker()
chunks = chunker.chunk(doc)
print(len(chunks[0].text.split()))
print(len(chunks[1].text.split()))
print(len(chunks[-1].text.split()))