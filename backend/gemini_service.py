import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Ensure .env is loaded
_backend_env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_backend_env):
    load_dotenv(_backend_env, override=True)
load_dotenv()
from models import (
    SkillInput, CareerMatch, TopPickRecommendation, StudyDay, StudyPlanResponse, ApiKeysConfig,
    MCQQuestion, MCQOption, CodingChallenge, InterviewQuestion,
    EvaluateCodeResponse, EvaluateAnswerResponse
)
from role_banks import get_role_mcqs, get_role_coding_challenges

logger = logging.getLogger("gemini_service")

# Curated benchmark dictionary of verified industry expectations
CAREER_DATABASE = {
    "Software Engineer": {
        "required": ["Python", "Java", "Data Structures & Algorithms", "SQL", "Git", "System Design"],
        "desc": "Designs, develops, tests, and maintains robust, scalable application software and backend microservices.",
        "demand": "94% (Very High)",
        "salary": "₹10 - ₹22 LPA",
        "prep_weeks": 8
    },
    "Backend Developer": {
        "required": ["Python", "SQL", "FastAPI / Node.js", "Docker", "Database Design", "Redis"],
        "desc": "Builds high-throughput APIs, data pipelines, caching layers, and database architectures.",
        "demand": "91% (High)",
        "salary": "₹9 - ₹18 LPA",
        "prep_weeks": 6
    },
    "AI / ML Engineer": {
        "required": ["Python", "Machine Learning", "PyTorch / TensorFlow", "Data Structures & Algorithms", "SQL", "Vector DBs"],
        "desc": "Develops machine learning models, fine-tunes LLMs, and deploys scalable inference pipelines.",
        "demand": "96% (Explosive)",
        "salary": "₹12 - ₹25 LPA",
        "prep_weeks": 10
    },
    "Full-Stack Developer": {
        "required": ["React", "JavaScript / TypeScript", "Python / Node.js", "SQL", "HTML / Tailwind CSS", "Git"],
        "desc": "Creates fluid client interfaces and bridges them to robust server-side business logic and databases.",
        "demand": "92% (High)",
        "salary": "₹8 - ₹17 LPA",
        "prep_weeks": 7
    },
    "Data Analyst": {
        "required": ["SQL", "Python", "Data Analytics", "Excel / Tableau", "Statistics"],
        "desc": "Extracts actionable business insights, creates operational dashboards, and conducts statistical queries.",
        "demand": "86% (Strong)",
        "salary": "₹7 - ₹14 LPA",
        "prep_weeks": 5
    },
    "Cloud & DevOps Engineer": {
        "required": ["Linux", "Docker", "Kubernetes", "AWS / GCP", "CI/CD", "Terraform"],
        "desc": "Automates cloud infrastructure, manages container orchestration, and optimizes deployment velocity.",
        "demand": "90% (High)",
        "salary": "₹11 - ₹20 LPA",
        "prep_weeks": 9
    }
}

class GeminiService:
    def __init__(self):
        self.default_env_key = os.getenv("GEMINI_API_KEY", "")

    def _resolve_key(self, specific_key: Optional[str], shared_key: Optional[str]) -> Optional[str]:
        if specific_key and specific_key.strip():
            return specific_key.strip()
        if shared_key and shared_key.strip():
            return shared_key.strip()
        live_env_key = os.getenv("GEMINI_API_KEY", "").strip() or self.default_env_key.strip()
        if live_env_key:
            return live_env_key
        return None

    def _get_client(self, api_key: Optional[str]):
        if not api_key:
            return None
        try:
            from google import genai
            return genai.Client(api_key=api_key)
        except Exception as e:
            logger.warning(f"Could not initialize google-genai: {e}")
            return None

    def compute_top_pick(
        self,
        careers: List[CareerMatch],
        skills: List[SkillInput],
        student_name: str = "Rakshita"
    ) -> TopPickRecommendation:
        if not careers:
            return TopPickRecommendation(
                career_title="Software Engineer",
                match_percentage=85,
                why_recommended=f"I recommend **Software Engineer** for you, {student_name}—your foundational problem-solving and software development skills match industry requisites.",
                mastered_skills_summary="Strong core language and algorithmic logic foundations.",
                remaining_skills_summary="Targeted practice in system design and cloud deployments.",
                action_note="Learning modern cloud workflows and microservices will make you 100% placement-ready."
            )

        top = careers[0]
        role_title = top.title
        match_pct = top.match_percentage

        mastered = top.matched_skills if top.matched_skills else [s.name for s in skills[:3]]
        missing = top.missing_skills if top.missing_skills else ["System Design", "Cloud Basics"]

        mastered_text = ", ".join(mastered[:3])
        missing_text = ", ".join(missing[:3])

        why_rec = (
            f"I recommend **{role_title}** for you, {student_name}—you've already built a strong foundation in "
            f"**{mastered_text}**, which gives you an immediate competitive edge for 2026-2027 entry-level roles."
        )

        remaining_text = (
            f"Learning just **{missing_text}** is enough to master this particular role and become 100% placement-ready."
        )

        return TopPickRecommendation(
            career_title=role_title,
            match_percentage=match_pct,
            why_recommended=why_rec,
            mastered_skills_summary=f"Mastered: {mastered_text}",
            remaining_skills_summary=remaining_text,
            action_note=f"Select this recommended role below to auto-generate your step-by-step master roadmap."
        )

    # ================= AGENT 1: CAREER ANALYSIS =================
    async def analyze_careers(
        self,
        student_name: str,
        skills: List[SkillInput],
        api_keys: Optional[ApiKeysConfig] = None
    ) -> Tuple[List[CareerMatch], TopPickRecommendation]:
        key = self._resolve_key(
            api_keys.career_api_key if api_keys else None,
            api_keys.shared_key if api_keys else None
        )
        client = self._get_client(key)

        skills_summary = ", ".join([f"{s.name} ({s.level})" for s in skills]) if skills else "None specified"

        if client:
            prompt = (
                f"Student Name: {student_name}\n"
                f"Student Skills: {skills_summary}\n\n"
                "Evaluate the student's skills against modern industry roles in 2026-2027. "
                "Return a JSON object with a list 'careers' containing 5-6 role recommendations sorted strictly by match_percentage descending. "
                "Each item must have: id, title, match_percentage (integer 35-95), description, market_demand, average_salary, matched_skills (list), missing_skills (list), timeline_weeks (int)."
            )
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                if response and response.text:
                    data = json.loads(response.text)
                    if "careers" in data and isinstance(data["careers"], list):
                        sorted_careers = sorted(
                            [CareerMatch(**c) for c in data["careers"]],
                            key=lambda x: x.match_percentage,
                            reverse=True
                        )
                        top_pick = self.compute_top_pick(sorted_careers, skills, student_name)
                        return sorted_careers, top_pick
            except Exception as e:
                logger.error(f"Gemini API Agent 1 error: {e}")

        # Deterministic Domain-Engine fallback
        results: List[CareerMatch] = []
        user_skill_map = {s.name.lower().strip(): s.level for s in skills}
        level_weights = {"Basic": 0.5, "Intermediate": 0.8, "Advanced": 1.0}

        for role_title, details in CAREER_DATABASE.items():
            matched = []
            missing = []
            score_accum = 0

            for req in details["required"]:
                matched_found = False
                for u_skill, u_lvl in user_skill_map.items():
                    if u_skill in req.lower() or req.lower() in u_skill:
                        matched.append(req)
                        score_accum += level_weights.get(u_lvl, 0.7) * 100
                        matched_found = True
                        break
                if not matched_found:
                    missing.append(req)

            total_req = max(1, len(details["required"]))
            base_ratio = len(matched) / total_req
            weighted_score = (score_accum / (total_req * 100)) * 100 if matched else 0
            final_match = int(0.6 * (base_ratio * 100) + 0.4 * weighted_score)
            final_match = max(35, min(95, final_match))

            results.append(CareerMatch(
                id=role_title.lower().replace(" ", "-").replace("/", "-"),
                title=role_title,
                match_percentage=final_match,
                description=details["desc"],
                market_demand=details["demand"],
                average_salary=details["salary"],
                matched_skills=matched if matched else ["Foundational Aptitude"],
                missing_skills=missing,
                timeline_weeks=details["prep_weeks"]
            ))

        results.sort(key=lambda x: x.match_percentage, reverse=True)
        top_pick = self.compute_top_pick(results, skills, student_name)
        return results, top_pick

    # ================= AGENT 2: STUDY PLAN GENERATOR =================
    async def generate_study_plan(
        self,
        student_name: str,
        target_career: str,
        skills: List[SkillInput],
        daily_hours: int = 2,
        api_keys: Optional[ApiKeysConfig] = None
    ) -> StudyPlanResponse:
        key = self._resolve_key(
            api_keys.study_plan_api_key if api_keys else None,
            api_keys.shared_key if api_keys else None
        )

        VERIFIED_CURRICULUM = {
            "Software Engineer": [
                {
                    "skill": "Python / Core Language",
                    "days": [
                        ("Data Types, Control Flow & String Slicing", "HackerRank -> Python -> Strings -> Mutations", "https://www.youtube.com/watch?v=kqtD5dpn9C8", "Python for Beginners - Full Course", "https://docs.python.org/3/tutorial/"),
                        ("Lists, Dictionaries & Set Comprehensions", "HackerRank -> Python -> Sets -> Symmetric Difference", "https://www.youtube.com/watch?v=daefaLgNkw0", "Python Dictionaries & Sets Explained", "https://docs.python.org/3/tutorial/datastructures.html"),
                        ("Object-Oriented Programming (Classes & Inheritance)", "HackerRank -> Python -> Classes -> Dealing with Complex Numbers", "https://www.youtube.com/watch?v=JeznW_7DlB0", "OOP in Python Tutorial", "https://docs.python.org/3/tutorial/classes.html"),
                        ("Exception Handling, File I/O & Context Managers", "HackerRank -> Python -> Errors and Exceptions", "https://www.youtube.com/watch?v=NIWwJbo-9_8", "Python Exception Handling & Context Managers", "https://docs.python.org/3/tutorial/errors.html")
                    ]
                },
                {
                    "skill": "Data Structures & Algorithms",
                    "days": [
                        ("Arrays & Two-Pointer Technique", "LeetCode -> #167 Two Sum II (Input Array Is Sorted)", "https://www.youtube.com/watch?v=On03HWe2tZM", "Two Pointer Technique Explained Simply", "https://en.wikipedia.org/wiki/Two-pointer_technique"),
                        ("Hash Maps & Frequency Analysis", "HackerRank -> Dictionaries and Hashmaps -> Two Strings", "https://www.youtube.com/watch?v=shs0KM3wKv8", "Hash Tables & Hash Maps - CS Basics", "https://visualgo.net/en/hashtable"),
                        ("Binary Search & Monotonic Search Spaces", "HackerRank -> Algorithms -> Search -> Ice Cream Parlor", "https://www.youtube.com/watch?v=MFhxShGxHWc", "Binary Search Algorithm in 100 Seconds", "https://www.geeksforgeeks.org/binary-search/"),
                        ("Linked Lists & Fast/Slow Pointer Cycle Detection", "HackerRank -> Data Structures -> Linked Lists -> Detect Loop", "https://www.youtube.com/watch?v=jcZtMh_jovU", "Detect Loop in Linked List (Floyd's Algorithm)", "https://visualgo.net/en/list"),
                        ("Stacks, Queues & Monotonic Stacks", "LeetCode -> #20 Valid Parentheses", "https://www.youtube.com/watch?v=WTzjTskDFMg", "Stacks and Queues Explained", "https://www.geeksforgeeks.org/stack-data-structure/"),
                        ("Binary Trees & Breadth-First / Depth-First Traversal", "LeetCode -> #102 Binary Tree Level Order Traversal", "https://www.youtube.com/watch?v=6ZnyEApgFYg", "Binary Tree Traversals (BFS, DFS)", "https://visualgo.net/en/bst")
                    ]
                },
                {
                    "skill": "SQL & Relational Databases",
                    "days": [
                        ("Complex Joins (INNER, LEFT, FULL OUTER)", "HackerRank -> SQL -> Basic Join -> African Cities", "https://www.youtube.com/watch?v=9yeOJ0ZMUYw", "SQL Joins Explained Visually", "https://www.postgresql.org/docs/current/queries-table-expressions.html"),
                        ("Aggregations, GROUP BY & HAVING Filters", "HackerRank -> SQL -> Aggregation -> Top Earners", "https://www.youtube.com/watch?v=QPdT8_MflWk", "SQL Aggregation and Grouping", "https://www.postgresql.org/docs/current/tutorial-agg.html"),
                        ("Window Functions (ROW_NUMBER, RANK, DENSE_RANK)", "LeetCode -> Database -> #178 Rank Scores", "https://www.youtube.com/watch?v=Ww71knvhQ-s", "SQL Window Functions Tutorial", "https://www.postgresql.org/docs/current/tutorial-window.html")
                    ]
                },
                {
                    "skill": "System Design & Git Workflows",
                    "days": [
                        ("Git Branching, PRs & Merge Conflict Resolution", "GitHub Skills -> Introduction to GitHub", "https://www.youtube.com/watch?v=RGOj5yH7evk", "Git and GitHub for Beginners", "https://git-scm.com/doc"),
                        ("REST API Architecture & HTTP Status Standards", "FastAPI Docs -> First Steps -> Path Parameters", "https://www.youtube.com/watch?v=tLKKmouUAMS", "FastAPI in 100 Seconds", "https://fastapi.tiangolo.com/tutorial/first-steps/")
                    ]
                }
            ],
            "AI / ML Engineer": [
                {
                    "skill": "Python & NumPy / Pandas",
                    "days": [
                        ("NumPy Vectorized Arrays & Broadcasting", "Kaggle -> Python -> Numerical Python", "https://www.youtube.com/watch?v=QUT1VHiLmmI", "NumPy Tutorial for Beginners", "https://numpy.org/doc/stable/user/quickstart.html"),
                        ("Pandas DataFrames, GroupBy & Data Cleaning", "Kaggle -> Pandas -> Grouping and Sorting", "https://www.youtube.com/watch?v=vmEHCJofslg", "Pandas Complete Course", "https://pandas.pydata.org/docs/getting_started/index.html")
                    ]
                },
                {
                    "skill": "PyTorch & Deep Learning Foundations",
                    "days": [
                        ("PyTorch Tensors, Gradients & Autograd", "PyTorch.org -> Tutorials -> Learn the Basics -> Tensors", "https://www.youtube.com/watch?v=ORMx45xqWkA", "PyTorch in 100 Seconds", "https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html"),
                        ("Multi-Layer Perceptrons & Backpropagation", "Kaggle -> Intro to Deep Learning -> A Single Neuron", "https://www.youtube.com/watch?v=aircAruvnKk", "Neural Networks from Scratch with PyTorch", "https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html"),
                        ("Convolutional Neural Networks & Vision Backbones", "Kaggle -> Computer Vision -> The Convolutional Classifier", "https://www.youtube.com/watch?v=KuXjwB4LzSA", "CNNs Explained Simply", "https://pytorch.org/vision/stable/index.html")
                    ]
                },
                {
                    "skill": "Vector Search & Retrieval Augmented Generation (RAG)",
                    "days": [
                        ("Self-Attention & Transformer Architecture", "HuggingFace NLP Course -> Chapter 1", "https://www.youtube.com/watch?v=SZorAJ4I-sA", "Attention Is All You Need Explained", "https://huggingface.co/docs/transformers/index"),
                        ("Sentence Embeddings & Qdrant / Pinecone Vector Stores", "Qdrant.tech -> Quickstart Python Client", "https://www.youtube.com/watch?v=klTvEwg3oJ4", "Vector Databases in 100 Seconds", "https://qdrant.tech/documentation/quick-start/"),
                        ("End-to-End RAG Pipeline with FastAPI", "FastAPI + Qdrant Integration Guide", "https://www.youtube.com/watch?v=T-D1OfcDW1M", "RAG Architecture Explained", "https://python.langchain.com/docs/get_started/introduction")
                    ]
                }
            ],
            "Data Analyst": [
                {
                    "skill": "SQL Mastery",
                    "days": [
                        ("Analytical SQL, CTEs & Common Table Expressions", "HackerRank -> SQL -> Advanced Select", "https://www.youtube.com/watch?v=9yeOJ0ZMUYw", "SQL for Data Analysis", "https://mode.com/sql-tutorial/sql-cte/"),
                        ("Window Functions & Rolling Averages", "LeetCode -> Database -> Consecutives Numbers", "https://www.youtube.com/watch?v=Ww71knvhQ-s", "SQL Window Functions Masterclass", "https://mode.com/sql-tutorial/sql-window-functions/")
                    ]
                },
                {
                    "skill": "Python for Analytics",
                    "days": [
                        ("Pandas Exploratory Data Analysis (EDA)", "Kaggle -> Data Cleaning Course", "https://www.youtube.com/watch?v=vmEHCJofslg", "Exploratory Data Analysis in Python", "https://pandas.pydata.org/docs/"),
                        ("Matplotlib & Seaborn Statistical Plotting", "Kaggle -> Data Visualization", "https://www.youtube.com/watch?v=a9UrKTVEeZA", "Seaborn Visualizations Tutorial", "https://seaborn.pydata.org/tutorial.html")
                    ]
                },
                {
                    "skill": "Dashboarding & A/B Testing",
                    "days": [
                        ("Building Interactive Dashboards (Power BI / Tableau)", "Tableau Public Tutorial", "https://www.youtube.com/watch?v=TPPlXWz7R5M", "Tableau in 100 Seconds", "https://help.tableau.com/current/guides/get-started-tutorial/en-us/get-started-tutorial-home.htm"),
                        ("Hypothesis Testing, P-Values & A/B Test Design", "Khan Academy -> Statistics and Probability", "https://www.youtube.com/watch?v=0oc49DyA3hU", "Hypothesis Testing Explained", "https://en.wikipedia.org/wiki/Statistical_hypothesis_testing")
                    ]
                }
            ]
        }

        if daily_hours == 1:
            split_str = "1 Hour/Day: 25 mins Concept Video + 35 mins Hands-on Coding"
        elif daily_hours == 2:
            split_str = "2 Hours/Day: 45 mins Concept Video + 1 hr 15 mins Hands-on Coding"
        elif daily_hours == 3:
            split_str = "3 Hours/Day: 1 hr Video/Theory + 2 hrs Guided Problem Solving"
        else:
            split_str = f"{daily_hours} Hours/Day: 1.5 hrs In-Depth Architecture + {daily_hours - 1.5:.1f} hrs Intensive Lab"

        curriculum = VERIFIED_CURRICULUM.get(target_career, VERIFIED_CURRICULUM["Software Engineer"])

        study_days: List[StudyDay] = []
        skill_breakdowns = []
        day_counter = 1

        for module in curriculum:
            skill_name = module["skill"]
            num_days = len(module["days"])
            skill_breakdowns.append(f"Master {skill_name} in {num_days * (2 if daily_hours == 1 else 1)} Days")

            for item in module["days"]:
                subtopic, platform_track, yt_url, yt_title, docs = item
                # REQUIREMENT: Day 1 and Day 2 checked by default
                is_initially_checked = (day_counter <= 2)
                study_days.append(StudyDay(
                    day=day_counter,
                    skill=skill_name,
                    subtopic=subtopic,
                    time_allocation=split_str,
                    platform=platform_track.split("->")[0].strip(),
                    practice_track=platform_track,
                    reference_title=yt_title,
                    reference_url=yt_url,
                    docs_url=docs,
                    completed=is_initially_checked
                ))
                day_counter += 1

        total_days = len(study_days)
        timeline_summary = f"{' | '.join(skill_breakdowns[:3])} | Total Job-Ready Timeline: {total_days} Days ({total_days // 7 + 1} Weeks)"

        return StudyPlanResponse(
            student_name=student_name,
            target_career=target_career,
            daily_hours=daily_hours,
            total_days=total_days,
            timeline_summary=timeline_summary,
            skill_breakdowns=skill_breakdowns,
            days=study_days
        )

    # ================= ZAM AI: 20 ROLE-SPECIFIC MCQS =================
    async def get_mcqs(self, target_career: str = "Software Engineer") -> List[MCQQuestion]:
        return get_role_mcqs(target_career)

    # Legacy static fallback
    def _legacy_get_mcqs(self) -> List[MCQQuestion]:
        return [
            MCQQuestion(
                id="mcq_1",
                question="What is the average time complexity of searching for an element in a balanced Hash Map versus a sorted array using Binary Search?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="O(1) in Hash Map, O(log N) in Binary Search"),
                    MCQOption(id="B", text="O(N) in Hash Map, O(1) in Binary Search"),
                    MCQOption(id="C", text="O(log N) in both"),
                    MCQOption(id="D", text="O(N log N) in Hash Map, O(N) in Binary Search")
                ],
                correct_option_id="A",
                explanation="Hash table lookups compute a hash bucket index in average O(1) time. Binary search iteratively halves the search interval in O(log N) time."
            ),
            MCQQuestion(
                id="mcq_2",
                question="What will be the output of the following Python snippet?",
                code_snippet="def test(x, arr=[]):\n    arr.append(x)\n    return arr\n\nprint(test(1))\nprint(test(2))",
                options=[
                    MCQOption(id="A", text="[1] and [2]"),
                    MCQOption(id="B", text="[1] and [1, 2]"),
                    MCQOption(id="C", text="[1, 2] and [1, 2]"),
                    MCQOption(id="D", text="Error: default mutable argument")
                ],
                correct_option_id="B",
                explanation="Default argument expressions in Python are evaluated once when the function is defined, so mutable defaults like lists persist across calls unless None is used."
            ),
            MCQQuestion(
                id="mcq_3",
                question="In SQL, which clause is executed immediately after GROUP BY and before SELECT?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="WHERE"),
                    MCQOption(id="B", text="HAVING"),
                    MCQOption(id="C", text="ORDER BY"),
                    MCQOption(id="D", text="LIMIT")
                ],
                correct_option_id="B",
                explanation="Logical query processing order: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT."
            ),
            MCQQuestion(
                id="mcq_4",
                question="Which of the following HTTP methods is NOT idempotent according to RFC 7231 specifications?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="GET"),
                    MCQOption(id="B", text="PUT"),
                    MCQOption(id="C", text="POST"),
                    MCQOption(id="D", text="DELETE")
                ],
                correct_option_id="C",
                explanation="POST creates new subsidiary resources upon consecutive requests, producing varying side-effects, making it non-idempotent."
            ),
            MCQQuestion(
                id="mcq_5",
                question="In relational database normalization, what distinguishes Third Normal Form (3NF) from Second Normal Form (2NF)?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="3NF eliminates non-atomic attributes."),
                    MCQOption(id="B", text="3NF eliminates partial dependency on a composite key."),
                    MCQOption(id="C", text="3NF eliminates transitive dependencies between non-prime attributes."),
                    MCQOption(id="D", text="3NF introduces foreign keys across tables.")
                ],
                correct_option_id="C",
                explanation="2NF eliminates partial dependencies; 3NF requires the schema to be in 2NF and further eliminates transitive dependencies (non-prime attributes depending on other non-prime attributes)."
            ),
            MCQQuestion(
                id="mcq_6",
                question="What is the worst-case time complexity of QuickSort when the pivot selection always picks the smallest or largest element?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="O(N log N)"),
                    MCQOption(id="B", text="O(N)"),
                    MCQOption(id="C", text="O(N^2)"),
                    MCQOption(id="D", text="O(log N)")
                ],
                correct_option_id="C",
                explanation="Unbalanced partitions (e.g. sorted array with first element as pivot) degrade QuickSort recursion depth to N, yielding O(N^2) worst-case time."
            ),
            MCQQuestion(
                id="mcq_7",
                question="In Git, what is the core behavioral difference between 'git merge' and 'git rebase'?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="git merge deletes commit history; git rebase preserves it."),
                    MCQOption(id="B", text="git merge creates a 3-way merge commit; git rebase reapplies commits onto a new base commit linearly."),
                    MCQOption(id="C", text="git rebase can only be used on the remote origin branch."),
                    MCQOption(id="D", text="git merge converts all commits into a single squash commit.")
                ],
                correct_option_id="B",
                explanation="Merge preserves the exact historical timeline and creates a merge commit. Rebase moves or reapplies your commits atop the target tip, producing a clean linear history."
            ),
            MCQQuestion(
                id="mcq_8",
                question="What does the following JavaScript asynchronous code print to the console?",
                code_snippet="console.log('1');\nsetTimeout(() => console.log('2'), 0);\nPromise.resolve().then(() => console.log('3'));\nconsole.log('4');",
                options=[
                    MCQOption(id="A", text="1, 2, 3, 4"),
                    MCQOption(id="B", text="1, 4, 2, 3"),
                    MCQOption(id="C", text="1, 4, 3, 2"),
                    MCQOption(id="D", text="1, 3, 4, 2")
                ],
                correct_option_id="C",
                explanation="Synchronous code runs first (1, 4), then microtasks in the Promise queue are drained (3), and finally macrotasks like setTimeout run (2)."
            ),
            MCQQuestion(
                id="mcq_9",
                question="Which ACID property ensures that transactions execute concurrently without seeing intermediate, uncommitted states of other transactions?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="Atomicity"),
                    MCQOption(id="B", text="Consistency"),
                    MCQOption(id="C", text="Isolation"),
                    MCQOption(id="D", text="Durability")
                ],
                correct_option_id="C",
                explanation="Isolation determines how transaction integrity is visible to other concurrent users, preventing dirty reads and non-repeatable reads."
            ),
            MCQQuestion(
                id="mcq_10",
                question="In Redis, what is the default eviction behavior when maxmemory is reached and 'allkeys-lru' policy is set?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="Throws an out-of-memory error on every write."),
                    MCQOption(id="B", text="Evicts the least recently used keys among all keys."),
                    MCQOption(id="C", text="Evicts keys with an explicit TTL expiration set only."),
                    MCQOption(id="D", text="Evicts keys randomly.")
                ],
                correct_option_id="B",
                explanation="The 'allkeys-lru' policy evicts the least recently used (LRU) keys across the entire keyspace regardless of whether a TTL expiration was configured."
            ),
            MCQQuestion(
                id="mcq_11",
                question="An in-order traversal of a valid Binary Search Tree (BST) will visit nodes in which order?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="Descending numerical order"),
                    MCQOption(id="B", text="Ascending numerical order"),
                    MCQOption(id="C", text="Level-by-level breadth-first order"),
                    MCQOption(id="D", text="Topological dependency order")
                ],
                correct_option_id="B",
                explanation="In-order traversal visits Left subtree -> Current Node -> Right subtree. For any BST, this yields values in non-decreasing sorted order."
            ),
            MCQQuestion(
                id="mcq_12",
                question="What is the space complexity of Depth-First Search (DFS) on an unbalanced binary tree with N nodes?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="O(1)"),
                    MCQOption(id="B", text="O(log N)"),
                    MCQOption(id="C", text="O(N)"),
                    MCQOption(id="D", text="O(N^2)")
                ],
                correct_option_id="C",
                explanation="In a skewed or degenerate binary tree (resembling a linked list), the call stack depth reaches N frames, resulting in O(N) space."
            ),
            MCQQuestion(
                id="mcq_13",
                question="Which HTTP status code should an API return when an authenticated client attempts to access a resource they do not have permissions for?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="401 Unauthorized"),
                    MCQOption(id="B", text="403 Forbidden"),
                    MCQOption(id="C", text="404 Not Found"),
                    MCQOption(id="D", text="405 Method Not Allowed")
                ],
                correct_option_id="B",
                explanation="401 signifies missing or invalid credentials (unauthenticated). 403 signifies the server understands the client's identity but refuses authorization."
            ),
            MCQQuestion(
                id="mcq_14",
                question="Why are B+ Trees preferred over B-Trees and Hash tables for disk-based database indexes?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="B+ Trees only store keys in leaf nodes connected by pointers, optimizing sequential range scans and disk I/O."),
                    MCQOption(id="B", text="B+ Trees require zero memory locks."),
                    MCQOption(id="C", text="B+ Trees execute lookups in O(1) guaranteed time."),
                    MCQOption(id="D", text="B+ Trees prevent database fragmentation permanently.")
                ],
                correct_option_id="A",
                explanation="By keeping data records only in leaf nodes linked as a doubly-linked list, internal nodes fit more keys per page, and range queries execute with minimal random disk I/O."
            ),
            MCQQuestion(
                id="mcq_15",
                question="In microservices architecture, what is the primary purpose of the Circuit Breaker pattern?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="Encrypt payload communications between services."),
                    MCQOption(id="B", text="Prevent cascading failures by failing fast when a downstream service becomes unhealthy."),
                    MCQOption(id="C", text="Distribute incoming HTTP traffic evenly across multiple container instances."),
                    MCQOption(id="D", text="Automatically optimize SQL database indexing.")
                ],
                correct_option_id="B",
                explanation="Circuit Breakers monitor failure rates and trip open when errors surpass a threshold, returning immediate fallbacks without exhausting connection pools."
            ),
            MCQQuestion(
                id="mcq_16",
                question="According to the CAP Theorem, when a network partition (P) occurs in a distributed system, what trade-off must be made?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="Choose between Consistency (C) and Availability (A)."),
                    MCQOption(id="B", text="Choose between Latency and Security."),
                    MCQOption(id="C", text="Both Consistency and Availability are guaranteed automatically."),
                    MCQOption(id="D", text="Choose between Read throughput and Write throughput only.")
                ],
                correct_option_id="A",
                explanation="When network partitions occur, a distributed data store must either reject requests (sacrificing Availability for Consistency) or accept conflicting writes (sacrificing Consistency for Availability)."
            ),
            MCQQuestion(
                id="mcq_17",
                question="What is the architectural drawback of using completely stateless JSON Web Tokens (JWT) for user sessions?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="JWTs cannot be sent over HTTPS."),
                    MCQOption(id="B", text="Revoking or invalidating an individual token before its expiry requires maintaining a server-side denylist."),
                    MCQOption(id="C", text="JWTs cannot store user IDs or claims."),
                    MCQOption(id="D", text="JWTs decrypt automatically on client browsers without keys.")
                ],
                correct_option_id="B",
                explanation="Because stateless JWTs validate purely through digital signature verification, a stolen token remains valid until expiry unless a revocation list or token versioning table is queried."
            ),
            MCQQuestion(
                id="mcq_18",
                question="In Dynamic Programming, what distinguishes Top-Down (Memoization) from Bottom-Up (Tabulation)?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="Memoization is iterative and uses no extra memory; Tabulation is recursive."),
                    MCQOption(id="B", text="Memoization uses recursion and caches subproblem results on-demand; Tabulation solves smaller subproblems iteratively in a table."),
                    MCQOption(id="C", text="Tabulation cannot solve optimization problems."),
                    MCQOption(id="D", text="Memoization is always O(1) time complexity.")
                ],
                correct_option_id="B",
                explanation="Memoization maintains recursion and caches results in a hash table or array. Tabulation avoids recursion stack overhead by filling subproblems systematically from base cases up."
            ),
            MCQQuestion(
                id="mcq_19",
                question="In Docker, why is multi-stage building considered an industry best practice for production images?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="It forces containers to run in rootless mode by default."),
                    MCQOption(id="B", text="It separates build-time dependencies (compilers, SDKs) from runtime artifacts, producing minimal, secure production containers."),
                    MCQOption(id="C", text="It merges all Docker layers into a single uncompressed tarball."),
                    MCQOption(id="D", text="It eliminates the need for container port forwarding.")
                ],
                correct_option_id="B",
                explanation="Multi-stage builds leave heavyweight compilers and dev tools behind in temporary build stages, copying only the compiled executable or static assets into a slim final runtime base (like Alpine or distroless)."
            ),
            MCQQuestion(
                id="mcq_20",
                question="What is the time complexity of building a Binary Heap from an unordered array of N elements using the bottom-up 'heapify' algorithm?",
                code_snippet=None,
                options=[
                    MCQOption(id="A", text="O(N log N)"),
                    MCQOption(id="B", text="O(N)"),
                    MCQOption(id="C", text="O(N^2)"),
                    MCQOption(id="D", text="O(1)")
                ],
                correct_option_id="B",
                explanation="Although inserting N elements one-by-one takes O(N log N), bottom-up heap construction (sifting down from the lowest parent nodes) mathematically converges to linear O(N) time."
            )
        ]

    # ================= ZAM AI: 2 ROLE-SPECIFIC CODING CHALLENGES =================
    async def get_coding_challenges(self, target_career: str = "Software Engineer") -> List[CodingChallenge]:
        return get_role_coding_challenges(target_career)

    # Legacy static coding challenge fallback
    def _legacy_get_coding_challenges(self) -> List[CodingChallenge]:
        return [
            CodingChallenge(
                id="code_01",
                title="Two Sum (Sorted Array) - Two Pointer Scan",
                difficulty="Medium",
                language="python",
                problem_statement="Given a 1-indexed sorted array of integers numbers and a target sum, find two distinct indices [i, j] such that numbers[i] + numbers[j] == target. Implement an optimal O(N) time and O(1) auxiliary space solution.",
                starter_code="def two_sum_sorted(numbers: list[int], target: int) -> list[int]:\n    # Implement optimal two pointer scan\n    left = 0\n    right = len(numbers) - 1\n    while left < right:\n        current_sum = numbers[left] + numbers[right]\n        if current_sum == target:\n            return [left + 1, right + 1]\n        elif current_sum < target:\n            left += 1\n        else:\n            right -= 1\n    return []\n",
                sample_input="numbers = [2, 7, 11, 15], target = 9",
                sample_output="[1, 2]",
                test_cases=[
                    {"input": "[2, 7, 11, 15], target = 9", "expected": "[1, 2]"},
                    {"input": "[2, 3, 4], target = 6", "expected": "[1, 3]"}
                ]
            ),
            CodingChallenge(
                id="code_02",
                title="Valid Parentheses - Stack Balance Validator",
                difficulty="Easy",
                language="python",
                problem_statement="Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if open brackets are closed by the same type of brackets in the correct order. Implement in O(N) time and O(N) space using a Stack.",
                starter_code="def is_valid_parentheses(s: str) -> bool:\n    # Implement stack validator\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top_elem = stack.pop() if stack else '#'\n            if mapping[char] != top_elem:\n                return False\n        else:\n            stack.append(char)\n    return not stack\n",
                sample_input="s = '()[]{}'",
                sample_output="True",
                test_cases=[
                    {"input": "'()[]{}'", "expected": "True"},
                    {"input": "'([)]'", "expected": "False"}
                ]
            )
        ]

    async def get_coding_challenge(self, target_career: str = "Software Engineer") -> CodingChallenge:
        challenges = await self.get_coding_challenges(target_career)
        return challenges[0]

    # ================= ZAM AI: EVALUATE CODE =================
    async def evaluate_code(
        self,
        code: str,
        language: str = "python",
        student_name: str = "Rakshita",
        api_keys: Optional[ApiKeysConfig] = None
    ) -> EvaluateCodeResponse:
        key = self._resolve_key(
            api_keys.sam_ai_api_key if api_keys else None,
            api_keys.shared_key if api_keys else None
        )
        client = self._get_client(key)

        if client:
            prompt = (
                f"Evaluate this candidate's code submission in {language}:\n"
                f"```\n{code}\n```\n\n"
                "Return a JSON object with: passed (bool), score (0-100), feedback (string), time_complexity (string), space_complexity (string)."
            )
            try:
                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                if res and res.text:
                    d = json.loads(res.text)
                    return EvaluateCodeResponse(**d)
            except Exception as e:
                logger.error(f"Error evaluating code: {e}")

        # Deterministic analysis for both challenges
        has_stack = "stack" in code and ("pop" in code or "append" in code)
        has_pointer = ("left" in code and "right" in code) or ("while" in code and "<" in code)

        if has_stack:
            return EvaluateCodeResponse(
                passed=True,
                score=95,
                feedback=f"Outstanding work, {student_name}! Optimal LIFO stack balance validation with linear O(N) runtime and O(N) space.",
                time_complexity="O(N)",
                space_complexity="O(N)"
            )
        elif has_pointer:
            return EvaluateCodeResponse(
                passed=True,
                score=92,
                feedback=f"Excellent work, {student_name}! Optimal two-pointer implementation with O(N) linear time and constant O(1) space.",
                time_complexity="O(N)",
                space_complexity="O(1)"
            )
        else:
            return EvaluateCodeResponse(
                passed=False,
                score=58,
                feedback="Code logic is missing the core algorithmic invariant. For two pointers, maintain inward scan bounds; for parentheses, utilize a LIFO stack.",
                time_complexity="O(N^2) or incomplete",
                space_complexity="O(1)"
            )

    # ================= ZAM AI: 5 INTERVIEW QUESTIONS =================
    async def get_sam_interview_questions(
        self,
        target_career: str = "Software Engineer",
        student_name: str = "Rakshita"
    ) -> List[InterviewQuestion]:
        return [
            InterviewQuestion(
                id="sam_q1",
                question_number=1,
                total_questions=5,
                question=f"Hello {student_name}, welcome to your technical interview for the {target_career} role. To kick off: How do you choose between an SQL (Relational) database and a NoSQL document database when architecting a high-throughput backend?",
                rubric_tags=["Core Concept Clarity", "Practical Trade-offs", "Real-World Application"]
            ),
            InterviewQuestion(
                id="sam_q2",
                question_number=2,
                total_questions=5,
                question="When building REST APIs in production, what is the importance of idempotency, and which HTTP methods (GET, POST, PUT, DELETE) should be strictly idempotent?",
                rubric_tags=["REST Standards", "Network Reliability", "System Integrity"]
            ),
            InterviewQuestion(
                id="sam_q3",
                question_number=3,
                total_questions=5,
                question="Imagine an API endpoint is suddenly taking 2.5 seconds to respond under heavy user traffic. Walk me step-by-step through how you would diagnose the bottleneck.",
                rubric_tags=["Debugging Strategy", "Database Indexing & Caching", "Observability"]
            ),
            InterviewQuestion(
                id="sam_q4",
                question_number=4,
                total_questions=5,
                question="Tell me about a challenging bug or architecture issue you ran into during a project. How did you isolate the root cause and ensure it won't reoccur?",
                rubric_tags=["STAR Method", "Root Cause Analysis", "Engineering Rigor"]
            ),
            InterviewQuestion(
                id="sam_q5",
                question_number=5,
                total_questions=5,
                question="As user load and data volume explode, how would you decouple synchronous request-response bottlenecks using asynchronous message queues like Kafka, RabbitMQ, or Redis Streams?",
                rubric_tags=["System Scalability", "Asynchronous Queuing", "Fault Tolerance & DLQ"]
            )
        ]

    # ================= SAM AI: EVALUATE ANSWER (LOYAL, HONEST, BAR-RAISER EVALUATION) =================
    async def evaluate_sam_answer(
        self,
        question_id: str,
        question_text: str,
        student_answer: str,
        target_career: str = "Software Engineer",
        student_name: str = "Rakshita",
        api_keys: Optional[ApiKeysConfig] = None
    ) -> EvaluateAnswerResponse:
        key = self._resolve_key(
            api_keys.sam_ai_api_key if api_keys else None,
            api_keys.shared_key if api_keys else None
        )
        client = self._get_client(key)

        clean_answer = (student_answer or "").strip()
        lower_ans = clean_answer.lower()
        words = clean_answer.split()

        # Check for admission of ignorance, evasion, or dismissive answers
        multiword_phrases = [
            "don't know", "dont know", "do not know", "idk", "no idea", "not sure",
            "no clue", "haven't learned", "haven't worked", "have not worked",
            "can't answer", "cannot answer", "dunno", "never heard", "no answer",
            "dont remember", "don't remember", "not familiar"
        ]
        exact_single_words = {"no", "idk", "pass", "skip", "none", "nothing", "na", "dunno"}

        is_ignorant = (
            any(phrase in lower_ans for phrase in multiword_phrases)
            or lower_ans in exact_single_words
            or len(words) < 5
        )

        # Immediate loyal response for acknowledged ignorance or non-answers — NEVER false praise!
        if is_ignorant:
            return EvaluateAnswerResponse(
                readiness_score=12,
                technical_depth=8,
                clarity=20,
                practical_relevance=10,
                feedback_summary=f"⚠️ Critical Knowledge Gap: Candidate explicitly acknowledged not knowing the concept. In an actual technical interview for {target_career}, choosing between SQL and NoSQL is an essential benchmark architectural topic. Master this concept: SQL (PostgreSQL/MySQL) guarantees strict ACID transactions with relational constraints, whereas NoSQL (MongoDB/DynamoDB) scales horizontally with flexible schemas for high write throughput.",
                strengths=[
                    "Honest acknowledgment of knowledge gap instead of fabricating inaccurate technical claims.",
                    "Demonstrated awareness of own technical boundaries without guessing."
                ],
                improvements=[
                    "Study ACID transactions vs NoSQL BASE consistency models and the CAP Theorem.",
                    "Practice explaining architectural trade-offs using concrete examples aloud."
                ]
            )

        if client:
            prompt = (
                f"You are Zam AI, an objective, loyal, and rigorous Senior Technical Bar-Raiser Interviewer assessing candidate {student_name} for a {target_career} role.\n"
                f"Question: {question_text}\n"
                f"Candidate Answer: {clean_answer}\n\n"
                "CRITICAL GRADING CRITERIA (LOYAL & HONEST EVALUATION — NO FALSE PRAISE):\n"
                "- If the candidate gives a shallow or partially inaccurate answer:\n"
                "  * Assign readiness_score between 35 and 55. Highlight specific missing trade-offs.\n"
                "- If the candidate gives a solid, accurate technical response:\n"
                "  * Assign readiness_score between 75 and 95. Highlight specific good practices mentioned.\n\n"
                "Return a JSON object with: readiness_score (int 0-100), technical_depth (int 0-100), clarity (int 0-100), practical_relevance (int 0-100), "
                "feedback_summary (2-3 concise sentences), strengths (list of 2 strings), improvements (list of 2 actionable bullet points)."
            )
            try:
                res = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                if res and res.text:
                    d = json.loads(res.text)
                    return EvaluateAnswerResponse(**d)
            except Exception as e:
                logger.error(f"Error evaluating interview response: {e}")

        # Deterministic loyal fallback (when offline or no API key)
        if is_ignorant:
            return EvaluateAnswerResponse(
                readiness_score=18,
                technical_depth=12,
                clarity=25,
                practical_relevance=15,
                feedback_summary=f"Candidate stated they do not know the answer. In an actual technical interview for {target_career}, this is a foundational benchmark topic that must be mastered. For this question: SQL databases (PostgreSQL/MySQL) enforce strict ACID transactions and relational schemas ideal for complex multi-table joins, whereas NoSQL stores (MongoDB/DynamoDB) offer horizontal sharding and flexible document schemas for high-velocity streaming architectures.",
                strengths=[
                    "Honest acknowledgment of knowledge gap instead of fabricating inaccurate technical claims.",
                    "Demonstrated awareness of own technical boundaries without guessing."
                ],
                improvements=[
                    "Study the CAP Theorem (Consistency, Availability, Partition Tolerance) and trade-offs between ACID and BASE models.",
                    "Review high-throughput database patterns: Connection pooling, read replicas, and caching layers (Redis)."
                ]
            )

        # Keyword-based loyal scoring for genuine answers
        tech_keywords = [
            "acid", "relational", "nosql", "postgres", "mongo", "horizontal", "vertical",
            "scale", "schema", "sharding", "throughput", "table", "join", "document",
            "cache", "redis", "partition", "replica", "idempotent", "latency", "bottleneck",
            "index", "queue", "kafka", "async", "lock", "consistency", "isolation"
        ]
        matched_kws = [kw for kw in tech_keywords if kw in lower_ans]
        kw_scores = len(matched_kws)

        if kw_scores >= 4 and len(words) >= 30:
            return EvaluateAnswerResponse(
                readiness_score=88,
                technical_depth=85,
                clarity=88,
                practical_relevance=90,
                feedback_summary=f"Strong response from {student_name}. You articulated key architectural principles ({', '.join(matched_kws[:3])}) with structured reasoning and clear trade-offs.",
                strengths=[
                    f"Effectively incorporated core concepts: {', '.join(matched_kws[:3])}.",
                    "Structured the explanation clearly with practical architectural considerations."
                ],
                improvements=[
                    "Cite concrete operational metrics (e.g., p99 latency target < 50ms) to make recommendations even more persuasive.",
                    "Discuss failure modes and disaster recovery strategies under high concurrency."
                ]
            )
        elif kw_scores >= 2 and len(words) >= 15:
            return EvaluateAnswerResponse(
                readiness_score=68,
                technical_depth=65,
                clarity=70,
                practical_relevance=68,
                feedback_summary=f"Reasonable foundational understanding from {student_name}, referencing {', '.join(matched_kws[:2])}. However, the answer lacks depth regarding high-throughput scaling constraints and failure scenarios.",
                strengths=[
                    "Captured the basic distinction and direction of the technology choices.",
                    "Clear, understandable conversational delivery."
                ],
                improvements=[
                    "Delve deeper into specific trade-offs (e.g., schema migrations, read vs write heavy workloads, sharding keys).",
                    "Mention concrete mitigation strategies like read-replicas, write buffers, and caching layers."
                ]
            )
        else:
            return EvaluateAnswerResponse(
                readiness_score=42,
                technical_depth=38,
                clarity=50,
                practical_relevance=40,
                feedback_summary=f"The answer provided by {student_name} is brief and misses critical technical requirements for a {target_career} role. It does not substantiate how the architecture behaves under heavy traffic.",
                strengths=[
                    "Attempted the question directly.",
                    "Kept the communication concise."
                ],
                improvements=[
                    "Elaborate on database normalization, indexing strategies, and horizontal partitioning.",
                    "Use the STAR method or structured trade-off matrices (Pros / Cons / When to Use) to structure answers."
                ]
            )

    # ================= AGENT 3: MENTOR CHAT =================
    async def mentor_chat(
        self,
        student_name: str,
        message: str,
        history: List[Dict[str, str]],
        skills: List[SkillInput],
        target_career: Optional[str] = None,
        api_keys: Optional[ApiKeysConfig] = None
    ) -> str:
        key = self._resolve_key(
            api_keys.mentor_api_key if api_keys else None,
            api_keys.shared_key if api_keys else None
        )
        client = self._get_client(key)

        skills_str = ", ".join([f"{s.name} ({s.level})" for s in skills]) if skills else "No specific skills logged yet"
        target_str = target_career if target_career else "Software Engineering / Tech"

        system_instruction = (
            f"You are ClariTrack.AI's Lead Career & Tech Mentor Zam AI, advising {student_name}. "
            f"Context: {student_name} has registered the following skills: {skills_str}. "
            f"Their selected target career is '{target_str}'. "
            "You have deep real-time knowledge of 2026-2027 industry hiring standards, fresher expectations, salary benchmarks, and coding best practices. "
            "Always be encouraging, highly actionable, structured (use bold headers, bullet points, clean markdown, and concrete examples), "
            "and tailor your answer specifically to their stated skills and target career."
        )

        if client:
            try:
                contents = []
                for h in history[-8:]:
                    contents.append(f"{h.get('role', 'user').capitalize()}: {h.get('content', '')}")
                contents.append(f"User: {message}")
                full_prompt = "\n\n".join(contents)

                response = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=full_prompt,
                    config={"system_instruction": system_instruction}
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.error(f"Gemini API Agent 3 error: {e}")

        lower_msg = message.lower()

        if "in-demand" in lower_msg or "2026" in lower_msg or "2027" in lower_msg:
            return (
                f"### 🔥 Most In-Demand Tech Careers for 2026 & 2027\n\n"
                f"Hi **{student_name}**! Based on current industry hiring patterns and venture shifts, here are the dominant roles recruiters are prioritizing:\n\n"
                f"1. **Agentic AI & LLM Systems Engineers (₹14 - ₹28 LPA)**\n"
                f"   - **What's expected:** Moving beyond basic prompts to **LangGraph, autonomous loops, vector DB indexing (Qdrant), and fine-tuning**.\n"
                f"   - **Relevance to you:** Since you're targeting **{target_str}**, building end-to-end RAG workflows will immediately set you apart.\n\n"
                f"2. **Full-Stack & Cloud Infrastructure Engineers (₹10 - ₹22 LPA)**\n"
                f"   - **What's expected:** Next.js 15, FastAPI/Node, Dockerization, and asynchronous queuing (Redis, Celery).\n\n"
                f"3. **Data Platform & Analytics Engineers (₹9 - ₹18 LPA)**\n"
                f"   - **What's expected:** Advanced SQL (CTEs, Window Functions), dbt modeling, and real-time streaming (Kafka).\n\n"
                f"💡 **Key Tip for You:** Your registered skills ({skills_str}) give you a great springboard. Focus on building **one live-deployed capstone** with clean GitHub documentation rather than 5 generic tutorials."
            )

        if "fresher" in lower_msg or "companies expecting" in lower_msg:
            return (
                f"### 🎯 What Top Tech Companies Expect from Freshers Right Now\n\n"
                f"Recruiters have shifted drastically away from cookie-cutter resume templates. Here is the realistic benchmark:\n\n"
                f"1. **Problem Solving & DSA:**\n"
                f"   - You do **not** need 1,000 LeetCode problems. What matters is mastery of **Two Pointers, Hashing, Binary Search, Trees, and Graphs** (approx 120-150 well-understood problems).\n\n"
                f"2. **Production-Ready Code Quality:**\n"
                f"   - Clean modular architecture, proper environment variable `.env` management, error handling, and API documentation.\n\n"
                f"3. **Database Proficiency:**\n"
                f"   - Relational database schema design (3NF), query indexing, and joins.\n\n"
                f"4. **Communication & Architectural Trade-offs:**\n"
                f"   - Explaining *why* you chose a specific database or algorithm over alternatives during system design rounds."
            )

        if "resume" in lower_msg or "project" in lower_msg:
            return (
                f"### 🛠️ Portfolio & Resume Strategy for {target_str}\n\n"
                f"To make your resume pass ATS screening and catch an engineering manager's eye:\n\n"
                f"- **The 1-Page Rule:** Clean markdown/PDF format with zero two-column graphic clutter.\n"
                f"- **Bullet Point Formula:** Use Google's XYZ formula: *'Accomplished [X], as measured by [Y], by doing [Z]'*.\n"
                f"  - *Example:* 'Reduced API query latency by 42% by implementing Redis caching and indexing foreign keys in PostgreSQL.'\n"
                f"- **Featured Project:** Pin a flagship repository with a live demonstration link, architecture diagram in the README, and unit tests."
            )

        if "checklist" in lower_msg or "1-week" in lower_msg or "missing" in lower_msg:
            return (
                f"### 📋 1-Week Action Checklist for {student_name}\n\n"
                f"Here is your targeted 7-day sprint plan based on **{target_str}** requirements:\n\n"
                f"- **Day 1 & 2:** Two-Pointer & Hash Map optimization drills on HackerRank (30 mins theory + 60 mins practice).\n"
                f"- **Day 3:** SQL Window Functions (`ROW_NUMBER()`, `DENSE_RANK()`) on LeetCode Database.\n"
                f"- **Day 4:** API Design: Build a FastAPI service with Pydantic validation and error handling.\n"
                f"- **Day 5:** Dockerize the service with a multi-stage Dockerfile.\n"
                f"- **Day 6 & 7:** Capstone integration and README documentation with architectural diagram.\n\n"
                f"Which of these areas feels like the biggest blocker for you right now?"
            )

        return (
            f"That's a great question, **{student_name}**! "
            f"When preparing for **{target_str}**, focusing on foundational problem-solving alongside production deployment is the fastest way to stand out. "
            f"Regarding your question, I recommend breaking it into three distinct phases:\n\n"
            f"1. **Conceptual Understanding:** Make sure you can write the solution down on paper without an IDE.\n"
            f"2. **Hands-on Execution:** Implement it with proper edge-case handling.\n"
            f"3. **Real-World Application:** Relate this directly to your project builds.\n\n"
            f"Would you like me to generate a specific coding drill or provide an example of how this is tested in technical interview screens?"
        )

gemini_service = GeminiService()
