"""
SearchAgent: fetches short simulated articles or uses SerpAPI (optional).
It returns a list of documents: dicts with 'title' and 'content'.
"""
import os
import requests
from typing import List, Dict

SIMULATED = [
    {
        "title": "Recent advances in transformer models",
        "content": "Transformers have revolutionized NLP. Recent work improved efficiency and scaling..."
    },
    {
        "title": "Sentiment trends in AI research",
        "content": "Researchers increasingly emphasize ethics, fairness, and interpretability..."
    },
    {
        "title": "Future directions in language models",
        "content": "Multimodal models, retrieval augmentation, and better evaluation metrics..."
    },
]

class SearchAgent:
    def __init__(self):
        self.serp_api_key = os.getenv("SERPAPI_KEY")

    def run(self, query: str, max_results: int = 3, use_web: bool = False) -> List[Dict]:
        if use_web and self.serp_api_key:
            return self._serp_search(query, max_results)
        # fallback: simulate documents
        out = []
        for i in range(max_results):
            item = SIMULATED[i % len(SIMULATED)].copy()
            item["title"] = f"{item['title']} — {query} (source {i+1})"
            item["content"] = f"{item['content']} (Related to: {query})"
            out.append(item)
        return out

    def _serp_search(self, query: str, max_results: int):
        url = "https://serpapi.com/search.json"
        params = {"q": query, "api_key": self.serp_api_key, "num": max_results}
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()
        docs = []
        for i, r in enumerate(data.get("organic_results", [])[:max_results]):
            title = r.get("title", f"Result {i+1}")
            snippet = r.get("snippet") or r.get("snippet", "")
            docs.append({"title": title, "content": snippet or "No snippet available."})
        return docs
