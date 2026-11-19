from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv

# Explicitly load .env from backend folder and project root
_backend_env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_backend_env):
    load_dotenv(_backend_env, override=True)
_root_env = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
if os.path.exists(_root_env):
    load_dotenv(_root_env)
load_dotenv(override=False)

from models import (
    UserAuthRequest,
    UserAuthResponse,
    AnalyzeCareersRequest,
    AnalyzeCareersResponse,
    GenerateStudyPlanRequest,
    StudyPlanResponse,
    MCQsRequest,
    MCQsResponse,
    CodingChallengeRequest,
    CodingChallenge,
    EvaluateCodeRequest,
    EvaluateCodeResponse,
    SamQuestionsRequest,
    SamQuestionsResponse,
    EvaluateAnswerRequest,
    EvaluateAnswerResponse,
    MentorChatRequest,
    MentorChatResponse,
    AssessmentRequest,
    AssessmentResponse
)
from gemini_service import gemini_service

app = FastAPI(
    title="ClariTrack.AI - Student Career & Success Platform",
    version="2.3.0",
    description="ClariTrack.AI: Multi-agent platform with Career Analysis, AI Study Planner, Zam AI Mock Interview Suite, and AI Mentor Chat."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ClariTrack.AI - Student Career & Learning Platform",
        "version": "2.3.0"
    }

# ================= PAGE 1: AUTHENTICATION =================
USERS_DB: Dict[str, Dict[str, str]] = {
    "rakshita@example.com": {
        "name": "Rakshita",
        "email": "rakshita@example.com",
        "password": "password123"
    }
}

@app.post("/api/auth/signup", response_model=UserAuthResponse)
def signup(req: UserAuthRequest):
    email = req.email.strip().lower()
    if email in USERS_DB:
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists. Please log in instead."
        )
    name = req.name.strip() if req.name else (email.split("@")[0].capitalize() or "Student")
    USERS_DB[email] = {
        "name": name,
        "email": email,
        "password": req.password
    }
    return UserAuthResponse(
        name=name,
        email=email,
        token=f"token_{name.lower()}_{abs(hash(email)) % 100000}"
    )

@app.post("/api/auth/login", response_model=UserAuthResponse)
def login(req: UserAuthRequest):
    email = req.email.strip().lower()
    if email not in USERS_DB:
        raise HTTPException(
            status_code=404,
            detail="No account found with this email. Please sign up first."
        )
    user_record = USERS_DB[email]
    if user_record["password"] != req.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password. Please verify your password and try again."
        )
    return UserAuthResponse(
        name=user_record["name"],
        email=email,
        token=f"token_{user_record['name'].lower()}_{abs(hash(email)) % 100000}"
    )

# ================= PAGE 2: AGENT 1 - CAREER ANALYSIS =================
@app.post("/api/analyze-careers", response_model=AnalyzeCareersResponse)
async def analyze_careers(req: AnalyzeCareersRequest):
    student_name = req.student_name or "Rakshita"
    careers, top_pick = await gemini_service.analyze_careers(
        student_name=student_name,
        skills=req.skills,
        api_keys=req.api_keys
    )
    return AnalyzeCareersResponse(
        student_name=student_name,
        careers=careers,
        top_pick=top_pick
    )

# ================= DYNAMIC ROLE ASSESSMENT SUITE =================
@app.post("/api/generate-assessment", response_model=AssessmentResponse)
async def generate_assessment(req: AssessmentRequest):
    role = req.selectedCareer or req.target_career or "Software Engineer"
    student_name = req.student_name or "Rakshita"
    mcqs = await gemini_service.get_mcqs(role)
    challenges = await gemini_service.get_coding_challenges(role)
    voice_qs = await gemini_service.get_sam_interview_questions(role, student_name)
    return AssessmentResponse(
        career_title=role,
        mcqs=mcqs,
        coding_challenges=challenges,
        voice_questions=voice_qs
    )

# ================= PAGE 3: AGENT 2 - STUDY PLANNER =================
@app.post("/api/generate-study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(req: GenerateStudyPlanRequest):
    student_name = req.student_name or "Rakshita"
    plan = await gemini_service.generate_study_plan(
        student_name=student_name,
        target_career=req.target_career,
        skills=req.skills,
        daily_hours=req.daily_hours,
        api_keys=req.api_keys
    )
    return plan

# ================= PAGE 4A: SAM AI INTERVIEW SUITE =================
@app.post("/api/sam-ai/mcqs", response_model=MCQsResponse)
async def get_sam_mcqs(req: MCQsRequest):
    questions = await gemini_service.get_mcqs(req.target_career or "Software Engineer")
    return MCQsResponse(questions=questions)

@app.post("/api/sam-ai/coding-challenge", response_model=CodingChallenge)
async def get_sam_coding_challenge(req: CodingChallengeRequest):
    challenge = await gemini_service.get_coding_challenge(req.target_career or "Software Engineer")
    return challenge

@app.post("/api/sam-ai/coding-challenges", response_model=List[CodingChallenge])
@app.post("/api/zam-ai/coding-challenges", response_model=List[CodingChallenge])
async def get_coding_challenges(req: CodingChallengeRequest):
    return await gemini_service.get_coding_challenges(req.target_career or "Software Engineer")

@app.post("/api/sam-ai/evaluate-code", response_model=EvaluateCodeResponse)
async def evaluate_sam_code(req: EvaluateCodeRequest):
    res = await gemini_service.evaluate_code(
        code=req.code,
        language=req.language,
        student_name=req.student_name or "Rakshita",
        api_keys=req.api_keys
    )
    return res

@app.post("/api/sam-ai/interview-questions", response_model=SamQuestionsResponse)
async def get_sam_questions(req: SamQuestionsRequest):
    questions = await gemini_service.get_sam_interview_questions(
        target_career=req.target_career or "Software Engineer",
        student_name=req.student_name or "Rakshita"
    )
    return SamQuestionsResponse(questions=questions)

@app.post("/api/sam-ai/evaluate-answer", response_model=EvaluateAnswerResponse)
@app.post("/api/zam-ai/evaluate-answer", response_model=EvaluateAnswerResponse)
async def evaluate_sam_answer(req: EvaluateAnswerRequest):
    res = await gemini_service.evaluate_sam_answer(
        question_id=req.question_id,
        question_text=req.question_text,
        student_answer=req.student_answer,
        target_career=req.target_career or "Software Engineer",
        student_name=req.student_name or "Rakshita",
        api_keys=req.api_keys
    )
    return res

# Zam AI Aliases
@app.post("/api/zam-ai/mcqs", response_model=MCQsResponse)
async def get_zam_mcqs(req: MCQsRequest):
    return await get_sam_mcqs(req)

@app.post("/api/zam-ai/coding-challenge", response_model=CodingChallenge)
async def get_zam_coding_challenge(req: CodingChallengeRequest):
    return await get_sam_coding_challenge(req)

@app.post("/api/zam-ai/evaluate-code", response_model=EvaluateCodeResponse)
async def evaluate_zam_code(req: EvaluateCodeRequest):
    return await evaluate_sam_code(req)

@app.post("/api/zam-ai/interview-questions", response_model=SamQuestionsResponse)
async def get_zam_questions(req: SamQuestionsRequest):
    return await get_sam_questions(req)

# ================= PAGE 4B: AGENT 3 - MENTOR CHAT =================
@app.post("/api/mentor-chat", response_model=MentorChatResponse)
async def mentor_chat(req: MentorChatRequest):
    student_name = req.student_name or "Rakshita"
    reply = await gemini_service.mentor_chat(
        student_name=student_name,
        message=req.message,
        history=[m.model_dump() for m in req.history],
        skills=req.skills,
        target_career=req.target_career,
        api_keys=req.api_keys
    )
    return MentorChatResponse(reply=reply)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
