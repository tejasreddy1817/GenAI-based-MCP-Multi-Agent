"""
Simplified AnalysisAgent: keyword extraction & sentiment without sklearn.
"""
from typing import List, Dict
import re
from collections import Counter

class AnalysisAgent:
    def __init__(self):
        self.positive_words = {"improve", "benefit", "advance", "success", "effective", "growth", "innovation"}
        self.negative_words = {"challenge", "problem", "limit", "fail", "issue", "risk", "uncertain"}

    def run(self, docs: List[Dict]) -> Dict:
        texts = [d["content"] for d in docs]
        joined = " ".join(texts)
        words = re.findall(r"\b[a-zA-Z]{4,}\b", joined.lower())
        freq = Counter(words)
        keywords = [w for w, _ in freq.most_common(8)]

        sentiment = self._sentiment_score(joined)
        avg_len = sum(len(t.split()) for t in texts) / len(texts)
        return {
            "num_docs": len(docs),
            "themes": keywords[:5],
            "keywords": keywords,
            "avg_word_count": round(avg_len, 2),
            "sentiment_score": sentiment,
        }

    def _sentiment_score(self, text: str):
        text = text.lower()
        pos = sum(text.count(w) for w in self.positive_words)
        neg = sum(text.count(w) for w in self.negative_words)
        total = pos - neg
        if total == 0:
            return 0.0
        return max(-1.0, min(1.0, total / (abs(total) + 1)))
