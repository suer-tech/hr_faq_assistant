from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)
from datasets import Dataset

def evaluate_response(query: str, answer: str, contexts: list):
    data = {
        "question": [query],
        "answer": [answer],
        "contexts": [contexts],
        "ground_truth": ["placeholder"]
    }
    dataset = Dataset.from_dict(data)

    score = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_recall, context_precision]
    )
    return score.to_pandas().iloc[0].to_dict()