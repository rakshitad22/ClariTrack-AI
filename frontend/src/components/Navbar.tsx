import React from 'react';
import { LogOut, Compass, Calendar, Mic } from 'lucide-react';
import { UserSession } from '../types';

interface NavbarProps {
  user: UserSession | null;
  currentPage: string;
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  user,
  currentPage,
  onNavigate,
  onLogout
}) => {
  return (
    <header className="sticky top-0 z-40 w-full h-16 backdrop-blur-xl bg-[#14141b]/95 border-b border-white/[0.08] transition-all">
      {/* Symmetrical 3-Column Precision Grid */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center max-w-7xl mx-auto px-6 h-16 w-full whitespace-nowrap">
        {/* ================= COLUMN 1 (LEFT): BRAND LOCKUP ================= */}
        <div className="flex items-center gap-3 justify-self-start">
          <div
            onClick={() => onNavigate(user ? 'skills' : 'login')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            {/* Geometric Track Emblem */}
            <div className="w-9 h-9 rounded-xl overflow-hidden border border-white/15 shadow-lg shadow-purple-500/20 bg-[#14141b] flex items-center justify-center flex-shrink-0 relative">
              <img
                src="/claritrack-logo.jpg"
                alt="ClariTrack AI Logo"
                className="w-full h-full object-cover object-[50%_28%] scale-[1.45] rounded-lg transition-transform group-hover:scale-[1.55]"
              />
            </div>

            <div className="flex flex-col justify-center">
              <div className="flex items-baseline">
                <span className="font-bold tracking-tight text-white text-lg group-hover:text-purple-100 transition-colors">
                  ClariTrack
                </span>
                <span className="font-extrabold text-lg bg-gradient-to-r from-[#d946ef] via-[#a855f7] to-[#10b981] bg-clip-text text-transparent">
                  .AI
                </span>
              </div>
              <div className="text-[11px] text-zinc-400 truncate max-w-[260px] whitespace-nowrap tracking-tight">
                Know Where You Stand. Rehearse the Moment.
              </div>
            </div>
          </div>
        </div>

        {/* ================= COLUMN 2 (CENTER): 3 NAVIGATION TABS DEAD-CENTER ================= */}
        {user ? (
          <nav className="hidden md:flex items-center gap-8 justify-self-center whitespace-nowrap">
            <button
              onClick={() => onNavigate('skills')}
              className={`py-2 text-sm font-medium flex items-center gap-2 transition-all whitespace-nowrap relative group ${
                currentPage === 'skills'
                  ? 'text-white font-semibold after:absolute after:bottom-[-2px] after:left-0 after:right-0 after:h-[2px] after:rounded-full after:bg-gradient-to-r after:from-[#d946ef] after:to-[#8b5cf6] after:shadow-[0_0_8px_rgba(217,70,239,0.7)]'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              <Compass className={`w-4 h-4 transition-colors ${currentPage === 'skills' ? 'text-[#d946ef]' : 'text-zinc-400 group-hover:text-zinc-200'}`} />
              <span>Skills & Careers</span>
            </button>

            <button
              onClick={() => onNavigate('study-plan')}
              className={`py-2 text-sm font-medium flex items-center gap-2 transition-all whitespace-nowrap relative group ${
                currentPage === 'study-plan'
                  ? 'text-white font-semibold after:absolute after:bottom-[-2px] after:left-0 after:right-0 after:h-[2px] after:rounded-full after:bg-gradient-to-r after:from-[#d946ef] after:to-[#8b5cf6] after:shadow-[0_0_8px_rgba(217,70,239,0.7)]'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              <Calendar className={`w-4 h-4 transition-colors ${currentPage === 'study-plan' ? 'text-purple-400' : 'text-zinc-400 group-hover:text-zinc-200'}`} />
              <span>Study Plan</span>
            </button>

            <button
              onClick={() => onNavigate('sam-ai')}
              className={`py-2 text-sm font-medium flex items-center gap-2 transition-all whitespace-nowrap relative group ${
                currentPage === 'sam-ai'
                  ? 'text-white font-semibold after:absolute after:bottom-[-2px] after:left-0 after:right-0 after:h-[2px] after:rounded-full after:bg-gradient-to-r after:from-[#d946ef] after:to-[#8b5cf6] after:shadow-[0_0_8px_rgba(217,70,239,0.7)]'
                  : 'text-zinc-400 hover:text-white'
              }`}
            >
              <Mic className={`w-4 h-4 transition-colors ${currentPage === 'sam-ai' ? 'text-emerald-400' : 'text-zinc-400 group-hover:text-zinc-200'}`} />
              <span>Zam AI Interview</span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse ml-0.5" />
            </button>
          </nav>
        ) : (
          <div />
        )}

        {/* ================= COLUMN 3 (RIGHT): CLEAN LOGOUT ALIGNED RIGHT ================= */}
        <div className="flex items-center justify-self-end">
          {user && (
            <div className="relative group/logout">
              <button
                onClick={onLogout}
                className="p-2 rounded-xl text-zinc-400 hover:text-rose-400 bg-[#1b1b24] hover:bg-rose-500/10 border border-white/[0.08] transition-colors flex-shrink-0"
                aria-label="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
              <div className="absolute right-0 top-full mt-2 opacity-0 pointer-events-none group-hover/logout:opacity-100 transition-opacity duration-150 px-2 py-1 bg-[#181824] border border-white/10 rounded-md text-[10px] text-zinc-300 font-medium whitespace-nowrap shadow-xl">
                Sign Out
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
