test_cases = [
    {
        "question": "What is the doctor visit copayment?",
        "expected_document": "data/Student-Healthcare.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "What are vacation policies?",
        "expected_document": "data/Employee-Handbook.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "What dental services are covered?",
        "expected_document": "data/Student-Healthcare.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "What is the doctor copayment?",
        "expected_document": "data/Employee-Handbook.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "How many vacation days are allowed?",
        "expected_document": "data/Employee-Handbook.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "What's the limit?",
        "expected_document": "data/Employee-Handbook.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "What is the dental coverage?",
        "expected_document": "data/Student-Healthcare.pdf",
        "minimum_score": 0.60
    },
    {
        "question": "What is the capital of France?",
        "expected_document": "out_of_domain",
        "minimum_score": 0.00
    },
    {
        "question": "Insurance",
        "expected_document": "data/Student-Healthcare.pdf",
        "minimum_score": 0.50
    }
]