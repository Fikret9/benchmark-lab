class RAGChatbot:
    def __init__(self, provider, retriever, llm_provider):
        self.provider = provider
        self.retriever = retriever
        self.llm_provider = llm_provider

    def ask(self, question):
        response = self.provider.embed([question])
        question_vector = response.embeddings[0]
        context = self.retriever.find_relevant_context(question_vector)


        prompt = f"""
        Answer only from the provided context.
        Context:
        {context}
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