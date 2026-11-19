import React, { useState, useEffect } from 'react';
import { Key } from 'lucide-react';
import { Navbar } from './components/Navbar';
import { ApiKeyModal } from './components/ApiKeyModal';
import { FloatingZamMentor } from './components/FloatingZamMentor';
import { LoginPage } from './pages/LoginPage';
import { SkillsPage } from './pages/SkillsPage';
import { StudyPlanPage } from './pages/StudyPlanPage';
import { SamAiPage as ZamAiPage } from './pages/SamAiPage';
import { MentorPage } from './pages/MentorPage';
import { UserSession } from './types';
import { storage } from './services/api';

export function App() {
  const [user, setUser] = useState<UserSession | null>(() => storage.getUser());
  const [currentPage, setCurrentPage] = useState<string>(() => {
    const savedUser = storage.getUser();
    return savedUser ? 'skills' : 'login';
  });
  const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);

  const keys = storage.getApiKeys();
  const hasCustomKey = !!(keys.shared_key || keys.career_api_key || keys.study_plan_api_key || keys.mentor_api_key || keys.sam_ai_api_key);

  // Hidden admin hotkey: Ctrl + Shift + K toggles API key modal
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'K' || e.key === 'k')) {
        e.preventDefault();
        setIsApiKeyModalOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleLoginSuccess = (session: UserSession) => {
    setUser(session);
    setCurrentPage('skills');
  };

  const handleLogout = () => {
    storage.clearUser();
    setUser(null);
    setCurrentPage('login');
  };

  const handleSelectCareer = (careerTitle: string) => {
    if (user) {
      const updated = storage.updateUser({ target_career: careerTitle });
      if (updated) setUser(updated);
    }
    setCurrentPage('study-plan');
  };

  return (
    <div className="min-h-screen bg-[#111116] text-slate-100 bg-mesh-glow flex flex-col font-sans antialiased selection:bg-[#d946ef] selection:text-white">
      {/* Top Single-Row Glass Navbar */}
      <Navbar
        user={user}
        currentPage={currentPage}
        onNavigate={(page) => setCurrentPage(page)}
        onLogout={handleLogout}
      />

      {/* Main Page Content */}
      <main className="flex-1 px-6 py-6 lg:py-8 max-w-7xl mx-auto w-full">
        {(!user || currentPage === 'login') && (
          <LoginPage onLoginSuccess={handleLoginSuccess} />
        )}

        {user && currentPage === 'skills' && (
          <SkillsPage
            user={user}
            onSelectCareer={handleSelectCareer}
          />
        )}

        {user && currentPage === 'study-plan' && (
          <StudyPlanPage
            user={user}
            onNavigateToMentor={() => setCurrentPage('mentor')}
            onNavigateToSkills={() => setCurrentPage('skills')}
            onNavigateToSamAi={() => setCurrentPage('sam-ai')}
          />
        )}

        {user && currentPage === 'sam-ai' && (
          <ZamAiPage
            user={user}
            onNavigateToMentor={() => setCurrentPage('mentor')}
            onNavigateToPlan={() => setCurrentPage('study-plan')}
          />
        )}

        {user && currentPage === 'mentor' && (
          <MentorPage
            user={user}
            onNavigateToSkills={() => setCurrentPage('skills')}
            onNavigateToPlan={() => setCurrentPage('study-plan')}
          />
        )}
      </main>

      {/* Sleek Bottom-Left API Keys Trigger — Invisibly visible (0% opacity by default, reveals on hover or via Ctrl+Shift+K) */}
      <button
        type="button"
        onClick={() => setIsApiKeyModalOpen(true)}
        className="fixed bottom-3 left-3 z-40 text-xs font-semibold text-zinc-300 hover:text-white bg-[#14141c]/95 hover:bg-[#1f1f2a] border border-white/10 hover:border-purple-500/50 px-3 py-1.5 rounded-xl transition-all duration-300 flex items-center gap-2 backdrop-blur-md cursor-pointer shadow-2xl opacity-0 hover:opacity-100 focus:opacity-100 group"
        title="Admin: Configure Gemini API Keys (Shortcut: Ctrl + Shift + K)"
      >
        <Key className="w-3.5 h-3.5 text-[#d946ef] group-hover:scale-110 transition-transform" />
        <span className="whitespace-nowrap font-bold">API Keys</span>
        {hasCustomKey ? (
          <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
        ) : (
          <span className="text-[10px] text-zinc-400 font-mono font-normal">(.env active)</span>
        )}
      </button>

      {/* Floating Bottom-Right Sparkling & Dancing Zam AI Mentor */}
      <FloatingZamMentor
        user={user}
        currentPage={currentPage}
        onNavigateToMentor={() => setCurrentPage('mentor')}
      />

      {/* Gemini API Keys Modal */}
      <ApiKeyModal
        isOpen={isApiKeyModalOpen}
        onClose={() => setIsApiKeyModalOpen(false)}
      />
    </div>
  );
}

export default App;
