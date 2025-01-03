# evaluate_accuracy.py
class AccuracyEvaluator:
    def evaluate(self, predictions, ground_truth):
        correct = sum(predictions.get(job_id) == ground_truth.get(job_id) for job_id in ground_truth)
        return correct / len(ground_truth) if ground_truth else 0
