import React, { useState, useEffect } from 'react';
import {
  Calendar,
  Clock,
  Sparkles,
  CheckSquare,
  Square,
  Play,
  ExternalLink,
  BookOpen,
  ArrowRight,
  MessageSquare,
  Mic,
  Layers
} from 'lucide-react';
import { UserSession, StudyPlanResponse } from '../types';
import { api, storage } from '../services/api';
import { VideoModal } from '../components/VideoModal';

interface StudyPlanPageProps {
  user: UserSession;
  onNavigateToMentor: () => void;
  onNavigateToSkills: () => void;
  onNavigateToSamAi: () => void;
}

export const StudyPlanPage: React.FC<StudyPlanPageProps> = ({
  user,
  onNavigateToMentor,
  onNavigateToSkills,
  onNavigateToSamAi
}) => {
  const targetCareer = user.target_career || 'Software Engineer';
  const [dailyHours, setDailyHours] = useState(user.daily_hours || 2);
  const [plan, setPlan] = useState<StudyPlanResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeVideo, setActiveVideo] = useState<{ title: string; url: string } | null>(null);

  useEffect(() => {
    handleGeneratePlan();
  }, [targetCareer]);

  const handleGeneratePlan = async (hours: number = dailyHours) => {
    try {
      setLoading(true);
      storage.updateUser({ daily_hours: hours, target_career: targetCareer });
      const skills = user.skills || [{ name: 'Python', level: 'Advanced' }];
      const res = await api.generateStudyPlan(targetCareer, skills, hours, user.name);

      // Check localStorage for previously checked days
      const savedChecksKey = `completed_days_${targetCareer}`;
      const savedChecks = localStorage.getItem(savedChecksKey);
      if (savedChecks) {
        try {
          const checkedSet = new Set(JSON.parse(savedChecks));
          res.days = res.days.map(d => ({ ...d, completed: checkedSet.has(d.day) }));
        } catch {}
      } else {
        // Initial Checked State: Mark Day 1 and Day 2 checked by default
        res.days = res.days.map(d => ({ ...d, completed: d.day <= 2 }));
        localStorage.setItem(savedChecksKey, JSON.stringify([1, 2]));
      }

      setPlan(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleHourSelect = (hours: number) => {
    setDailyHours(hours);
    handleGeneratePlan(hours);
  };

  const handleToggleDayComplete = (dayNum: number) => {
    if (!plan) return;
    const updatedDays = plan.days.map((d) =>
      d.day === dayNum ? { ...d, completed: !d.completed } : d
    );
    setPlan({ ...plan, days: updatedDays });

    // Persist completed days in localStorage
    const completedDayNums = updatedDays.filter(d => d.completed).map(d => d.day);
    localStorage.setItem(`completed_days_${targetCareer}`, JSON.stringify(completedDayNums));
  };

  const completedCount = plan ? plan.days.filter((d) => d.completed).length : 0;
  const totalCount = plan ? plan.days.length : 1;
  const progressPct = Math.round((completedCount / totalCount) * 100);

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* ================= HEADER & ZAM AI QUICK-LINK CTA ================= */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 text-[#d946ef] text-xs font-semibold border border-purple-500/25 mb-2">
            <Calendar className="w-3.5 h-3.5" />
            <span>ClariTrack.AI • Master Schedule & Action Roadmap</span>
          </div>
          <h1 className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
            Personalized Master Schedule
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
            Skill-by-skill, day-by-day roadmap with exact concept/practice splits and verified reference links.
          </p>
        </div>

        {/* Top Navigation CTAs */}
        <div className="flex items-center gap-3">
          <button
            onClick={onNavigateToSamAi}
            className="px-4 py-2.5 rounded-xl btn-primary text-xs font-bold flex items-center gap-2 shadow-lg"
          >
            <Mic className="w-4 h-4" />
            <span>Zam AI Mock Interview 🎙️ →</span>
          </button>

          <button
            onClick={onNavigateToMentor}
            className="px-4 py-2.5 rounded-xl bg-[#1b1b24] hover:bg-[#22222e] text-slate-200 border border-white/10 text-xs font-bold flex items-center gap-2 transition-colors"
          >
            <MessageSquare className="w-4 h-4 text-purple-400" />
            <span>AI Mentor Chat 💬 →</span>
          </button>
        </div>
      </div>

      {/* ================= TRIGGER & CONFIRMATION BLOCK ================= */}
      <div className="matte-card p-6 space-y-5">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
          <div className="space-y-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Active Focus Track
            </span>
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-extrabold text-white">
                Target Career Selected: <span className="text-[#d946ef]">{targetCareer}</span>
              </h2>
              <button
                onClick={onNavigateToSkills}
                className="text-xs text-purple-400 hover:text-purple-300 underline font-semibold"
              >
                (Switch Role)
              </button>
            </div>
          </div>

          {/* Daily Study Hours Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center gap-3">
            <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-cyan-400" />
              <span>Daily Commitment:</span>
            </span>

            <div className="flex items-center gap-1.5 bg-[#14141b] p-1 rounded-2xl border border-white/10">
              {[1, 2, 3, 4].map((hr) => (
                <button
                  key={hr}
                  type="button"
                  onClick={() => handleHourSelect(hr)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    dailyHours === hr
                      ? 'btn-primary text-white shadow-md'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {hr} hr/day {hr === 2 && '⭐'}
                </button>
              ))}
            </div>

            <button
              onClick={() => handleGeneratePlan(dailyHours)}
              disabled={loading}
              className="px-4 py-2 rounded-xl btn-primary text-xs font-extrabold flex items-center gap-1.5 shadow-lg disabled:opacity-50"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>{loading ? 'Structuring...' : 'Generate My Complete Study Plan 🚀'}</span>
            </button>
          </div>
        </div>

        {/* Total Days to Master Summary & Progress Bar */}
        {plan && (
          <div className="space-y-4 pt-1">
            <div className="p-4 rounded-2xl bg-[#14141b] border border-white/[0.08] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="space-y-1">
                <span className="text-[10px] font-mono uppercase tracking-wider text-[#d946ef] font-bold">
                  Total Days to Master Summary
                </span>
                <p className="text-xs font-bold text-white">
                  {plan.timeline_summary}
                </p>
              </div>

              {/* Completion Tracker */}
              <div className="flex items-center gap-3 flex-shrink-0">
                <div className="text-right">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold">Mastery Progress</span>
                  <div className="text-sm font-extrabold text-emerald-400 font-mono">
                    {completedCount} of {totalCount} Days ({progressPct}%)
                  </div>
                </div>
              </div>
            </div>

            {/* Linear Progress Bar */}
            <div className="w-full h-2 rounded-full bg-white/5 overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-[#d946ef] via-[#8b5cf6] to-[#10b981] transition-all duration-500 rounded-full"
                style={{ width: `${progressPct}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* ================= DAILY BREAKDOWN CARDS ================= */}
      {loading ? (
        <div className="p-16 matte-card text-center space-y-3">
          <div className="w-8 h-8 border-2 border-[#d946ef] border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-300 font-semibold">
            Agent 2 is grounding curriculum against official docs and verified video tutorials...
          </p>
        </div>
      ) : plan ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              Day-by-Day Execution Modules
            </h3>
            <span className="text-xs text-slate-400">
              Day 1 & Day 2 completed by default • Check off days as you master topics
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {plan.days.map((item) => (
              <div
                key={item.day}
                className={`p-5 rounded-2xl border transition-all space-y-3.5 flex flex-col justify-between ${
                  item.completed
                    ? 'bg-emerald-950/15 border-emerald-500/30'
                    : 'matte-card border-white/[0.08] hover:border-white/20'
                }`}
              >
                <div className="space-y-3">
                  {/* Top Day Header & Checkbox */}
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-center gap-2.5">
                      <button
                        type="button"
                        onClick={() => handleToggleDayComplete(item.day)}
                        className="text-slate-400 hover:text-emerald-400 transition-colors"
                        title={item.completed ? 'Mark Incomplete' : 'Mark Completed'}
                      >
                        {item.completed ? (
                          <CheckSquare className="w-5 h-5 text-emerald-400" />
                        ) : (
                          <Square className="w-5 h-5 text-slate-500" />
                        )}
                      </button>

                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono font-extrabold text-cyan-400">
                            Day {item.day}
                          </span>
                          <span className="px-2 py-0.2 rounded-full bg-white/5 text-slate-300 text-[10px] font-mono border border-white/5">
                            {item.skill}
                          </span>
                        </div>
                        <h4 className={`text-sm font-bold mt-0.5 ${
                          item.completed ? 'text-slate-300 line-through opacity-80' : 'text-white'
                        }`}>
                          {item.subtopic}
                        </h4>
                      </div>
                    </div>

                    <div className="text-[10px] font-mono px-2 py-0.5 rounded-lg bg-black/40 text-purple-300 border border-purple-500/20 flex-shrink-0">
                      {dailyHours}h Commitment
                    </div>
                  </div>

                  {/* Exact time allocation split */}
                  <div className="text-[11px] text-slate-400 bg-[#14141b] p-2 rounded-xl border border-white/5 font-mono">
                    ⏱️ <span className="text-slate-200">{item.time_allocation}</span>
                  </div>

                  {/* Specific Practice Platform Instructions */}
                  <div className="p-2.5 rounded-xl bg-black/40 border border-white/5 text-xs space-y-0.5">
                    <span className="text-cyan-300 font-semibold text-[11px] block">
                      Target Practice Track ({item.platform}):
                    </span>
                    <p className="text-slate-300 font-mono text-[11px]">
                      {item.practice_track}
                    </p>
                  </div>
                </div>

                {/* Real Reference Links (Verified YouTube + Official Docs) */}
                <div className="pt-2 border-t border-white/5 flex items-center justify-between text-xs">
                  <button
                    type="button"
                    onClick={() => setActiveVideo({ title: item.reference_title, url: item.reference_url })}
                    className="text-purple-400 hover:text-purple-300 flex items-center gap-1.5 font-semibold group"
                  >
                    <div className="p-1 rounded-lg bg-purple-500/20 group-hover:bg-purple-500/30 text-purple-400">
                      <Play className="w-3 h-3 fill-current" />
                    </div>
                    <span className="truncate max-w-[200px]">{item.reference_title}</span>
                  </button>

                  <a
                    href={item.docs_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-slate-400 hover:text-slate-200 flex items-center gap-1 text-[11px]"
                  >
                    <BookOpen className="w-3.5 h-3.5" />
                    <span>Official Docs</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {/* ================= BOTTOM CTAS ================= */}
      <div className="matte-card p-6 text-center space-y-4">
        <h3 className="text-base font-bold text-white">
          Ready to test your knowledge or need personalized advice?
        </h3>
        <p className="text-xs text-slate-400 max-w-lg mx-auto">
          Take a live technical screening in Zam AI Mock Interview or chat 24/7 with our AI Career & Tech Mentor.
        </p>
        <div className="flex items-center justify-center gap-3">
          <button
            onClick={onNavigateToSamAi}
            className="px-6 py-3 rounded-2xl btn-primary text-xs font-bold inline-flex items-center gap-2 shadow-lg"
          >
            <Mic className="w-4 h-4" />
            <span>Launch Zam AI Mock Interview 🎙️ →</span>
          </button>

          <button
            onClick={onNavigateToMentor}
            className="px-6 py-3 rounded-2xl bg-[#14141b] hover:bg-[#22222e] text-slate-200 border border-white/10 text-xs font-bold inline-flex items-center gap-2 transition-colors"
          >
            <MessageSquare className="w-4 h-4 text-purple-400" />
            <span>Ask AI Career & Tech Mentor 💬 →</span>
          </button>
        </div>
      </div>

      {/* Video Modal Player */}
      <VideoModal
        video={activeVideo}
        onClose={() => setActiveVideo(null)}
      />
    </div>
  );
};
