from fastapi import FastAPI
from pydantic import BaseModel
from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.summarizer_agent import SummarizerAgent

from agents.validator_agent import ValidatorAgent
from agents.formatter_agent import FormatterAgent
import os
from dotenv import load_dotenv
from agents.image_generator_agent import ImageGeneratorAgent
image_agent = ImageGeneratorAgent()


load_dotenv()

app = FastAPI(title="MCP Server - Smart Research Assistant")

# Initialize agents
search_agent = SearchAgent()
analysis_agent = AnalysisAgent()
summarizer_agent = SummarizerAgent(use_openai=bool(os.getenv("OPENAI_API_KEY")))
validator_agent = ValidatorAgent()
formatter_agent = FormatterAgent()

# Define input/output schemas
class TopicRequest(BaseModel):
    query: str
    max_results: int = 3
    use_web: bool = False

class DocsRequest(BaseModel):
    docs: list

class SummaryRequest(BaseModel):
    topic: str
    docs: list
    analysis: dict

class ValidationRequest(BaseModel):
    summary: str
    docs: list
    analysis: dict

class FormatRequest(BaseModel):
    topic: str
    summary: str
    analysis: dict

# -----------------------------
# Define MCP Tools (API routes)
# -----------------------------
@app.post("/search_tool")
def search_tool(req: TopicRequest):
    docs = search_agent.run(req.query, max_results=req.max_results, use_web=req.use_web)
    return {"documents": docs}

@app.post("/analyze_tool")
def analyze_tool(req: DocsRequest):
    result = analysis_agent.run(req.docs)
    return {"analysis": result}

@app.post("/summarize_tool")
def summarize_tool(req: SummaryRequest):
    result = summarizer_agent.run(req.topic, req.docs, req.analysis)
    return {"summary": result}

@app.post("/validate_tool")
def validate_tool(req: ValidationRequest):
    result = validator_agent.run(req.summary, req.docs, req.analysis)
    return {"validation": result}

@app.post("/format_tool")
def format_tool(req: FormatRequest):
    md = formatter_agent.to_markdown(req.topic, req.summary, req.analysis)
    return {"markdown": md}

@app.post("/image_tool")
def image_tool(req: SummaryRequest):
    try:
        prompt = f"Generate an image for: {req.topic}. Themes: {', '.join(req.analysis.get('themes', []))}"
        image_url = image_agent.run(prompt)
        return {"image_url": image_url}
    except Exception as e:
        #  Always return JSON, even when generation fails
        return {"error": str(e), "image_url": None}

# Run the MCP server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
