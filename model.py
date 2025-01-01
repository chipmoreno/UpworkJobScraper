class SimpleMLModel:
    def __init__(self):
        # Placeholder for a "trained" model, using basic weights
        self.weights = {"budget": 0.5, "elapsed": -0.2, "experience_level": 1.0}

    def preprocess(self, job_data):
        """Convert job features into a numerical representation."""
        budget = float(job_data.get("budget", 0))
        elapsed_time = self.elapsed_to_seconds(job_data.get("elapsed", "00:00:00"))
        experience_level = self.encode_experience_level(job_data.get("experience_level", "Intermediate"))
        return [budget, elapsed_time, experience_level]

    def elapsed_to_seconds(self, elapsed):
        """Convert HH:MM:SS format to seconds."""
        h, m, s = map(int, elapsed.split(":"))
        return h * 3600 + m * 60 + s

    def encode_experience_level(self, level):
        """Encode experience level as a numerical value."""
        mapping = {"Intermediate": 1, "Expert": 2}
        return mapping.get(level, 1)

    def predict(self, job_data):
        """Simple prediction based on weighted sum of features."""
        features = self.preprocess(job_data)
        score = sum(f * w for f, w in zip(features, self.weights.values()))
        return "Apply" if score > 50 else "Skip"
