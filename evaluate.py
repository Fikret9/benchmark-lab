import os


def evaluate(test_cases, provider,retriever):
    passed = 0
    failed = 0
    failures = []
    for test in test_cases:
        """    Create Vector for the query """
        response = provider.embed(test["question"])
        question_vector = response.embeddings[0]

        results = retriever.find_relevant_context(question_vector)
        print(test["question"])
        print(results)

        document_match = False
        answer_match = False

        for score, text, document in results:
            print(repr(document))
            print(repr(test["expected_document"]))


            if os.path.normpath(document) == os.path.normpath(test["expected_document"]):
               document_match = True
               print(f"Document match: {document_match}")

            if test["expected_contains"] in text:
               answer_match = True
               print(f"Answer match: {answer_match}")

            print(f"Expected: {repr(test['expected_contains'])}")
            print(f"Text contains? {test['expected_contains'] in text}")



        if document_match and answer_match:
           passed +=1
           print(
                 f"PASS\n"
                 f"Question: {test['question']}\n"
                 f"Retrieved: {document}\n"
                )
        else:
          failed +=1
          print(
                f"FAIL\n"
                f"Expected: {test['expected_document']}\n"
                f"Retrieved: {document}\n\n"
            )

    total = passed + failed
    accuracy = (passed / total * 100) if total else 0

    print("=" * 21)
    print("Evaluation Summary")
    print("=" * 21)
    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Accuracy: {accuracy:.1f}%")
    print()
    print("Failures:")
    print()

    for item in failures:
        print(f"- {item}")