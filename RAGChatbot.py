class RAGChatbot:
    def __init__(self, provider, retriever, llm_provider):
        self.provider = provider
        self.retriever = retriever
        self.llm_provider = llm_provider

    def ask(self, question):
        response = self.provider.embed([question])
        question_vector = response.embeddings[0]
        context = self.retriever.find_relevant_context(question_vector)
        print("context")
        parts = []

        for score, text, source in context:
            parts.append(f"Source: {source}\n{text}")

        context_text = "\n\n---\n\n".join(parts)

        prompt = f"""
        You are answering questions about company documents.
        Use ONLY the information in the context below.

        If the answer is not explicitly contained in the context, reply exactly:
        "I don't know."
        
        Context:
        {context_text}
        Question:
        {question}
        If the answer is not in the context, say you don't know.
        """

        return self.llm_provider.generate(prompt)


    def chat_loop(self):
        while True:
            question = input("Enter your question (or type 'quit'): ").strip()
            if question.lower() == "quit":
                break
            print(self.ask(question))