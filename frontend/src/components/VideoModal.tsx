import React from 'react';
import { X, Play, ExternalLink } from 'lucide-react';

interface VideoModalProps {
  video: { title: string; url: string } | null;
  onClose: () => void;
}

export const VideoModal: React.FC<VideoModalProps> = ({ video, onClose }) => {
  if (!video) return null;

  // Extract video ID from youtube URL
  let videoId = 'kqtD5dpn9C8';
  try {
    if (video.url.includes('v=')) {
      videoId = video.url.split('v=')[1].split('&')[0];
    } else if (video.url.includes('youtu.be/')) {
      videoId = video.url.split('youtu.be/')[1].split('?')[0];
    }
  } catch {
    videoId = 'kqtD5dpn9C8';
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-in fade-in duration-200">
      <div className="w-full max-w-3xl bg-obsidian-950 border border-white/20 rounded-2xl overflow-hidden shadow-2xl space-y-3 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-violet-500/20 text-violet-400">
              <Play className="w-4 h-4 fill-current" />
            </div>
            <h4 className="text-xs font-bold text-white truncate max-w-md">
              {video.title}
            </h4>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="aspect-video w-full rounded-xl overflow-hidden bg-black border border-white/10">
          <iframe
            src={`https://www.youtube.com/embed/${videoId}?autoplay=1`}
            title={video.title}
            className="w-full h-full"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>

        <div className="flex justify-between items-center text-xs text-slate-400 pt-1">
          <span>Verified Curriculum Lecture • Curated by AI Study Plan Agent</span>
          <a
            href={video.url}
            target="_blank"
            rel="noreferrer"
            className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-semibold"
          >
            Open in YouTube <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </div>
  );
};
