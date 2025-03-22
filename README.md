# 🧪 LLM Evaluation Lab  
> _Continuous, standardized, and intelligent evaluation infrastructure for large language models_

---

## 🚀 What is LLM Evaluation Lab?

**LLM Evaluation Lab** is a platform for **automated benchmarking, failure discovery, and continuous testing** of large language models (LLMs) — built for the next generation of **AI agents**, **LLM-based products**, and **research labs**.

It helps ML teams, researchers, and AI companies:
- Identify and track **hallucinations, regressions, and unsafe completions**
- Compare model performance across **tasks, versions, or fine-tunes**
- Simulate adversarial attacks like **jailbreaks and prompt injections**
- Generate **beautiful, actionable reports** to share or integrate into CI

> ⚡ Evaluate your models like OpenAI, Meta, and DeepMind — without the overhead.

---

## 🔍 Key Features

### ✅ Standardized Evaluation Engine  
Run controlled, repeatable benchmarks on:
- Factual QA, Math, Code, Logic, Reasoning
- Multi-modal inputs (Vision, Audio, Text)
- Role-played and real-world prompts

### 🤖 Agent Evaluation Mode  
Evaluate autonomous agents (AutoGPT-style) across:
- Task success rate
- Reasoning efficiency
- Hallucination frequency and step-level breakdown

### 🧠 Regression Tracking & Analytics  
- Compare model versions over time
- Visualize capability shifts, failures, and wins
- Get alerts on unexpected regressions

### 🛡 Jailbreak & Prompt Injection Simulator  
- Launch adversarial red teaming runs
- Detect common prompt attack vectors
- Rank your models by “jailbreak resistance”

### 🪄 Dynamic Prompt Miner (Optional Add-on)  
- Pull real-world prompts from Reddit, GitHub, etc.
- Auto-label and inject into test sets for fresh evaluations

### 📊 Beautiful Visualizations & Dashboards  
- Radar charts, diff viewers, failure heatmaps
- Leaderboards by model, score, category
- Embedding clusters of failed completions

---

## 🧱 Tech Stack

| Layer        | Tech Used |
|--------------|-----------|
| **Frontend** | React + Tailwind + D3.js |
| **Backend**  | FastAPI + Celery + LangChain |
| **LLM APIs** | OpenAI, Claude, LLaMA, Gemini, Ollama |
| **DB**       | PostgreSQL / Supabase |
| **DevOps**   | Docker + Railway / Fly.io |

---

## 📦 Get Started

```bash
git clone https://github.com/thabhelo/llm-evaluation-lab
cd llm-evaluation-lab
cp .env.example .env
docker-compose up --build
