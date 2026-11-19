import React, { useState, useRef, useEffect } from 'react';
import {
  Sparkles,
  Bot,
  X,
  Send,
  Maximize2,
  User,
  RotateCcw,
  MessageSquare
} from 'lucide-react';
import { UserSession, ChatMessage } from '../types';
import { api } from '../services/api';

interface FloatingZamMentorProps {
  user: UserSession | null;
  currentPage: string;
  onNavigateToMentor: () => void;
}

const QUICK_PROMPTS = [
  "What are in-demand 2026 tech careers?",
  "Fresher hiring expectations?",
  "Review my study roadmap."
];

export const FloatingZamMentor: React.FC<FloatingZamMentorProps> = ({
  user,
  currentPage,
  onNavigateToMentor
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: `👋 **Hi! I'm Zam AI**, your personal career and technical mentor. I'm connected to your profile and target goals. How can I help you accelerate today?`
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, isLoading]);

  // Don't show floating launcher if already on the dedicated full-page /mentor view or not logged in
  if (!user || currentPage === 'mentor') {
    return null;
  }

  const handleSend = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query || isLoading) return;

    const userMsg: ChatMessage = { role: 'user', content: query };
    const newHistory = [...messages, userMsg];
    setMessages(newHistory);
    setInput('');
    setIsLoading(true);

    try {
      const res = await api.mentorChat(
        query,
        newHistory,
        user.name,
        user.skills || [],
        user.target_career
      );
      setMessages(prev => [...prev, { role: 'assistant', content: res.reply }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "I had a temporary hiccup. Let's try that question once more!"
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {/* ================= EXPANDED SLIDE-OVER CHAT DRAWER ================= */}
      {isOpen && (
        <div className="w-[360px] sm:w-[410px] h-[520px] max-h-[82vh] bg-[#161620] border border-white/15 shadow-[0_10px_40px_rgba(0,0,0,0.7)] rounded-2xl flex flex-col overflow-hidden mb-4 animate-in slide-in-from-bottom-4 fade-in duration-200">
          {/* Header */}
          <div className="p-3.5 px-4 bg-[#14141d] border-b border-white/[0.08] flex items-center justify-between flex-shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#d946ef] to-[#8b5cf6] p-[1.5px] shadow-md shadow-purple-500/25">
                <div className="w-full h-full bg-[#111116] rounded-[10px] flex items-center justify-center">
                  <Bot className="w-4 h-4 text-[#d946ef]" />
                </div>
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-bold text-white">Zam AI</span>
                  <span className="text-[9px] uppercase font-mono px-1.5 py-0.2 rounded bg-purple-500/15 text-purple-300 border border-purple-500/30">
                    Mentor
                  </span>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse ml-0.5" />
                </div>
                <div className="text-[10px] text-zinc-400 truncate max-w-[200px]">
                  Target: {user.target_career || 'Software Engineer'}
                </div>
              </div>
            </div>

            <div className="flex items-center gap-1.5 text-zinc-400">
              <button
                type="button"
                onClick={() => {
                  setIsOpen(false);
                  onNavigateToMentor();
                }}
                className="p-1.5 rounded-lg hover:text-white hover:bg-white/[0.06] transition-colors"
                title="Open full page mentor chat"
              >
                <Maximize2 className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg hover:text-white hover:bg-white/[0.06] transition-colors"
                title="Minimize Zam AI"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-3.5 space-y-3.5 text-xs">
            {messages.map((m, idx) => {
              const isUser = m.role === 'user';
              return (
                <div
                  key={idx}
                  className={`flex gap-2 ${isUser ? 'ml-auto flex-row-reverse max-w-[85%]' : 'mr-auto max-w-[92%]'}`}
                >
                  <div className={`w-6 h-6 rounded-lg flex items-center justify-center flex-shrink-0 text-[10px] font-bold ${
                    isUser
                      ? 'bg-gradient-to-tr from-cyan-500 to-emerald-400 text-black'
                      : 'bg-gradient-to-tr from-[#d946ef] to-[#8b5cf6] text-white'
                  }`}>
                    {isUser ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
                  </div>

                  <div className={`p-3 rounded-xl leading-relaxed whitespace-pre-wrap ${
                    isUser
                      ? 'bg-purple-500/20 border border-purple-500/35 text-white'
                      : 'bg-[#1b1b26] border border-white/[0.08] text-zinc-200'
                  }`}>
                    {m.content}
                  </div>
                </div>
              );
            })}

            {isLoading && (
              <div className="flex items-center gap-2 text-zinc-400 text-[11px] italic pl-8">
                <span className="w-1.5 h-1.5 rounded-full bg-[#d946ef] animate-ping" />
                <span>Zam AI is thinking...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompts */}
          <div className="px-3 py-1.5 bg-[#14141d]/80 border-t border-white/[0.05] flex items-center gap-1.5 overflow-x-auto no-scrollbar">
            {QUICK_PROMPTS.map((prompt, pIdx) => (
              <button
                key={pIdx}
                type="button"
                onClick={() => handleSend(prompt)}
                className="whitespace-nowrap px-2.5 py-1 rounded-lg bg-white/[0.04] hover:bg-white/[0.08] border border-white/5 text-[10px] text-zinc-300 hover:text-white transition-colors"
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Chat Input */}
          <div className="p-2.5 bg-[#14141d] border-t border-white/[0.08]">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-1.5"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask Zam AI anything..."
                className="flex-1 bg-[#1c1c28] border border-white/10 rounded-xl px-3 py-2 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-[#d946ef]"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="p-2 rounded-xl btn-primary text-white disabled:opacity-40 transition-opacity flex-shrink-0"
              >
                <Send className="w-3.5 h-3.5" />
              </button>
            </form>
          </div>
        </div>
      )}

      {/* ================= FLOATING DANCING & SPARKLING LAUNCHER BUTTON ================= */}
      <div className="relative flex items-center">
        {/* Tooltip / Speech Bubble */}
        {!isOpen && (
          <div
            className={`absolute right-full mr-3.5 top-7 -translate-y-1/2 pointer-events-none transition-all duration-300 ease-out ${
              isHovered ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-2'
            }`}
          >
            <div className="relative px-3.5 py-1.5 rounded-xl bg-[#181824]/95 border border-white/15 text-xs font-semibold text-white whitespace-nowrap shadow-2xl backdrop-blur-md flex items-center gap-1.5">
              <span>Hi, I'm Zam AI. Ask me!</span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              {/* Subtle Pointer Arrow pointing to the button */}
              <div className="absolute top-1/2 -right-1.5 -translate-y-1/2 w-3 h-3 bg-[#181824] border-t border-r border-white/15 transform rotate-45" />
            </div>
          </div>
        )}

        {/* Outer Twinkling Star Accents */}
        <div className="pointer-events-none absolute inset-[-14px]">
          {/* Top-Right Emerald Star */}
          <div className="absolute top-0 right-1 text-emerald-400 animate-twinkle-fast">
            <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24">
              <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5z" />
            </svg>
          </div>

          {/* Top-Left Magenta Star */}
          <div className="absolute top-1 left-0 text-[#d946ef] animate-twinkle-delayed">
            <svg className="w-3 h-3 fill-current" viewBox="0 0 24 24">
              <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5z" />
            </svg>
          </div>

          {/* Bottom-Left Violet Star */}
          <div className="absolute bottom-6 left-1 text-[#8b5cf6] animate-twinkle-slow">
            <svg className="w-2.5 h-2.5 fill-current" viewBox="0 0 24 24">
              <path d="M12 0L14.5 9.5L24 12L14.5 14.5L12 24L9.5 14.5L0 12L9.5 9.5z" />
            </svg>
          </div>
        </div>

        {/* Main Floating Orb Button + Visible Zam AI Pill Label */}
        <div className="flex flex-col items-center gap-1.5 animate-float-dance">
          <button
            type="button"
            onClick={() => setIsOpen(!isOpen)}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onFocus={() => setIsHovered(true)}
            onBlur={() => setIsHovered(false)}
            className="relative group animate-pulse-glow bg-gradient-to-tr from-[#d946ef] via-[#8b5cf6] to-[#10b981] p-[2px] rounded-full shadow-[0_0_25px_rgba(217,70,239,0.45)] hover:shadow-[0_0_35px_rgba(217,70,239,0.7)] transition-all transform hover:scale-105 active:scale-95"
            aria-label="Ask Zam AI Mentor"
          >
            <div className="w-13 h-13 sm:w-14 sm:h-14 bg-[#16161e] rounded-full flex items-center justify-center relative overflow-hidden backdrop-blur-md">
              {/* Subtle rotating background sweep */}
              <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/20 via-transparent to-emerald-500/20 opacity-70 group-hover:opacity-100 transition-opacity" />

              {/* Icon Content */}
              <div className="relative flex items-center justify-center">
                {isOpen ? (
                  <X className="w-6 h-6 text-white group-hover:rotate-90 transition-transform" />
                ) : (
                  <div className="relative">
                    <Bot className="w-6 h-6 text-white group-hover:scale-110 transition-transform" />
                    <Sparkles className="w-3.5 h-3.5 text-emerald-400 absolute -top-1.5 -right-2 animate-bounce" />
                  </div>
                )}
              </div>
            </div>
          </button>

          {/* Visible "Zam AI" Pill Label (Shows before hover) */}
          {!isOpen && (
            <div className="text-[10px] font-semibold tracking-wider uppercase text-zinc-200 bg-[#16161e]/90 border border-white/10 px-2 py-0.5 rounded-full shadow-md flex items-center gap-1 backdrop-blur-sm pointer-events-none">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span>Zam AI</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};