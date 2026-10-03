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

1. **Gathers Intelligence** — Queries 5 SerpApi engines in parallel: **Google Search, News, Jobs, Shopping, Scholar**
2. **Synthesizes a Report** — Generates a structured due diligence summary (Legal, Talent, Products, IP)
3. **Runs an Adversarial Debate** — A Bull analyst argues FOR the deal; a Bear analyst tears it apart
4. **Delivers a Verdict** — A CEO agent makes the final call: **ACQUIRE**, **PASS**, or **RENEGOTIATE**
5. **Exports a PDF** — Download the full boardroom-ready report

---

## 🏗️ Architecture
[ User Input: Company + Description ]
│
▼
┌───────────────────────────────┐
│ Phase 01: Intelligence │
│ 5× SerpApi Engines │
│ • Google Search │
│ • Google News (legal risks) │
│ • Google Jobs (talent) │
│ • Google Shopping (products) │
│ • Google Scholar (IP/patents)│
└───────────────────────────────┘
│
▼
┌───────────────────────────────┐
│ Phase 02: Intel Report │
│ Reporter Agent (Groq LLM) │
└───────────────────────────────┘
│
┌─────┴─────┐
▼ ▼
┌────────────┐ ┌────────────┐
│ 🐂 BULL │ │ 🐻 BEAR │
│ FOR deal │ │ AGAINST │
└────────────┘ └────────────┘
│ │
└─────┬─────┘
▼
┌───────────────────────────────┐
│ Phase 04: ⚖️ Judge (CEO) │
│ ACQUIRE / PASS / RENEGOTIATE │
└───────────────────────────────┘
│
▼
[ PDF Report Downloaded ]


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
git clone https://github.com/YOUR_USERNAME/Vanguard-MA-Due-Diligence.git
cd Vanguard-MA-Due-Diligence
