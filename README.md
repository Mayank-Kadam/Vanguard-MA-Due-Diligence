# 🏛️ VANGUARD — Autonomous M&A Due Diligence Engine

> **Built for the SerpApi India Hackathon 2026**

An autonomous multi-agent AI engine that performs M&A due diligence on any company using **5 SerpApi engines** and an **adversarial Bull vs. Bear AI debate**.

![SerpApi](https://img.shields.io/badge/SerpApi-5%20Engines-FF3D00)
![Groq](https://img.shields.io/badge/Groq-gpt--oss--120b-0A0A0A)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![anime.js](https://img.shields.io/badge/anime.js-Animated-yellow)

---

## 🎯 What It Does

Vanguard replaces a multi-week, $500K consulting engagement with a **60-second AI analysis**:

1. **Gathers Intelligence** — Queries 5 SerpApi engines in parallel
2. **Synthesizes a Report** — Generates a structured due diligence summary (Legal, Talent, Products, IP)
3. **Runs an Adversarial Debate** — A Bull analyst argues FOR the deal; a Bear analyst tears it apart
4. **Delivers a Verdict** — A CEO agent makes the final call: **ACQUIRE**, **PASS**, or **RENEGOTIATE**
5. **Exports a PDF** — Download the full boardroom-ready report

---

## 🏗️ How It Works

### Phase 01 — Intelligence Gathering
The engine queries **5 SerpApi engines** simultaneously:
- **Google Search** — company overview
- **Google News** — legal risks, lawsuits, PR crises
- **Google Jobs** — talent & hiring trends
- **Google Shopping** — product pricing & market presence
- **Google Scholar** — patents & research

### Phase 02 — Intel Report
A Groq-powered LLM synthesizes the raw search data into a structured due diligence summary across 4 categories: **Legal, Talent, Products, and IP**.

### Phase 03 — Adversarial Debate
Two AI agents argue the deal:
- **🐂 The Bull** — argues FOR the acquisition (growth, talent, market position)
- **🐻 The Bear** — argues AGAINST it (lawsuits, regulatory risk, cash burn)

### Phase 04 — CEO Verdict
A third agent, acting as the CEO, listens to both sides and delivers one of three verdicts:
- ✅ **ACQUIRE**
- ❌ **PASS**
- ⚠️ **RENEGOTIATE** (with 3 concrete safeguards)

---

## 🛠️ Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Backend   | FastAPI + Uvicorn (Python 3.13)         |
| AI Models | Groq (`openai/gpt-oss-120b`)            |
| Search    | SerpApi (5 engines)                     |
| Frontend  | HTML + Tailwind CSS + anime.js          |
| Streaming | Server-Sent Events (SSE)                |
| Export    | Native browser print → Save as PDF      |

---

## 🚀 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Mayank-Kadam/Vanguard-MA-Due-Diligence.git
cd Vanguard-MA-Due-Diligence
