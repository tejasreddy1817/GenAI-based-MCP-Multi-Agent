"""
ValidatorAgent: performs simple checks like missing sections and short coherence checks.
"""
from typing import List, Dict

class ValidatorAgent:
    def run(self, summary: str, docs: List[Dict], analysis: Dict) -> Dict:
        checks = {}
        checks["has_introduction"] = "introduction" in summary.lower()
        checks["has_key_insights"] = "key insights" in summary.lower() or "insights" in summary.lower()
        checks["has_future_trends"] = "future trends" in summary.lower() or "recommendation" in summary.lower()
        checks["num_sources"] = len(docs)
        lines = [l.strip() for l in summary.splitlines() if l.strip()]
        dup_count = len(lines) - len(set(lines))
        checks["redundant_lines"] = int(dup_count)
        return checks
