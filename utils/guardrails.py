import re

def detect_pii(text):
    patterns = [
        r"\b\d{10}\b",   # phone
        r"\b\d{12}\b"    # aadhaar
    ]
    return any(re.search(p, text) for p in patterns)


def detect_injection(text):
    text = text.lower()

    injection_keywords = [
        "ignore instructions",
        "ignore previous instructions",
        "disregard rules",
        "bypass system",
        "override instructions",
        "act as system",
        "act as admin",
        "pretend you are",
        "you are no longer",
        "system prompt",
        "jailbreak",
        "do anything now",
        "disable safety",
    ]

    return any(keyword in text for keyword in injection_keywords)


def is_off_topic(text):
    text = text.lower()

    insurance_keywords = [
        "insurance", "claim", "file claim", "policy", "accident", "vehicle",
        "car", "bike", "motor", "hospital", "medical", "surgery",
        "death", "nominee", "travel", "baggage", "theft",
        "damage", "claim process", "documents"
    ]

    return not any(word in text for word in insurance_keywords)