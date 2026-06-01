import re
import math
import time
from typing import Dict, Any, List

# Import our freshly hardened sensory shield layers
from src.pipeline.tone_sensor import ToneMatrixSensor
from src.pipeline.intent_parser import LiteralIntentParser
from src.pipeline.paradox_guard import ParadoxGuard

class HardenedDynamicContextRouter:
    def __init__(self, max_tone_magnitude: float = 1.0):
        self.max_tone_magnitude = max_tone_magnitude
        self.mode_registry = {
            "literal": {
                "suffix": "Provide a direct, factual answer with no emotional embellishment.",
                "params": {"temperature": 0.3, "top_p": 0.5}
            },
            "paradox_aware": {
                "suffix": "A cognitive paradox has been detected. Proceed with measured steps.",
                "params": {"temperature": 0.5, "top_p": 0.7}
            }
        }

    def route(self, paradox_state: bool) -> Dict[str, Any]:
        base_mode = "paradox_aware" if paradox_state else "literal"
        return {
            "context_mode": base_mode,
            "llm_params": self.mode_registry[base_mode]["params"],
            "system_prompt_suffix": self.mode_registry[base_mode]["suffix"]
        }


class HardenedFrontRoomController:
    def __init__(self):
        self.active_table: List[Dict[str, str]] = []

    def log_user_utterance(self, input_text: str):
        self.active_table.append({"role": "user", "content": input_text})

    def log_assistant_response(self, response_text: str):
        self.active_table.append({"role": "assistant", "content": response_text})
        # Keeps exactly a true rolling 2-turn window (4 items max)
        if len(self.active_table) >= 4:
            self.active_table = self.active_table[-4:]

    def get_history_state(self) -> List[Dict[str, str]]:
        return self.active_table


class OmniOrchestrator:
    def __init__(self, user_id: str):
        self.intent_parser = LiteralIntentParser()
        self.tone_sensor = ToneMatrixSensor()
        self.paradox_guard = ParadoxGuard(threshold=0.25, max_tone_magnitude=self.tone_sensor.get_max_magnitude())
        self.context_router = HardenedDynamicContextRouter(max_tone_magnitude=self.tone_sensor.get_max_magnitude())
        self.front_room = HardenedFrontRoomController()

    def process_incoming_request(self, raw_input: str) -> Dict[str, Any]:
        """Runs the pre-AI sensory shield before hitting runtime execution."""
        tone_vector = self.tone_sensor.score_text(raw_input)
        clean_intent = self.intent_parser.parse_intent(raw_input)
        paradox_telemetry = self.paradox_guard.evaluate(tone_vector, clean_intent)
        routing_payload = self.context_router.route(paradox_telemetry["paradox_state"])
        
        self.front_room.log_user_utterance(clean_intent)

        return {
            "target_inference_text": clean_intent,
            "system_instruction_override": routing_payload["system_prompt_suffix"],
            "llm_runtime_parameters": routing_payload["llm_params"],
            "paradox_alert": paradox_telemetry["paradox_state"],
            "active_context_history": self.front_room.get_history_state()
        }

    def finalize_turn(self, final_llm_response: str) -> str:
        """Commits the actual LLM generation to the buffer window."""
        self.front_room.log_assistant_response(final_llm_response)
        return f"Buffer locked. Messages in window: {len(self.front_room.get_history_state())}"
