from __future__ import annotations
import re
from typing import List
import nltk
from nltk.corpus import stopwords

STOP = set()
def ensure_nltk():
    global STOP
    try:
        STOP = set(stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        STOP = set(stopwords.words('english'))

SKILL_PATTERN = re.compile(r"[A-Za-z][A-Za-z+.#]*")

def naive_skill_tokens(text: str) -> List[str]:
    if not isinstance(text, str):
        return []
    toks = [t for t in SKILL_PATTERN.findall(text) if t.lower() not in STOP and len(t) > 2]
    return toks