
from sklearn.metrics.pairwise import cosine_similarity
import embedding
from chunk import Chunk


class Retriever:
    def __init__(self, embeddings,chunks):
        self.embeddings = embeddings
        self.chunks = chunks
        """
        Takes a user query embedding, calculates cosine similarity against
        stored records, and returns the top K most relevant text chunks.
        """

    def find_relevant_context(self, question_embedding, top_k: int = 3):

        if not question_embedding:
            return []

        scores = []

        # STEP 1: Loop through records and calculate cosine_similarity
        for embedding in self.embeddings:
            score = cosine_similarity(
            [question_embedding],
            [embedding.vector]
            )[0][0]
            scores.append((float(score), embedding.chunk_id)
        )

        # STEP 2: Sort top results
        top_chunks = sorted(
           scores,
           reverse=True
        )[:3]

        # STEP 3: Return top results texts
        chunk_map = {chunk.id: chunk for chunk in self.chunks}
        results = []
        for score, chunk_id in top_chunks:
            text = chunk_map[chunk_id].text
            document= chunk_map[chunk_id].source
            results.append((score, text,document))


        for score, text, document in results:
            print(score)
            print(text)
            print("-" * 50)

        return results