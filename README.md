# ClariTrack.AI – Know Where You Stand. Rehearse the Moment.

ClariTrack.AI is a full-stack, multi-agent student career intelligence and readiness platform built with **React, TypeScript, Vite, Tailwind CSS, Lucide Icons, FastAPI, Python 3, Pydantic v2, and Google GenAI SDK (`gemini-2.5-flash` & `gemini-2.5-pro`)**.

Featuring the **ClariTrack.AI** dark matte charcoal (`#111116` / `#14141b`) + vivid magenta-to-purple gradient (`#d946ef` to `#8b5cf6`) + emerald readiness ring (`#10b981`) aesthetic without any proctoring or security clutter.

---

## 💎 The ClariTrack.AI Multi-Page Journey

### Page 1: Login & Sign-Up (`/`)
- **Left Panel (Sliding Motivational Quotes):** Auto-sliding carousel featuring inspiring coding, career growth, and persistence quotes.
- **Right Panel (Unified Form):**
  - Switch between **Sign Up** and **Log In**.
  - Student details: **Full Name / Username** (e.g. `Rakshita`), **Email**, and **Password**.
  - Collapsible **"Configure Gemini API Keys"** drawer with fallback to backend `GEMINI_API_KEY`.
  - Seamless authentication saving session to `localStorage` and routing to `/skills`.

### Page 2: Personalized Skill Entry & Career Match (`/skills`)
- **Personalized Hero Greeting:** *"Hi, Rakshita! 👋 - Tell ClariTrack.AI what you know, and our neural matching engine will calculate your highest-matching career paths."*
- **Left Column (Dynamic Skill Builder):**
  - Skill text input + proficiency tier selector: **`Basic`**, **`Intermediate`**, **`Advanced`**.
  - Quick-add recommendation chips (`+ Python`, `+ Java`, `+ SQL`, `+ React`, `+ DSA`...).
  - **"+ Add One More Skill"** button to append rows dynamically + delete (`×`) buttons.
  - Primary button: **"Analyze My Skills & Show Career Paths ✨"**.
- **Right Column (Career Match Results):**
  - Powered by **Agent 1 (`POST /api/analyze-careers` with `gemini-2.5-flash`)**.
  - Career cards **strictly sorted from highest match percentage to lowest** (e.g., 85%, 78%, 65%).
  - Detailed cards with match %, market demand, salary benchmarks, matched tags, and missing gap tags.
  - Direct CTA: **"Choose {Role} & Build Study Plan →"**.

### Page 3: Master Schedule & Daily Study Plan (`/study-plan`)
- **Target Career Confirmation & Daily Study Hours:**
  - Active career indicator with quick switch option.
  - Daily commitment selector (`1 hr/day`, `2 hrs/day`, `3 hrs/day`, `4 hrs/day`).
  - **"Generate My Complete Study Plan"** button.
- **Powered by Agent 2 (`POST /api/generate-study-plan` with `gemini-2.5-pro`):**
  - **Total Days to Master Summary:** Skill-by-skill master days breakdown and total job-ready timeline.
  - **Day-by-Day Execution Cards:**
    - Day number, skill, and exact sub-topic from scratch.
    - Exact hours/day and time allocation splits (concept video vs. hands-on coding).
    - Specific practice platform track (e.g., *HackerRank → Python → Mutations*).
    - Verified reference links (playable YouTube tutorial modal + documentation).
  - **Initial Checked State:** **Day 1 and Day 2 are checked/completed by default** on initial render, with progress tracking persisted in state/localStorage.
  - Quick links to **Zam AI Mock Interview** and **AI Mentor Chat**.

### Page 4A: "Zam AI" Mock Interview Suite (`/sam-ai`)
- **Top Mode Switcher:**
  1. **`1. MCQs`**: Conceptual timed practice with instant explanations and score evaluation.
  2. **`2. Simple Coding`**: Practical beginner-to-intermediate coding challenge with typing + copy-pasting code editor and AI complexity report (time/space complexity analysis).
  3. **`3. Zam AI Voice Interview`**:
     - Live interview question prompt: `• ZAM AI LIVE INTERVIEW • QUESTION X OF Y` in rose-pink/magenta uppercase tracking.
     - Rubric tags: `Core Concept Clarity`, `Practical Trade-offs`, `Real-World Application`.
     - **`Mute Speech` / `Unmute Speech`** toggle with `window.speechSynthesis`.
     - Answer box supporting **Speaking** via `Click to Speak` (Web Speech API), **Typing**, and **Copy-Pasting** freely without interception.
     - Live **Word Count** and vivid magenta **`SUBMIT RESPONSE`** button.
     - **Right Evaluation Panel:** Emerald circular readiness ring (`#10b981`), rubric breakdown gauges, and **ZAM AI EVALUATION FEED**.

### Page 4B: Unlimited AI Career & Tech Mentor Chat (`/mentor`)
- **24/7 Context-Aware Zam AI Mentor (`POST /api/mentor-chat` with `gemini-2.5-pro`):**
  - Automatically synchronized with student name (`Rakshita`), logged skills, and target career.
  - One-click starter prompts for 2026-2027 tech hiring trends, fresher expectations, and project reviews.
  - Markdown rendering, code snippets, copy button, and chat history reset.

---

## 🚀 Running the Project

### 1. Backend (FastAPI)
```bash
# In project root:
.\backend\venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --port 8000 --host 127.0.0.1
```
- API Docs: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/health`

### 2. Frontend (React + Vite)
```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
- Access in browser: `http://127.0.0.1:5173/` (or `http://localhost:5173/`)
