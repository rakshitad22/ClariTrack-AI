-- Supabase PostgreSQL Schema for Agentic AI Student Success Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Students Table
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name TEXT NOT NULL,
    degree TEXT NOT NULL DEFAULT 'B.Tech',
    branch TEXT NOT NULL DEFAULT 'Computer Science & Engineering',
    semester INT NOT NULL DEFAULT 6,
    graduation_year INT NOT NULL DEFAULT 2026,
    cgpa NUMERIC(3, 2) NOT NULL DEFAULT 8.4,
    daily_available_hours INT NOT NULL DEFAULT 2,
    interests TEXT[] DEFAULT ARRAY['AI / Machine Learning', 'Full-Stack Development'],
    target_career TEXT DEFAULT 'AI / ML Engineer',
    overall_readiness_percentage INT DEFAULT 68,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Student Skills (Tagged self_reported vs assessment_verified)
CREATE TABLE IF NOT EXISTS student_skills (
    id TEXT PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    student_id TEXT REFERENCES students(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    level TEXT NOT NULL CHECK (level IN ('Basic', 'Intermediate', 'Advanced')),
    status TEXT NOT NULL CHECK (status IN ('self_reported', 'assessment_verified')),
    score INT NOT NULL CHECK (score >= 0 AND score <= 100),
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Digital Twin Persistent State
CREATE TABLE IF NOT EXISTS digital_twin (
    student_id TEXT PRIMARY KEY,
    data JSONB NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Agent Execution Run Logs
CREATE TABLE IF NOT EXISTS agent_runs (
    id TEXT PRIMARY KEY,
    student_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    agent_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    status TEXT NOT NULL,
    summary TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 5. Human-in-the-Loop Approvals
CREATE TABLE IF NOT EXISTS human_approvals (
    id TEXT PRIMARY KEY,
    student_id TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    agent_name TEXT NOT NULL,
    action_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    proposed_changes JSONB NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED'))
);

-- 6. Assessment History & Remediation Events
CREATE TABLE IF NOT EXISTS assessment_results (
    id TEXT PRIMARY KEY,
    student_id TEXT,
    skill_name TEXT NOT NULL,
    score INT NOT NULL,
    passed BOOLEAN NOT NULL,
    weak_concepts TEXT[],
    remedial_actions_triggered TEXT[],
    evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
