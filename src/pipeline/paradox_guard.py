import math
from typing import Dict, Any, List

class ParadoxGuard:
    def __init__(self, threshold: float = 0.25, max_tone_magnitude: float = None):
        self.threshold = threshold
        self.max_tone_magnitude = max_tone_magnitude  

    def _calculate_magnitude(self, vector: List[float]) -> float:
        return math.sqrt(sum(v ** 2 for v in vector))

    def evaluate(self, tone_vector: List[float], raw_intent: str) -> Dict[str, Any]:
        raw_tone_mag = self._calculate_magnitude(tone_vector)
        
        if self.max_tone_magnitude and self.max_tone_magnitude > 0:
            tone_magnitude = raw_tone_mag / self.max_tone_magnitude
        else:
            tone_magnitude = raw_tone_mag

        # FIXED: Directly flags neutral input as safe, bypassing length false-positives
        if tone_magnitude == 0.0:
            return {
                "variance_gap": 0.0,
                "paradox_state": False,
                "status": "Status: Nominal"
            }

        # Intent complexity length scaling bound
        intent_complexity = min(len(raw_intent) / 100.0, 1.0)
        variance_gap = abs(tone_magnitude - intent_complexity)
        is_paradox = variance_gap > self.threshold

        return {
            "variance_gap": round(variance_gap, 5),
            "paradox_state": is_paradox,
            "status": "ALERT: Paradox Detected" if is_paradox else "Status: Nominal"
        }

