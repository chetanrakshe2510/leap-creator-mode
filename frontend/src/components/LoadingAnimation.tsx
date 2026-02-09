
import React from 'react';
import { Sparkles } from 'lucide-react';

interface LoadingAnimationProps {
  message?: string;
}

const LoadingAnimation = ({ message = "Creating your video explanation..." }: LoadingAnimationProps) => {
  return (
    <div className="retro-window w-full max-w-4xl mx-auto mb-8">
      <div className="retro-window-title bg-retro-green">
        <div className="flex items-center space-x-2">
          <span>VIDEO GENERATOR</span>
        </div>
        <div className="retro-window-title-buttons">
          <div className="retro-window-button bg-retro-yellow"></div>
          <div className="retro-window-button bg-retro-green"></div>
          <div className="retro-window-button bg-red-500"></div>
        </div>
      </div>
      
      <div className="retro-window-content p-8">
        <div className="flex flex-col items-center justify-center space-y-6">
          <Sparkles size={48} className="text-retro-green animate-pulse" />
          
          <div className="font-mono text-center">
            <div className="mb-2">{message}</div>
            <div className="flex items-center">
              <span>Loading</span>
              <span className="cursor-blink ml-1"></span>
            </div>
            <div className="mt-4 text-xs text-retro-gray">
              This typically takes 2-3 minutes. We'll email you when it's ready!
            </div>
          </div>
          
          <div className="w-full max-w-md">
            <div className="loading-bar">
              <div className="loading-bar-progress bg-retro-green"></div>
            </div>
            <div className="mt-2 text-xs font-mono text-retro-gray text-center">
              Please wait while we create your educational content...
            </div>
          </div>
          
          <div className="grid grid-cols-2 gap-4 mt-4 text-sm font-mono">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-retro-green animate-pulse"></div>
              <span>Analyzing topic</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-retro-yellow animate-pulse"></div>
              <span>Creating animations</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-retro-green animate-pulse"></div>
              <span>Adding explanations</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-retro-green animate-pulse"></div>
              <span>Preparing video</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingAnimation;
