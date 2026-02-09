import React from 'react';
import { Sparkles } from 'lucide-react';
import LeapLogo from '@/components/LeapLogo';

const RetroHeader = () => {
  return (
    <header className="py-8 mb-10 animate-boot-up">
      <div className="container max-w-4xl mx-auto">
        <div className="flex flex-col items-center justify-center space-y-6">
          <div className="flex items-center space-x-4">
            <Sparkles size={40} className="text-retro-green" />
            <LeapLogo className="h-20 w-auto" />
          </div>

          <div className="retro-chip bg-retro-green text-lg px-4 py-2">
            v1.0.0 ALPHA
          </div>

          <p className="text-center font-mono text-xl md:text-2xl max-w-2xl font-medium">
            Generate explainer videos to learn anything
          </p>
        </div>
      </div>
    </header>
  );
};

export default RetroHeader;
