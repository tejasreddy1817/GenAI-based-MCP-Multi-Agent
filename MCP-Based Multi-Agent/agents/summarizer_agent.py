"""
SummarizerAgent: creates Introduction, Key Insights, Future Trends.
If OPENAI_API_KEY present and use_openai=True, uses OpenAI completions.
Else falls back to an extractive/templated summarizer.
"""
import os
from typing import List, Dict

try:
    import openai
except Exception:
    openai = None

class SummarizerAgent:
    def __init__(self, use_openai: bool = False):
        self.use_openai = use_openai and bool(os.getenv("OPENAI_API_KEY")) and openai is not None
        if self.use_openai:
            openai.api_key = os.getenv("OPENAI_API_KEY")

    def run(self, topic: str, docs: List[Dict], analysis: Dict) -> str:
        if self.use_openai:
            return self._openai_summarize(topic, docs, analysis)
        return self._simple_summarize(topic, docs, analysis)

    def _simple_summarize(self, topic, docs, analysis):
        intro = f"**Introduction**\n\nThis report summarizes findings related to **{topic}** from {analysis['num_docs']} sources."
        insights = "\n\n**Key Insights**\n\n"
        insights += "\n".join(f"- {k}" for k in analysis["themes"])
        insights += f"\n\nAverage words per doc: {analysis['avg_word_count']}"
        sentiment = "neutral"
        if analysis["sentiment_score"] > 0.3:
            sentiment = "positive"
        elif analysis["sentiment_score"] < -0.3:
            sentiment = "negative"
        insights += f"\nOverall sentiment: **{sentiment}**"

        future = "\n\n**Future Trends & Recommendations**\n\n"
        future += "- Explore multimodal and retrieval-augmented models.\n"
        future += "- Emphasize ethical and interpretability aspects.\n"

        return "\n\n".join([intro, insights, future])

    def _openai_summarize(self, topic, docs, analysis):
        snippets = "\n".join(f"{i+1}. {d['title']}: {d['content']}" for i, d in enumerate(docs))
        prompt = f"""
Create a report for the topic '{topic}' using the following sections:
1. Introduction
2. Key Insights (bulleted)
3. Future Trends and Recommendations

Analysis Summary:
{analysis}

Documents:
{snippets}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
