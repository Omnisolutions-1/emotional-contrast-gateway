import re

class LiteralIntentParser:
    def __init__(self):
        self.noise_pattern = re.compile(
            r'\b(please|kindly|ugh|oh|wow|gosh|hate to ask but|honestly|literally)\b',
            re.IGNORECASE
        )
        self.emotion_punct = re.compile(r'[^\w\s\-\./\\]')
        self.spacing_pattern = re.compile(r'\s+')

    def parse_intent(self, text: str) -> str:
        cleaned = self.noise_pattern.sub("", text)
        cleaned = self.emotion_punct.sub("", cleaned)
        return self.spacing_pattern.sub(" ", cleaned).strip()
