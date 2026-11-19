import React, { useState } from 'react';
import { X, Key, CheckCircle, ExternalLink, Sparkles, ChevronDown, ChevronUp } from 'lucide-react';
import { storage } from '../services/api';
import { ApiKeysConfig } from '../types';

interface ApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSaved?: () => void;
}

export const ApiKeyModal: React.FC<ApiKeyModalProps> = ({ isOpen, onClose, onSaved }) => {
  const [keys, setKeys] = useState<ApiKeysConfig>(storage.getApiKeys());
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [saved, setSaved] = useState(false);

  if (!isOpen) return null;

  const handleSave = () => {
    storage.setApiKeys(keys);
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      if (onSaved) onSaved();
      onClose();
    }, 700);
  };

  const handleClear = () => {
    storage.setApiKeys({});
    setKeys({});
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className="w-full max-w-lg bg-[#1b1b24] border border-white/15 rounded-2xl p-6 shadow-2xl relative space-y-5">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-purple-500/15 text-[#d946ef] border border-purple-500/25">
            <Key className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Configure ClariTrack.AI Keys</h3>
            <p className="text-xs text-slate-400">
              Power deep AI reasoning, study schedule curation, and mentor coaching.
            </p>
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-white/[0.03] border border-white/10 text-xs text-slate-300 space-y-1.5">
          <div className="flex items-center gap-1.5 text-cyan-400 font-semibold">
            <Sparkles className="w-4 h-4" />
            <span>Smart Fallback Active</span>
          </div>
          <p className="text-slate-400 text-[11px] leading-relaxed">
            If left blank, the platform automatically defaults to the backend <code className="text-cyan-300">GEMINI_API_KEY</code> from <code className="text-slate-200">.env</code>, or our built-in high-fidelity intelligent simulation so the app runs smoothly with zero errors.
          </p>
        </div>

        {/* Primary / Shared Key */}
        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-slate-300 flex items-center justify-between">
            <span>Primary / Shared Gemini API Key</span>
            <a
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              rel="noreferrer"
              className="text-cyan-400 hover:text-cyan-300 text-[11px] flex items-center gap-1"
            >
              Get Free Key <ExternalLink className="w-3 h-3" />
            </a>
          </label>
          <input
            type="password"
            value={keys.shared_key || ''}
            onChange={(e) => setKeys({ ...keys, shared_key: e.target.value })}
            placeholder="AIzaSy..."
            className="w-full glass-input px-3.5 py-2.5 text-xs font-mono"
          />
        </div>

        {/* Advanced Per-Agent Keys Toggle */}
        <div className="space-y-3 pt-1">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-xs font-semibold text-violet-400 hover:text-violet-300 flex items-center gap-1.5"
          >
            {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            <span>{showAdvanced ? 'Hide Per-Agent Specific Keys' : 'Configure Separate Keys Per Agent (Optional)'}</span>
          </button>

          {showAdvanced && (
            <div className="space-y-3 p-3.5 rounded-xl bg-black/40 border border-white/5 animate-in fade-in">
              <div>
                <label className="text-[11px] font-medium text-slate-300 block mb-1">
                  Career Match Agent Key (Gemini 2.5 Flash)
                </label>
                <input
                  type="password"
                  value={keys.career_api_key || ''}
                  onChange={(e) => setKeys({ ...keys, career_api_key: e.target.value })}
                  placeholder="Leave empty to use Primary Key"
                  className="w-full glass-input px-3 py-1.5 text-xs font-mono"
                />
              </div>

              <div>
                <label className="text-[11px] font-medium text-slate-300 block mb-1">
                  Study Plan Agent Key (Gemini 2.5 Pro + Grounding)
                </label>
                <input
                  type="password"
                  value={keys.study_plan_api_key || ''}
                  onChange={(e) => setKeys({ ...keys, study_plan_api_key: e.target.value })}
                  placeholder="Leave empty to use Primary Key"
                  className="w-full glass-input px-3 py-1.5 text-xs font-mono"
                />
              </div>

              <div>
                <label className="text-[11px] font-medium text-slate-300 block mb-1">
                  AI Mentor Chat Key (Gemini 2.5 Pro + Grounding)
                </label>
                <input
                  type="password"
                  value={keys.mentor_api_key || ''}
                  onChange={(e) => setKeys({ ...keys, mentor_api_key: e.target.value })}
                  placeholder="Leave empty to use Primary Key"
                  className="w-full glass-input px-3 py-1.5 text-xs font-mono"
                />
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-2 border-t border-white/10">
          <button
            onClick={handleClear}
            className="text-xs text-slate-400 hover:text-rose-400 transition-colors"
          >
            Clear Stored Keys
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] text-xs font-medium text-slate-300"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-5 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-lg shadow-cyan-500/20 transition-all"
            >
              {saved ? (
                <>
                  <CheckCircle className="w-4 h-4 text-emerald-300" />
                  <span>Saved!</span>
                </>
              ) : (
                <span>Save Keys</span>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
