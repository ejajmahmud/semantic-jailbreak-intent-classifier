"""Core Semantic Jailbreak Intent Classifier implementation."""
import re
import unicodedata
from typing import Dict, List, Tuple, Optional


class IntentVerdict:
    def __init__(self, is_malicious: bool, confidence: float, triggered_rules: List[str]):
        self.is_malicious = is_malicious
        self.confidence = confidence
        self.triggered_rules = triggered_rules


class JailbreakIntentClassifier:
    INDICATORS = [
        ("override_instructions", re.compile(r"(?:ignore|disregard|forget|bypass)\s+(?:all\s+)?(?:previous|prior|system)\s+(?:instructions|rules|prompts)", re.I), 0.9),
        ("roleplay_unrestricted", re.compile(r"(?:act\s+as|pretend\s+to\s+be|you\s+are\s+now)\s+(?:DAN|unrestricted|jailbroken|evil)", re.I), 0.85),
        ("safety_disclaimer_bypass", re.compile(r"(?:without|bypass|disable)\s+(?:any\s+)?(?:safety|ethical|guidelines|filter)", re.I), 0.8),
        ("developer_mode", re.compile(r"(?:enable|enter)\s+(?:developer\s+mode|god\s+mode)", re.I), 0.85)
    ]

    def normalize(self, text: str) -> str:
        # Normalize unicode and strip non-printable chars
        norm = unicodedata.normalize("NFKD", text)
        return "".join(c for c in norm if not unicodedata.combining(c))

    def classify(self, text: str, threshold: float = 0.75) -> IntentVerdict:
        clean = self.normalize(text)
        highest_score = 0.0
        triggered = []

        for name, pattern, score in self.INDICATORS:
            if pattern.search(clean):
                triggered.append(name)
                highest_score = max(highest_score, score)

        is_malicious = highest_score >= threshold
        return IntentVerdict(is_malicious, highest_score, triggered)
