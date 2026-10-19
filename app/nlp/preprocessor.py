import re
import unicodedata
from typing import Dict, Any

URDU_NUMBERS = {
    "aik": "1", "ek": "1", "do": "2", "teen": "3", "char": "4", "chaar": "4",
    "paanch": "5", "panch": "5", "che": "6", "chhe": "6", "saat": "7",
    "aath": "8", "nau": "9", "no": "9", "das": "10", "gyara": "11",
    "bara": "12", "pandrah": "15", "pandran": "15", "bees": "20",
    "pachees": "25", "tees": "30", "chalees": "40", "challis": "40",
    "pachaas": "50", "pachas": "50", "saath": "60", "sattar": "70",
    "assi": "80", "navve": "90", "sau": "100", "so": "100",
    "hazaar": "1000", "hazar": "1000", "lakh": "100000"
}

ROMAN_URDU_NORMALIZATION = [
    (r"\bpaanch\s+sau\b", "500"),
    (r"\bteen\s+sau\b", "300"),
    (r"\bdo\s+sau\b", "200"),
    (r"\bchallis\s+dollar\b", "$40"),
    (r"\bchalees\s+dollar\b", "$40"),
    (r"\bkam\s+az\s+kam\b", "MOQ"),
    (r"\bkam\s+se\s+kam\b", "MOQ"),
    (r"\bkam\s+az\s+kam\s+(\d+)\b", r"MOQ \1"),
    (r"\b(\d+)\s+din\s+mein\s+delivery\b", r"delivery \1 days"),
    (r"\b(\d+)\s+days\s+delivery\b", r"delivery \1 days"),
    (r"\basli\s+chamray\b", "genuine leather"),
    (r"\basli\s+chamra\b", "genuine leather"),
    (r"\bchamray\b", "leather"),
    (r"\bchamra\b", "leather"),
    (r"\bmardana\b", "men"),
    (r"\bzanana\b", "women"),
    (r"\bkaala\b", "black"),
    (r"\bkala\b", "black"),
    (r"\bneela\b", "blue"),
    (r"\bsufaid\b", "white"),
    (r"\bsafaid\b", "white"),
    (r"\blaall\b", "red"),
    (r"\blal\b", "red"),
    (r"\bhara\b", "green"),
    (r"\bsabz\b", "green"),
]

def normalize_urdu_text(text: str) -> str:
    """
    Cleans unicode, normalizes Roman Urdu words, replaces verbal numbers,
    and maps common Pakistani export jargon.
    """
    if not text:
        return ""

    # Unicode normalization
    cleaned = unicodedata.normalize("NFKC", text.strip())

    # Lowercase for pattern matching
    normalized = cleaned.lower()

    # Normalize specific multi-word phrases first
    for pattern, replacement in ROMAN_URDU_NORMALIZATION:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    # Convert known single-word verbal numbers where appropriate
    tokens = normalized.split()
    converted_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        # Check compound numbers like "paanch sau"
        if i + 1 < len(tokens) and token in URDU_NUMBERS and tokens[i+1] in ["sau", "so", "hazar", "hazaar"]:
            mult = 100 if tokens[i+1] in ["sau", "so"] else 1000
            val = int(URDU_NUMBERS[token]) * mult
            converted_tokens.append(str(val))
            i += 2
            continue
        elif token in URDU_NUMBERS and tokens[i-1:i] != ["kam"]:
            # If next word is "piece", "dollar", "din", convert
            if i + 1 < len(tokens) and tokens[i+1] in ["piece", "pieces", "dollar", "din", "days", "pcs"]:
                converted_tokens.append(URDU_NUMBERS[token])
            else:
                converted_tokens.append(token)
        else:
            converted_tokens.append(token)
        i += 1

    result = " ".join(converted_tokens)
    # Remove multiple spaces
    result = re.sub(r"\s+", " ", result)
    return result
