import re
from typing import Dict, Any, List, Optional

class DynamicContextRouter:
    def __init__(self, config: Optional[Dict] = None, max_tone_magnitude: float = 1.0):
        self.dimension_map = [
            {"label": "valence",    "pos_mode": "empathetic",   "neg_mode": "guarded"},
            {"label": "activation", "pos_mode": "creative",     "neg_mode": "skeptical"},
            {"label": "depth",      "pos_mode": "analytical",   "neg_mode": "reflective"}
        ]
        
        self.literal_magnitude_threshold = 0.15   
        self.max_tone_magnitude = max_tone_magnitude

        self.mode_registry = {
            "literal": {
                "suffix": "Provide a direct, factual answer with no emotional embellishment.",
                "params": {"temperature": 0.3, "top_p": 0.5, "repetition_penalty": 1.0}
            },
            "empathetic": {
                "suffix": "Respond with warmth and empathy. Validate the user's emotional state.",
                "params": {"temperature": 0.8, "top_p": 0.9, "repetition_penalty": 1.1}
            },
            "guarded": {
                "suffix": "The user may be in a defensive or negative state. Proceed cautiously.",
                "params": {"temperature": 0.5, "top_p": 0.7, "repetition_penalty": 1.0}
            },
            "creative": {
                "suffix": "Think divergently. Use metaphors and out-of-the-box solutions.",
                "params": {"temperature": 1.0, "top_p": 0.95, "repetition_penalty": 1.2}
            },
            "skeptical": {
                "suffix": "Adopt a critical, evidence-based stance. Question assumptions.",
                "params": {"temperature": 0.4, "top_p": 0.6, "repetition_penalty": 1.0}
            },
            "analytical": {
                "suffix": "Break down the problem step-by-step. Use structured reasoning.",
                "params": {"temperature": 0.2, "top_p": 0.3, "repetition_penalty": 1.0}
            },
            "reflective": {
                "suffix": "Encourage introspection. Explore underlying meanings.",
                "params": {"temperature": 0.7, "top_p": 0.85, "repetition_penalty": 1.1}
            },
            "paradox_aware": {
                "suffix": "A cognitive paradox has been detected. Balance literal meaning with emotional subtext.",
                "params": {"temperature": 0.6, "top_p": 0.8, "repetition_penalty": 1.2}
            }
        }
        if config:
            self.mode_registry.update(config.get("mode_registry", {}))
            self.dimension_map = config.get("dimension_map", self.dimension_map)
            self.literal_magnitude_threshold = config.get("literal_magnitude_threshold", 0.15)

    def _classify_tone(self, tone_vector: List[float]) -> str:
        raw_mag = sum(x**2 for x in tone_vector) ** 0.5
        normalized_mag = raw_mag / self.max_tone_magnitude if self.max_tone_magnitude > 0 else raw_mag
        
        if normalized_mag < self.literal_magnitude_threshold:
            return "literal"

        max_idx = 0
        max_val = abs(tone_vector[0])
        for i in range(1, len(tone_vector)):
            if abs(tone_vector[i]) > max_val:
                max_val = abs(tone_vector[i])
                max_idx = i

        dim = self.dimension_map[max_idx]
        return dim["pos_mode"] if tone_vector[max_idx] >= 0 else dim["neg_mode"]

    def _classify_intent(self, clean_intent: str, raw_text: Optional[str] = None) -> str:
        text = raw_text if raw_text is not None else clean_intent
        
        polite_imperative = re.search(r'\b(could|can|would|will)\s+you\s+(run|get|find|calculate|show|list|open|stop|start)\b', text.lower())
        if polite_imperative:
            return "command"
            
        if "?" in text:
            return "question"
            
        imperative_starts = ("run", "get", "find", "calculate", "show", "list", "open", "stop", "start")
        if clean_intent.lower().startswith(imperative_starts):
            return "command"
        return "statement"

    def route(self, tone_vector: List[float], clean_intent: str, paradox_state: bool, raw_text: Optional[str] = None) -> Dict[str, Any]:
        if paradox_state:
            base_mode = "paradox_aware"
            tone_mode = self._classify_tone(tone_vector)
        else:
            base_mode = self._classify_tone(tone_vector)
            tone_mode = base_mode

        intent_type = self._classify_intent(clean_intent, raw_text)
        mode_meta = self.mode_registry.get(base_mode, self.mode_registry["literal"])

        return {
            "context_mode": base_mode,
            "tone_mode_debug": tone_mode,
            "intent_type": intent_type,
            "system_prompt_suffix": mode_meta["suffix"],
            "llm_params": mode_meta["params"]
        }
