"""
FormatterAgent: simple conversion to markdown and (optionally) more formats.
"""
import markdown2

class FormatterAgent:
    def to_markdown(self, topic: str, summary: str, analysis: dict) -> str:
        header = f"# {topic}\n\n"
        meta = f"_Auto-generated summary — {analysis['num_docs']} sources — Sentiment: {analysis['sentiment_score']}_\n\n"
        md = header + meta + summary + "\n\n"
        return md

    def to_html(self, md: str) -> str:
        return markdown2.markdown(md)
