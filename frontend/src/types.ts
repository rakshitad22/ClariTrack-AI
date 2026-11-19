export interface SkillInput {
  name: string;
  level: 'Basic' | 'Intermediate' | 'Advanced';
}

export interface ApiKeysConfig {
  shared_key?: string;
  career_api_key?: string;
  study_plan_api_key?: string;
  mentor_api_key?: string;
  sam_ai_api_key?: string;
}

export interface UserSession {
  name: string;
  email: string;
  token: string;
  target_career?: string;
  daily_hours?: number;
  skills?: SkillInput[];
}

export interface CareerMatch {
  id: string;
  title: string;
  match_percentage: number;
  description: string;
  market_demand: string;
  average_salary: string;
  matched_skills: string[];
  missing_skills: string[];
  timeline_weeks: number;
}

export interface TopPickRecommendation {
  career_title: string;
  match_percentage: number;
  why_recommended: string;
  mastered_skills_summary: string;
  remaining_skills_summary: string;
  action_note: string;
}

export interface AnalyzeCareersResponse {
  student_name: string;
  careers: CareerMatch[];
  top_pick?: TopPickRecommendation;
}

export interface StudyDay {
  day: number;
  skill: string;
  subtopic: string;
  time_allocation: string;
  platform: string;
  practice_track: string;
  reference_title: string;
  reference_url: string;
  docs_url: string;
  completed: boolean;
}

export interface StudyPlanResponse {
  student_name: string;
  target_career: string;
  daily_hours: number;
  total_days: number;
  timeline_summary: string;
  skill_breakdowns: string[];
  days: StudyDay[];
}

// ================= SAM AI INTERVIEW TYPES =================
export interface MCQOption {
  id: string;
  text: string;
}

export interface MCQQuestion {
  id: string;
  question: string;
  code_snippet?: string;
  options: MCQOption[];
  correct_option_id: string;
  explanation: string;
}

export interface CodingChallenge {
  id: string;
  title: string;
  difficulty: string;
  language: string;
  problem_statement: string;
  starter_code: string;
  sample_input: string;
  sample_output: string;
  test_cases: Array<{ input: string; expected: string }>;
}

export interface EvaluateCodeResponse {
  passed: boolean;
  score: number;
  feedback: string;
  time_complexity: string;
  space_complexity: string;
}

export interface InterviewQuestion {
  id: string;
  question_number: number;
  total_questions: number;
  question: string;
  rubric_tags: string[];
}

export interface EvaluateAnswerResponse {
  readiness_score: number;
  technical_depth: number;
  clarity: number;
  practical_relevance: number;
  feedback_summary: string;
  strengths: string[];
  improvements: string[];
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}
