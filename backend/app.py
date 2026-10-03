# ==========================================================
# VANGUARD BACKEND - M&A Due Diligence API Server
# ==========================================================
import os
import json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# ==== LOAD KEYS FROM .env FILE ====
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

if not GROQ_API_KEY or not SERPAPI_API_KEY:
    raise ValueError("Missing API keys! Please create a .env file with GROQ_API_KEY and SERPAPI_API_KEY")

# ==== AI BRAINS ====
llm = ChatGroq(api_key=GROQ_API_KEY, model="openai/gpt-oss-120b", temperature=0.1)
creative_llm = ChatGroq(api_key=GROQ_API_KEY, model="openai/gpt-oss-120b", temperature=0.5)

# ==== FASTAPI SETUP ====
app = FastAPI(title="Vanguard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    company: str
    description: str

# ==== SERPAPI SEARCH HELPER ====
def serpapi_call(query, engine):
    url = "https://serpapi.com/search"
    params = {"q": query, "api_key": SERPAPI_API_KEY, "engine": engine}
    try:
        response = requests.get(url, params=params, timeout=15)
        results = response.json()
        output = ""
        search_items = (
            results.get("organic_results") or
            results.get("news_results") or
            results.get("jobs_results") or
            results.get("shopping_results") or []
        )
        for r in search_items[:3]:
            title = r.get('title', 'No title')
            snippet = r.get('snippet', r.get('description', 'No snippet'))
            output += f"- {title}: {snippet}\n"
        return output if output else "No results found."
    except Exception as e:
        return f"Search error: {str(e)}"

# ==== THE EVENT STREAM (Real-time updates) ====
def event_stream(company, description):
    def emit(event_type, data):
        return f"data: {json.dumps({'type': event_type, 'data': data})}\n\n"

    yield emit("start", {"company": company, "description": description})

    searches = [
        ("web",      "google",          f"{company} {description} company overview"),
        ("news",     "google_news",     f"{company} {description} lawsuit legal issues"),
        ("jobs",     "google_jobs",     f"{company} {description} hiring jobs"),
        ("shopping", "google_shopping", f"{company} {description} products prices"),
        ("scholar",  "google_scholar",  f"{company} {description} patents research"),
    ]

    results = {}
    for key, engine, query in searches:
        yield emit("search_start", {"engine": key})
        result = serpapi_call(query, engine)
        results[key] = result
        yield emit("search_complete", {"engine": key, "result": result})

    research_doc = (
        f"=== WEB ===\n{results['web']}\n\n"
        f"=== NEWS ===\n{results['news']}\n\n"
        f"=== JOBS ===\n{results['jobs']}\n\n"
        f"=== SHOPPING ===\n{results['shopping']}\n\n"
        f"=== SCHOLAR ===\n{results['scholar']}"
    )

    # ---- Reporter ----
    yield emit("reporter_start", {})
    report_prompt = (
        f"You are an M&A analyst. Create a concise due diligence summary of {company} "
        f"(which is: {description}) based on this data:\n\n{research_doc}\n\n"
        f"Use bullet points for key findings in categories: Legal, Talent, Products, IP."
    )
    report = llm.invoke([HumanMessage(content=report_prompt)]).content
    yield emit("reporter_complete", {"report": report})

    # ---- Bull ----
    yield emit("bull_start", {})
    bull = creative_llm.invoke([HumanMessage(content=(
        f"You are a Bullish M&A Analyst. Argue FOR acquiring {company} (which is: {description}). "
        f"Use this data:\n{report}\n\nHighlight growth, talent, and market position. 2 paragraphs."
    ))]).content
    yield emit("bull_complete", {"bull": bull})

    # ---- Bear ----
    yield emit("bear_start", {})
    bear = creative_llm.invoke([HumanMessage(content=(
        f"You are a Bearish M&A Analyst. Argue AGAINST acquiring {company} (which is: {description}). "
        f"Use this data:\n{report}\n\nWeaponize lawsuits, risks. 2 paragraphs."
    ))]).content
    yield emit("bear_complete", {"bear": bear})

    # ---- Judge ----
    yield emit("judge_start", {})
    judge_prompt = (
        f"You are the CEO making a final acquisition decision on {company}.\n\n"
        f"The Bull argued:\n{bull}\n\n"
        f"The Bear argued:\n{bear}\n\n"
        f"IMPORTANT: Start your response with EXACTLY ONE WORD on the first line: "
        f"either ACQUIRE, PASS, or RENEGOTIATE. Then a blank line, then 2 paragraphs of reasoning.\n\n"
        f"CRITICAL RULES for choosing:\n"
        f"- Do NOT default to RENEGOTIATE as a safe middle ground. That is weak leadership.\n"
        f"- Choose ACQUIRE if the strategic case is strong and the risks are manageable.\n"
        f"- Choose PASS if the risks clearly outweigh the upside (e.g., dying business, massive liabilities, no clear moat).\n"
        f"- Only choose RENEGOTIATE if a specific, concrete deal structure (escrow, earn-out, safeguards) would genuinely unlock value.\n\n"
        f"If you chose RENEGOTIATE, list 3 concrete safeguards at the end. Be decisive."
    )
    ruling_raw = creative_llm.invoke([HumanMessage(content=judge_prompt)]).content

    # Parse the decision from the first line
    first_line = ruling_raw.strip().split('\n')[0].strip().upper()
    if "RENEGOTIATE" in first_line:
        decision = "RENEGOTIATE"
    elif "ACQUIRE" in first_line:
        decision = "ACQUIRE"
    elif "PASS" in first_line:
        decision = "PASS"
    else:
        ruling_upper = ruling_raw.upper()
        if "RENEGOTIATE" in ruling_upper:
            decision = "RENEGOTIATE"
        elif "PASS" in ruling_upper[:200]:
            decision = "PASS"
        elif "ACQUIRE" in ruling_upper[:200]:
            decision = "ACQUIRE"
        else:
            decision = "REVIEW"

    # Clean the ruling text
    ruling_lines = ruling_raw.strip().split('\n')
    if ruling_lines[0].strip().upper() in ["ACQUIRE", "PASS", "RENEGOTIATE"]:
        ruling = '\n'.join(ruling_lines[1:]).strip()
    else:
        ruling = ruling_raw

    yield emit("judge_complete", {"ruling": ruling, "decision": decision})

    yield emit("complete", {})

# ==== ROUTES ====
@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    return StreamingResponse(
        event_stream(request.company, request.description),
        media_type="text/event-stream"
    )

@app.get("/")
async def root():
    return {"status": "Vanguard API is running", "version": "1.1"}
