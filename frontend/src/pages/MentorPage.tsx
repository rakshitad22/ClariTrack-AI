import React, { useState, useRef, useEffect } from 'react';
import {
  Bot,
  Send,
  User,
  Sparkles,
  Copy,
  Check,
  RotateCcw
} from 'lucide-react';
import { UserSession, ChatMessage } from '../types';
import { api } from '../services/api';

interface MentorPageProps {
  user: UserSession;
  onNavigateToSkills: () => void;
  onNavigateToPlan: () => void;
}

const STARTER_PROMPTS = [
  "What are the most in-demand tech careers in 2026 & 2027?",
  "Which skills are companies expecting from freshers right now?",
  "How should I prepare my projects and resume for my target role?",
  "Give me a 1-week revision checklist for my missing skills."
];

export const MentorPage: React.FC<MentorPageProps> = ({
  user,
  onNavigateToSkills,
  onNavigateToPlan
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: `👋 **Hello ${user.name}!** I'm **Zam AI**, your dedicated **ClariTrack.AI** Career & Tech Mentor. I've automatically synchronized your profile:\n\n- **Target Career:** \`${user.target_career || 'Software Engineer'}\`\n- **Logged Skills:** ${user.skills?.map(s => `\`${s.name}\``).join(', ') || 'General CS fundamentals'}\n\nAsk me anything about 2026-2027 hiring trends, fresher interview screening, coding doubts, or resume project reviews!`
    }
  ]);

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (textToSend?: string) => {
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
          content: "I ran into a temporary connection hiccup. Let's try that question again, or you can test one of the starter prompt chips!"
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = (text: string, idx: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleClearHistory = () => {
    if (window.confirm('Reset conversation history?')) {
      setMessages([
        {
          role: 'assistant',
          content: `History reset! Ready when you are, **${user.name}**.`
        }
      ]);
    }
  };

  return (
    <div className="h-[calc(100vh-100px)] flex flex-col matte-card shadow-2xl overflow-hidden animate-in fade-in duration-300">
      {/* ================= CHAT HEADER ================= */}
      <div className="p-4 lg:px-6 border-b border-white/[0.08] flex items-center justify-between bg-[#14141b] flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#d946ef] to-[#8b5cf6] p-[1px] shadow-lg shadow-purple-500/20">
            <div className="w-full h-full bg-[#111116] rounded-[11px] flex items-center justify-center">
              <Bot className="w-5 h-5 text-[#d946ef]" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-extrabold text-white">ClariTrack.AI • Zam AI Career & Tech Mentor</h2>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-[10px] uppercase font-mono px-2 py-0.2 rounded-full bg-purple-500/15 text-[#d946ef] border border-purple-500/30">
                Zam AI Mentor • Gemini 2.5 Pro
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Personalized for <strong className="text-white">{user.name}</strong> • Target: <span className="text-[#d946ef] font-semibold">{user.target_career || 'Software Engineer'}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleClearHistory}
            className="p-2 rounded-xl text-slate-400 hover:text-white bg-[#14141b] hover:bg-white/[0.08] border border-white/10 transition-colors"
            title="Reset conversation history"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* ================= MESSAGE STREAM ================= */}
      <div className="flex-1 overflow-y-auto p-4 lg:p-6 space-y-5">
        {messages.map((msg, idx) => {
          const isUser = msg.role === 'user';

          return (
            <div
              key={idx}
              className={`flex gap-3 max-w-4xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
            >
              {/* Avatar */}
              <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 text-xs font-bold ${
                isUser
                  ? 'bg-gradient-to-tr from-cyan-500 to-emerald-400 text-black shadow-md'
                  : 'bg-gradient-to-tr from-[#d946ef] to-[#8b5cf6] text-white shadow-md'
              }`}>
                {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              {/* Message Bubble */}
              <div className={`group relative p-4 rounded-2xl text-xs leading-relaxed transition-all ${
                isUser
                  ? 'bg-purple-500/20 border border-purple-500/40 text-white shadow-lg'
                  : 'bg-[#14141b] border border-white/[0.08] text-slate-200'
              }`}>
                {/* Copy button */}
                <button
                  onClick={() => handleCopy(msg.content, idx)}
                  className="absolute top-2 right-2 p-1 rounded-md opacity-0 group-hover:opacity-100 hover:bg-white/10 text-slate-400 hover:text-white transition-opacity"
                  title="Copy text"
                >
                  {copiedIndex === idx ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                </button>

                {/* Formatted Text */}
                <div className="whitespace-pre-wrap font-sans space-y-2">
                  {msg.content}
                </div>
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex gap-3 max-w-2xl mr-auto animate-in fade-in">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-[#d946ef] to-[#8b5cf6] flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white animate-spin" />
            </div>
            <div className="p-4 rounded-2xl bg-[#14141b] border border-white/[0.08] text-xs text-slate-400 flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-[#d946ef] animate-pulse" />
              <span>Agent 3 is grounding insights against 2026-2027 market benchmarks...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ================= STARTER CHIPS & INPUT FORM ================= */}
      <div className="p-4 lg:p-6 border-t border-white/[0.08] bg-[#14141b] space-y-3 flex-shrink-0">
        {/* Starter Chips */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-none">
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 flex-shrink-0">
            Suggested:
          </span>
          {STARTER_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSendMessage(prompt)}
              className="px-3 py-1.5 rounded-full bg-[#1b1b24] hover:bg-[#22222e] border border-white/5 hover:border-purple-500/30 text-[11px] text-slate-300 hover:text-[#d946ef] font-medium whitespace-nowrap transition-all"
            >
              <span>{prompt}</span>
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask anything about ${user.target_career || 'tech careers'}, coding concepts, salary, or resume tips...`}
            className="flex-1 matte-input px-4 py-3 text-xs font-medium text-white placeholder-slate-500 focus:border-[#d946ef]"
          />

          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-5 py-3 rounded-xl btn-primary text-xs flex items-center gap-1.5 shadow-lg disabled:opacity-50 transition-all flex-shrink-0"
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Send</span>
          </button>
        </form>
      </div>
    </div>
  );
};
