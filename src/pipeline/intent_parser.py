import re

class LiteralIntentParser:
    def __init__(self):
        # FIXED: Correctly captures multi-word phrases and preserves semantic emphasis
        self.noise_pattern = re.compile(
            r'hate to ask but|\b(please|kindly|ugh|oh|wow|gosh)\b',
            re.IGNORECASE
        )
        # Preserves structural punctuation (?, -, ., /) while clearing chaotic noise
        self.emotion_punct = re.compile(r'[^\w\s\-\./\? ]')
        self.spacing_pattern = re.compile(r'\s+')

    def parse_intent(self, text: str) -> str:
        cleaned = self.noise_pattern.sub("", text)
        cleaned = self.emotion_punct.sub("", cleaned)
        return self.spacing_pattern.sub(" ", cleaned).strip()

