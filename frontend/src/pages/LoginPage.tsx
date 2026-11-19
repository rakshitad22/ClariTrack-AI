import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  ArrowRight,
  Quote,
  Lock,
  Mail,
  User,
  Eye,
  EyeOff,
  ShieldCheck,
  AlertCircle
} from 'lucide-react';
import { api, storage } from '../services/api';
import { UserSession } from '../types';

interface LoginPageProps {
  onLoginSuccess: (session: UserSession) => void;
}

const QUOTES = [
  {
    quote: "Every expert was once a beginner who refused to quit.",
    author: "Helen Hayes",
    tag: "Persistence & Growth"
  },
  {
    quote: "Small daily consistency beats intense last-minute cramming every single time.",
    author: "James Clear",
    tag: "Study Mastery"
  },
  {
    quote: "Build skills that solve real-world problems, and career opportunities will seek you out.",
    author: "Industry Mentor Wisdom",
    tag: "High-Yield Strategy"
  },
  {
    quote: "The best way to predict your software engineering career in 2026 is to build it.",
    author: "Tech Leadership",
    tag: "Future Proofing"
  }
];

export const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess }) => {
  const [isLoginTab, setIsLoginTab] = useState(false);
  const [name, setName] = useState('Rakshita');
  const [email, setEmail] = useState('rakshita@example.com');
  const [password, setPassword] = useState('password123');
  const [confirmPassword, setConfirmPassword] = useState('password123');

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [quoteIndex, setQuoteIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    const timer = setInterval(() => {
      setQuoteIndex((prev) => (prev + 1) % QUOTES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  // Clear errors when switching tabs
  const handleTabSwitch = (loginMode: boolean) => {
    setIsLoginTab(loginMode);
    setErrorMsg('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    if (!email.trim() || !password.trim()) {
      setErrorMsg('Please enter both email and password.');
      return;
    }

    if (!isLoginTab) {
      if (!name.trim()) {
        setErrorMsg('Please enter your full name or username.');
        return;
      }
      if (password !== confirmPassword) {
        setErrorMsg('Passwords do not match. Please verify your confirm password.');
        return;
      }
      if (password.length < 6) {
        setErrorMsg('Password should be at least 6 characters.');
        return;
      }
    }

    try {
      setLoading(true);
      setErrorMsg('');

      let session: UserSession;
      if (isLoginTab) {
        session = await api.login(email.trim(), password, name);
      } else {
        session = await api.signup(email.trim(), password, name.trim());
      }

      storage.setUser(session);
      onLoginSuccess(session);
    } catch (err: any) {
      console.error(err);
      const message = err.message || (isLoginTab ? 'Failed to log in. Please check your credentials.' : 'Failed to create account.');
      setErrorMsg(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-65px)] flex items-center justify-center p-4 lg:p-10 relative overflow-hidden">
      {/* Background Ambient Glow */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-purple-600/15 rounded-full blur-[128px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-emerald-600/15 rounded-full blur-[128px] pointer-events-none" />

      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
        {/* ================= LEFT PANEL: SLIDING MOTIVATIONAL QUOTES ================= */}
        <div className="lg:col-span-6 space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl overflow-hidden border border-white/15 shadow-xl shadow-purple-500/20 bg-[#14141b] flex items-center justify-center p-0.5">
              <img
                src="/claritrack-logo.jpg"
                alt="ClariTrack AI"
                className="w-full h-full object-cover object-[50%_28%] scale-[1.45] rounded-xl"
              />
            </div>
            <div>
              <div className="flex items-baseline">
                <span className="text-2xl lg:text-3xl font-bold tracking-tight text-white">
                  ClariTrack
                </span>
                <span className="text-2xl lg:text-3xl font-extrabold bg-gradient-to-r from-[#d946ef] via-[#a855f7] to-[#10b981] bg-clip-text text-transparent">
                  .AI
                </span>
              </div>
              <div className="text-xs text-zinc-400 font-medium">
                Know Where You Stand. Rehearse the Moment.
              </div>
            </div>
          </div>

          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/25 text-[#d946ef] text-xs font-semibold backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5" />
            <span>ClariTrack.AI • Personalized Student Success Network</span>
          </div>

          <div className="space-y-3">
            <h1 className="text-3xl lg:text-5xl font-extrabold text-white tracking-tight leading-tight">
              Master Your Tech Career with{' '}
              <span className="bg-gradient-to-r from-[#d946ef] via-purple-300 to-emerald-400 bg-clip-text text-transparent">
                ClariTrack.AI
              </span>
            </h1>
            <p className="text-sm text-slate-300 max-w-lg leading-relaxed">
              Input what you know today. ClariTrack.AI matches your skills to high-yield careers, constructs a day-by-day mastery schedule, conducts live Zam AI mock interviews, and guides you 24/7.
            </p>
          </div>

          {/* Motivational Quotes Card */}
          <div className="matte-card p-6 rounded-2xl relative overflow-hidden space-y-4 shadow-2xl border-white/[0.08]">
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-0.5 rounded-full bg-purple-500/20 text-[#d946ef] text-[10px] font-mono uppercase font-bold border border-purple-500/30">
                {QUOTES[quoteIndex].tag}
              </span>
              <Quote className="w-6 h-6 text-purple-400/30" />
            </div>

            <div className="min-h-[90px] flex items-center">
              <p className="text-base font-semibold text-slate-100 italic leading-relaxed transition-all duration-500">
                "{QUOTES[quoteIndex].quote}"
              </p>
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-white/5">
              <span className="text-xs font-bold text-slate-300">
                — {QUOTES[quoteIndex].author}
              </span>

              {/* Dot Indicators */}
              <div className="flex items-center gap-1.5">
                {QUOTES.map((_, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setQuoteIndex(idx)}
                    className={`h-1.5 rounded-full transition-all duration-300 ${
                      quoteIndex === idx ? 'w-6 bg-[#d946ef]' : 'w-1.5 bg-white/20 hover:bg-white/40'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* ================= RIGHT PANEL: UNIFIED LOGIN / SIGN-UP CARD ================= */}
        <div className="lg:col-span-6">
          <div className="matte-card p-8 rounded-3xl space-y-6 shadow-2xl border-white/[0.12] bg-[#14141c]/90 backdrop-blur-xl relative overflow-hidden">
            {/* Top Accent Gradient Line */}
            <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-[#d946ef] via-[#a855f7] to-[#10b981]" />

            {/* Tab Switcher */}
            <div className="grid grid-cols-2 p-1.5 rounded-2xl bg-[#0f0f15] border border-white/[0.08] text-xs font-bold shadow-inner">
              <button
                type="button"
                onClick={() => handleTabSwitch(false)}
                className={`py-3 rounded-xl transition-all font-semibold flex items-center justify-center gap-2 ${
                  !isLoginTab
                    ? 'btn-primary text-white shadow-lg font-bold'
                    : 'text-zinc-400 hover:text-white'
                }`}
              >
                <User className="w-3.5 h-3.5" />
                <span>Sign Up (New Student)</span>
              </button>
              <button
                type="button"
                onClick={() => handleTabSwitch(true)}
                className={`py-3 rounded-xl transition-all font-semibold flex items-center justify-center gap-2 ${
                  isLoginTab
                    ? 'btn-primary text-white shadow-lg font-bold'
                    : 'text-zinc-400 hover:text-white'
                }`}
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Log In</span>
              </button>
            </div>

            {/* Error Message Alert */}
            {errorMsg && (
              <div className="p-3.5 rounded-xl bg-rose-500/15 border border-rose-500/35 text-rose-300 text-xs font-medium flex items-start gap-2.5 animate-in fade-in slide-in-from-top-1 duration-200">
                <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                <span className="leading-relaxed">{errorMsg}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Full Name field ONLY in Signup Mode */}
              {!isLoginTab && (
                <div className="space-y-1.5 animate-in fade-in duration-200">
                  <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                    <User className="w-3.5 h-3.5 text-[#d946ef]" />
                    <span>Full Name / Username</span>
                  </label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Rakshita Sharma"
                    className="w-full matte-input px-4 py-3 text-xs font-medium text-white focus:border-[#d946ef] rounded-xl shadow-inner transition-colors"
                  />
                </div>
              )}

              {/* Email Address field for both */}
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Mail className="w-3.5 h-3.5 text-[#d946ef]" />
                  <span>Email Address</span>
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="rakshita@example.com"
                  className="w-full matte-input px-4 py-3 text-xs font-medium text-white focus:border-[#d946ef] rounded-xl shadow-inner transition-colors"
                />
              </div>

              {/* Password field with View Password toggle */}
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <Lock className="w-3.5 h-3.5 text-[#d946ef]" />
                  <span>Password</span>
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full matte-input px-4 py-3 pr-11 text-xs font-medium text-white focus:border-[#d946ef] rounded-xl shadow-inner transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white transition-colors"
                    title={showPassword ? 'Hide password' : 'View password'}
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4 text-zinc-400" />}
                  </button>
                </div>
              </div>

              {/* Confirm Password field ONLY in Signup Mode with View Password toggle */}
              {!isLoginTab && (
                <div className="space-y-1.5 animate-in fade-in duration-200">
                  <label className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Confirm Password</span>
                  </label>
                  <div className="relative">
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      required
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Re-enter your password"
                      className="w-full matte-input px-4 py-3 pr-11 text-xs font-medium text-white focus:border-emerald-500 rounded-xl shadow-inner transition-colors"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white transition-colors"
                      title={showConfirmPassword ? 'Hide password' : 'View password'}
                    >
                      {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4 text-zinc-400" />}
                    </button>
                  </div>
                </div>
              )}

              {/* Submit CTA Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 rounded-xl btn-primary text-xs font-bold uppercase tracking-wider text-white flex items-center justify-center gap-2 shadow-xl hover:shadow-purple-500/25 disabled:opacity-50 mt-6 transition-all hover:scale-[1.01]"
              >
                <span>{loading ? 'Authenticating...' : isLoginTab ? 'Log In to Platform →' : 'Create Account & Start →'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>

            {/* Bottom helper prompt */}
            <div className="pt-2 text-center text-xs text-zinc-400">
              {isLoginTab ? (
                <span>
                  New to ClariTrack.AI?{' '}
                  <button
                    type="button"
                    onClick={() => handleTabSwitch(false)}
                    className="text-[#d946ef] hover:underline font-bold"
                  >
                    Create an account here
                  </button>
                </span>
              ) : (
                <span>
                  Already have an account?{' '}
                  <button
                    type="button"
                    onClick={() => handleTabSwitch(true)}
                    className="text-emerald-400 hover:underline font-bold"
                  >
                    Log in here
                  </button>
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};