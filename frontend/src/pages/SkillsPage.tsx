import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Plus,
  Trash2,
  Compass,
  ArrowRight,
  TrendingUp,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { UserSession, SkillInput, CareerMatch, TopPickRecommendation } from '../types';
import { api, storage } from '../services/api';

interface SkillsPageProps {
  user: UserSession;
  onSelectCareer: (careerTitle: string) => void;
}

const POPULAR_SUGGESTIONS = [
  'Python', 'Java', 'SQL', 'React', 'Data Structures & Algorithms',
  'Machine Learning', 'FastAPI', 'Docker', 'Git', 'JavaScript'
];

export const SkillsPage: React.FC<SkillsPageProps> = ({ user, onSelectCareer }) => {
  const [skills, setSkills] = useState<SkillInput[]>(
    user.skills && user.skills.length > 0
      ? user.skills
      : [
          { name: 'Python', level: 'Advanced' },
          { name: 'SQL', level: 'Intermediate' },
          { name: 'React', level: 'Basic' }
        ]
  );

  const [careers, setCareers] = useState<CareerMatch[]>([]);
  const [topPick, setTopPick] = useState<TopPickRecommendation | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    handleAnalyze();
  }, []);

  const handleAddSkillRow = () => {
    setSkills([...skills, { name: '', level: 'Intermediate' }]);
  };

  const handleRemoveSkillRow = (index: number) => {
    const updated = [...skills];
    updated.splice(index, 1);
    setSkills(updated);
  };

  const handleSkillChange = (index: number, field: keyof SkillInput, val: any) => {
    const updated = [...skills];
    updated[index] = { ...updated[index], [field]: val };
    setSkills(updated);
  };

  const handleQuickAdd = (skillName: string) => {
    if (skills.some(s => s.name.toLowerCase() === skillName.toLowerCase())) return;
    setSkills([...skills, { name: skillName, level: 'Intermediate' }]);
  };

  const handleAnalyze = async () => {
    const validSkills = skills.filter(s => s.name.trim() !== '');
    if (validSkills.length === 0) return;

    try {
      setIsAnalyzing(true);
      storage.updateUser({ skills: validSkills });
      const res = await api.analyzeCareers(validSkills, user.name);
      setCareers(res.careers);
      if (res.top_pick) {
        setTopPick(res.top_pick);
      } else if (res.careers && res.careers.length > 0) {
        const top = res.careers[0];
        setTopPick({
          career_title: top.title,
          match_percentage: top.match_percentage,
          why_recommended: `I recommend **${top.title}** for you, ${user.name}—you've already built a strong foundation in **${top.matched_skills.slice(0, 3).join(', ')}**, which gives you an immediate competitive edge for 2026-2027 entry-level roles.`,
          mastered_skills_summary: `Mastered: ${top.matched_skills.slice(0, 3).join(', ')}`,
          remaining_skills_summary: `Learning just **${top.missing_skills.slice(0, 3).join(', ')}** is enough to master this particular role and become 100% placement-ready.`,
          action_note: 'Select this recommended role below to auto-generate your step-by-step master roadmap.'
        });
      }
    } catch (err) {
      console.error('Error analyzing careers:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleChooseCareer = (careerTitle: string) => {
    storage.updateUser({ target_career: careerTitle });
    onSelectCareer(careerTitle);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* ================= GREETING HEADER ================= */}
      <div className="matte-card p-6 relative overflow-hidden">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/25 text-[#d946ef] text-xs font-semibold mb-1">
            <Compass className="w-3.5 h-3.5" />
            <span>ClariTrack.AI • Career Intelligence & Role Matcher</span>
          </div>

          <h1 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
            Hi, {user.name}! 👋
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
            Tell ClariTrack.AI what you know, and our neural matching engine will calculate your highest-matching career paths.
          </p>
        </div>
      </div>

      {/* ================= TWO-COLUMN WORKSPACE ================= */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* ================= LEFT COLUMN: DYNAMIC SKILL BUILDER ================= */}
        <div className="lg:col-span-5 matte-card p-6 space-y-6 sticky top-20">
          <div className="border-b border-white/[0.08] pb-4">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#d946ef]" />
              <span>Dynamic Skill Builder</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Type your skills and pick a proficiency tier.
            </p>
          </div>

          {/* Quick-add chips */}
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold text-slate-400">Quick Suggestions:</span>
            <div className="flex flex-wrap gap-1.5">
              {POPULAR_SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => handleQuickAdd(s)}
                  className="px-2.5 py-1 rounded-lg bg-[#14141b] hover:bg-white/[0.08] border border-white/5 hover:border-purple-500/30 text-slate-300 hover:text-[#d946ef] text-[11px] font-medium transition-colors"
                >
                  + {s}
                </button>
              ))}
            </div>
          </div>

          {/* Skill Rows */}
          <div className="space-y-3 max-h-[360px] overflow-y-auto pr-1">
            {skills.map((skill, index) => (
              <div
                key={index}
                className="flex items-center gap-2 p-2 rounded-xl bg-[#14141b] border border-white/5 hover:border-white/15 transition-all"
              >
                <input
                  type="text"
                  value={skill.name}
                  onChange={(e) => handleSkillChange(index, 'name', e.target.value)}
                  placeholder="Type your skill here (e.g., Python, SQL)..."
                  className="flex-1 matte-input px-3 py-2 text-xs font-semibold text-white"
                />

                <select
                  value={skill.level}
                  onChange={(e) => handleSkillChange(index, 'level', e.target.value as any)}
                  className="matte-input px-2.5 py-2 text-xs font-semibold text-[#d946ef]"
                >
                  <option value="Basic" className="bg-[#14141b] text-slate-200">Basic</option>
                  <option value="Intermediate" className="bg-[#14141b] text-slate-200">Intermediate</option>
                  <option value="Advanced" className="bg-[#14141b] text-slate-200">Advanced</option>
                </select>

                <button
                  type="button"
                  onClick={() => handleRemoveSkillRow(index)}
                  className="p-2 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 rounded-xl transition-colors"
                  title="Remove skill"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* + Add One More Skill Button */}
          <button
            type="button"
            onClick={handleAddSkillRow}
            className="w-full py-2.5 rounded-xl border border-dashed border-purple-500/40 hover:border-[#d946ef] bg-purple-500/5 hover:bg-purple-500/10 text-purple-300 text-xs font-bold flex items-center justify-center gap-2 transition-all"
          >
            <Plus className="w-4 h-4 text-[#d946ef]" />
            <span>+ Add One More Skill</span>
          </button>

          {/* Primary CTA */}
          <button
            type="button"
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className="w-full py-3.5 rounded-xl btn-primary text-xs font-extrabold flex items-center justify-center gap-2 shadow-xl disabled:opacity-50 tracking-wider uppercase"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isAnalyzing ? 'Analyzing Roles & Benchmarks...' : 'Analyze My Skills & Show Career Paths'}</span>
          </button>
        </div>

        {/* ================= RIGHT COLUMN: CAREER MATCH RESULTS ================= */}
        <div className="lg:col-span-7 space-y-5">
          {/* Featured Zam AI Top Pick Recommendation Spotlight */}
          {topPick && !isAnalyzing && (
            <div className="relative overflow-hidden rounded-2xl p-6 bg-gradient-to-br from-[#1b1427] via-[#161622] to-[#121c19] border border-emerald-500/40 shadow-[0_0_25px_rgba(16,185,129,0.14)] space-y-4 animate-in fade-in">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs font-bold tracking-wider uppercase font-mono shadow-sm">
                  <Sparkles className="w-3.5 h-3.5 text-[#d946ef] animate-pulse" />
                  ★ ZAM AI TOP PICK FOR YOU
                </span>
                <span className="text-xs font-mono font-extrabold text-emerald-400 bg-emerald-950/40 px-3 py-1 rounded-full border border-emerald-500/20">
                  {topPick.match_percentage}% Match
                </span>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-black text-white tracking-tight flex items-center gap-2">
                  <span>{topPick.career_title}</span>
                </h3>
                <p className="text-xs text-zinc-300 leading-relaxed">
                  {topPick.why_recommended.split('**').map((chunk, i) =>
                    i % 2 === 1 ? <strong key={i} className="text-white font-bold">{chunk}</strong> : chunk
                  )}
                </p>
                <div className="p-3 rounded-xl bg-black/40 border border-white/5 text-xs text-zinc-300 space-y-1 font-mono">
                  <div className="text-emerald-400 font-semibold text-[11px]">
                    ✓ {topPick.mastered_skills_summary}
                  </div>
                  <div className="text-purple-300 font-medium text-[11px]">
                    ⚡ {topPick.remaining_skills_summary}
                  </div>
                </div>
              </div>

              <button
                type="button"
                onClick={() => handleChooseCareer(topPick.career_title)}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl btn-primary text-xs font-bold uppercase tracking-wider text-white shadow-xl hover:scale-[1.02] transition-all flex items-center justify-center gap-2"
              >
                <span>Choose This Recommended Career →</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-extrabold text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                <span>Recommended Career Paths</span>
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Strictly ordered from highest match percentage to lowest.
              </p>
            </div>
            <span className="text-[11px] font-mono px-2.5 py-1 rounded-full bg-white/5 text-slate-300 border border-white/10">
              {careers.length} Matches Found
            </span>
          </div>

          {isAnalyzing ? (
            <div className="p-12 matte-card text-center space-y-3">
              <div className="w-8 h-8 border-2 border-[#d946ef] border-t-transparent rounded-full animate-spin mx-auto" />
              <p className="text-xs text-slate-300 font-semibold">
                Agent 1 is evaluating skill matrices against 2026-2027 industry requisites...
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {careers.map((career) => {
                const match = career.match_percentage;
                const isTop = match >= 75;

                return (
                  <div
                    key={career.id}
                    className="matte-card matte-card-hover p-6 space-y-4"
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-base font-bold text-white">
                            {career.title}
                          </h3>
                          <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-mono font-semibold border border-emerald-500/20">
                            {career.market_demand}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                          {career.description}
                        </p>
                        <div className="text-[11px] font-mono text-emerald-300 font-semibold mt-1">
                          Benchmark Salary: {career.average_salary}
                        </div>
                      </div>

                      {/* Percentage Match Radial Gauge */}
                      <div className="flex items-center gap-3 p-3 rounded-2xl bg-[#14141b] border border-white/5 flex-shrink-0 self-start sm:self-auto">
                        <div className="text-right">
                          <div className="text-[10px] uppercase font-bold text-slate-400">Match</div>
                          <div className={`text-xl font-extrabold font-mono ${
                            isTop ? 'text-emerald-400' : match >= 60 ? 'text-[#d946ef]' : 'text-amber-400'
                          }`}>
                            {match}%
                          </div>
                        </div>

                        <div className="relative w-11 h-11 flex items-center justify-center">
                          <svg className="w-11 h-11 transform -rotate-90">
                            <circle
                              cx="22"
                              cy="22"
                              r="18"
                              stroke="currentColor"
                              strokeWidth="3.5"
                              className="text-white/10"
                              fill="transparent"
                            />
                            <circle
                              cx="22"
                              cy="22"
                              r="18"
                              stroke={isTop ? '#10b981' : match >= 60 ? '#d946ef' : '#fbbf24'}
                              strokeWidth="3.5"
                              fill="transparent"
                              strokeDasharray="113.1"
                              strokeDashoffset={113.1 - (113.1 * match) / 100}
                              strokeLinecap="round"
                            />
                          </svg>
                        </div>
                      </div>
                    </div>

                    {/* Matched vs Missing Skills */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1 text-xs">
                      <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-1">
                        <span className="text-emerald-300 font-bold text-[10px] uppercase flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3 text-emerald-400" /> Matched Skills:
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {career.matched_skills.map((s, idx) => (
                            <span key={idx} className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[10px] font-medium">
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="p-2.5 rounded-xl bg-rose-950/20 border border-rose-500/20 space-y-1">
                        <span className="text-rose-400 font-bold text-[10px] uppercase flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" /> Missing Skill Gaps:
                        </span>
                        <div className="flex flex-wrap gap-1">
                          {career.missing_skills.map((s, idx) => (
                            <span key={idx} className="px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 text-[10px] font-medium">
                              {s}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Action Button: Choose & Build Study Plan */}
                    <div className="pt-2 border-t border-white/5 flex items-center justify-between">
                      <span className="text-xs text-slate-400">
                        Estimated {career.timeline_weeks} weeks to complete readiness
                      </span>

                      <button
                        type="button"
                        onClick={() => handleChooseCareer(career.title)}
                        className="px-4 py-2 rounded-xl btn-primary text-xs font-bold flex items-center gap-1.5 shadow-lg"
                      >
                        <span>Choose Career & Build Study Plan →</span>
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
