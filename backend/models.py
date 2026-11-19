from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

class SkillInput(BaseModel):
    name: str
    level: Literal["Basic", "Intermediate", "Advanced"] = "Intermediate"

class UserAuthRequest(BaseModel):
    name: Optional[str] = "Rakshita"
    email: str
    password: str

class UserAuthResponse(BaseModel):
    name: str
    email: str
    token: str

class ApiKeysConfig(BaseModel):
    shared_key: Optional[str] = None
    career_api_key: Optional[str] = None
    study_plan_api_key: Optional[str] = None
    mentor_api_key: Optional[str] = None
    sam_ai_api_key: Optional[str] = None

class AnalyzeCareersRequest(BaseModel):
    student_name: Optional[str] = "Rakshita"
    skills: List[SkillInput]
    api_keys: Optional[ApiKeysConfig] = None

class CareerMatch(BaseModel):
    id: str
    title: str
    match_percentage: int
    description: str
    market_demand: str
    average_salary: str
    matched_skills: List[str]
    missing_skills: List[str]
    timeline_weeks: int

class TopPickRecommendation(BaseModel):
    career_title: str
    match_percentage: int
    why_recommended: str
    mastered_skills_summary: str
    remaining_skills_summary: str
    action_note: str

class AnalyzeCareersResponse(BaseModel):
    student_name: str
    careers: List[CareerMatch]
    top_pick: Optional[TopPickRecommendation] = None

class GenerateStudyPlanRequest(BaseModel):
    student_name: Optional[str] = "Rakshita"
    target_career: str
    skills: List[SkillInput]
    daily_hours: int = 2
    api_keys: Optional[ApiKeysConfig] = None

class StudyDay(BaseModel):
    day: int
    skill: str
    subtopic: str
    time_allocation: str
    platform: str
    practice_track: str
    reference_title: str
    reference_url: str
    docs_url: str
    completed: bool = False

class StudyPlanResponse(BaseModel):
    student_name: str
    target_career: str
    daily_hours: int
    total_days: int
    timeline_summary: str
    skill_breakdowns: List[str]
    days: List[StudyDay]

# ================= SAM AI INTERVIEW SUITE MODELS =================
class MCQOption(BaseModel):
    id: str
    text: str

class MCQQuestion(BaseModel):
    id: str
    question: str
    code_snippet: Optional[str] = None
    options: List[MCQOption]
    correct_option_id: str
    explanation: str

class MCQsRequest(BaseModel):
    target_career: Optional[str] = "Software Engineer"
    skills: List[SkillInput] = []
    api_keys: Optional[ApiKeysConfig] = None

class MCQsResponse(BaseModel):
    questions: List[MCQQuestion]

class CodingChallenge(BaseModel):
    id: str
    title: str
    difficulty: str
    language: str
    problem_statement: str
    starter_code: str
    sample_input: str
    sample_output: str
    test_cases: List[Dict[str, str]]

class CodingChallengeRequest(BaseModel):
    target_career: Optional[str] = "Software Engineer"
    skills: List[SkillInput] = []
    api_keys: Optional[ApiKeysConfig] = None

class EvaluateCodeRequest(BaseModel):
    challenge_id: str
    code: str
    language: str = "python"
    student_name: Optional[str] = "Rakshita"
    api_keys: Optional[ApiKeysConfig] = None

class EvaluateCodeResponse(BaseModel):
    passed: bool
    score: int
    feedback: str
    time_complexity: str
    space_complexity: str

class InterviewQuestion(BaseModel):
    id: str
    question_number: int
    total_questions: int
    question: str
    rubric_tags: List[str]

class SamQuestionsRequest(BaseModel):
    target_career: Optional[str] = "Software Engineer"
    skills: List[SkillInput] = []
    student_name: Optional[str] = "Rakshita"
    api_keys: Optional[ApiKeysConfig] = None

class SamQuestionsResponse(BaseModel):
    questions: List[InterviewQuestion]

class EvaluateAnswerRequest(BaseModel):
    question_id: str
    question_text: str
    student_answer: str
    target_career: Optional[str] = "Software Engineer"
    student_name: Optional[str] = "Rakshita"
    api_keys: Optional[ApiKeysConfig] = None

class EvaluateAnswerResponse(BaseModel):
    readiness_score: int
    technical_depth: int
    clarity: int
    practical_relevance: int
    feedback_summary: str
    strengths: List[str]
    improvements: List[str]

# ================= MENTOR CHAT =================
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class MentorChatRequest(BaseModel):
    student_name: Optional[str] = "Rakshita"
    message: str
    history: List[ChatMessage] = []
    skills: List[SkillInput] = []
    target_career: Optional[str] = None
    api_keys: Optional[ApiKeysConfig] = None

class MentorChatResponse(BaseModel):
    reply: str

# ================= DYNAMIC ASSESSMENT SUITE =================
class AssessmentRequest(BaseModel):
    selectedCareer: Optional[str] = "Software Engineer"
    target_career: Optional[str] = None
    skills: Optional[List[SkillInput]] = []
    student_name: Optional[str] = "Rakshita"

class AssessmentResponse(BaseModel):
    career_title: str
    mcqs: List[MCQQuestion]
    coding_challenges: List[CodingChallenge]
    voice_questions: List[InterviewQuestion]
