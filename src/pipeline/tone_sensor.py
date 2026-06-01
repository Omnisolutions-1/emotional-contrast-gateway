import re
import math
from typing import List

class ToneMatrixSensor:
    def __init__(self):
        self.mock_matrix = {
            "joy":     [0.10, 0.15, 0.05],
            "grief":   [-0.10, -0.05, 0.20],
            "sarcasm": [0.15, -0.10, 0.15],
            "neutral": [0.00, 0.00, 0.00]
        }
        self.shift_constant = 0.05
        self._max_magnitude = self._compute_max_magnitude()

        def _compute_true_max_magnitude(self) -> float:
        """Computes the true maximum Euclidean norm of the combined vector space."""
        total_vector = [0.0, 0.0, 0.0]
        for vec in self.mock_matrix.values():
            for i in range(3):
                total_vector[i] += vec[i] * self.shift_constant
        return math.sqrt(sum(x**2 for x in total_vector))


    def get_max_magnitude(self) -> float:
        return self._max_magnitude

    def score_text(self, text: str) -> List[float]:
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        base_vector = [0.0, 0.0, 0.0]
        
        for token, vector in self.mock_matrix.items():
            if token in words:  
                base_vector = [v + vector[i] * self.shift_constant for i, v in enumerate(base_vector)]
        return base_vector
