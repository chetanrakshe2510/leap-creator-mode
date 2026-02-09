import React, { useState, useEffect } from 'react';

interface PromptInputProps {
  onSubmit: (prompt: string, difficultyLevel: string, email: string) => void;
  isLoading: boolean;
}

const PromptInput = ({ onSubmit, isLoading }: PromptInputProps) => {
  const [prompt, setPrompt] = useState('');
  const [difficultyLevel, setDifficultyLevel] = useState('eli5');
  const [email, setEmail] = useState('');
  const [displayPlaceholder, setDisplayPlaceholder] = useState('');
  const [emailError, setEmailError] = useState('');
  const [promptError, setPromptError] = useState('');

  const examplePrompts = [
    "Explain why does water expand when frozen?",
    "How do you calculate GCF of 2 numbers?",
    "What causes lightning during a thunderstorm?"
  ];

  useEffect(() => {
    let currentIndex = 0;

    // Set the initial placeholder
    setDisplayPlaceholder(examplePrompts[currentIndex]);

    // Setup the interval to change the placeholder
    const interval = setInterval(() => {
      currentIndex = (currentIndex + 1) % examplePrompts.length;
      setDisplayPlaceholder(examplePrompts[currentIndex]);
    }, 3000); // Change every 3 seconds

    // Cleanup function
    return () => {
      clearInterval(interval);
    };
  }, []);

  const validateEmail = (email: string): boolean => {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newEmail = e.target.value;
    setEmail(newEmail);

    if (newEmail && !validateEmail(newEmail)) {
      setEmailError('Please enter a valid email address');
    } else {
      setEmailError('');
    }
  };

  // Validate prompt length
  const validatePromptLength = (text: string): boolean => {
    const trimmedLength = text.trim().length;
    if (trimmedLength < 10) {
      setPromptError('Your question is too short (minimum 10 characters)');
      return false;
    } else if (trimmedLength > 140) {
      setPromptError('Your question is too long (maximum 140 characters)');
      return false;
    } else {
      setPromptError('');
      return true;
    }
  };

  // Handle prompt change with validation
  const handlePromptChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newPrompt = e.target.value;
    setPrompt(newPrompt);
    validatePromptLength(newPrompt);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    if (!prompt.trim()) {
      setPromptError('Please enter a question or topic');
      return;
    }

    // Validate prompt length - need to check result explicitly as boolean
    if (validatePromptLength(prompt) === false) {
      return;
    }

    if (!email.trim()) {
      setEmailError('Email is required');
      return;
    }

    if (!validateEmail(email)) {
      setEmailError('Please enter a valid email address');
      return;
    }

    if (!isLoading) {
      console.log("Submitting form:", { prompt, difficultyLevel, email });
      onSubmit(prompt, difficultyLevel, email);
    }
  };

  return (
    <div className="retro-window w-full max-w-4xl mx-auto mb-8 animate-boot-up" style={{ animationDelay: '0.2s' }}>
      <div className="retro-window-title bg-retro-green">
        <div className="flex items-center space-x-2">
          <span>VIDEO MAGIC LAB</span>
        </div>
        <div className="retro-window-title-buttons">
          <div className="retro-window-button bg-retro-yellow"></div>
          <div className="retro-window-button bg-retro-green"></div>
          <div className="retro-window-button bg-red-500"></div>
        </div>
      </div>

      <div className="retro-window-content">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="prompt" className="block font-mono text-base md:text-lg">
              ENTER YOUR TOPIC:
            </label>
            <div className="relative">
              <textarea
                id="prompt"
                value={prompt}
                onChange={handlePromptChange}
                className={`retro-input h-32 font-mono text-base md:text-lg resize-none ${promptError ? 'border-red-500' : ''}`}
                placeholder={displayPlaceholder}
                disabled={isLoading}
              />
            </div>
            <div className={`text-right font-mono text-sm ${prompt.trim().length === 0 ? 'text-retro-gray' :
              prompt.trim().length < 10 ? 'text-red-500' :
                prompt.trim().length > 140 ? 'text-red-500' :
                  'text-green-600'
              }`}>
              {prompt.length} CHARACTERS {promptError ? `— ${promptError}` : ''}
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="difficulty" className="block font-mono text-base md:text-lg">
              EXPLANATION LEVEL:
            </label>
            <div className="relative">
              <select
                id="difficulty"
                value={difficultyLevel}
                onChange={(e) => setDifficultyLevel(e.target.value)}
                className="retro-input w-full font-mono p-3 text-base md:text-lg"
                disabled={isLoading}
              >
                <option value="eli5">ELI5: Explain like I'm 5</option>
                <option value="normal">Normal: Simple language, minimal technical terms</option>
                <option value="advanced" disabled className="text-retro-gray">
                  Advanced: Coming in future release
                </option>
              </select>
            </div>
          </div>

          <div className="space-y-2">
            <label htmlFor="email" className="block font-mono text-base md:text-lg">
              YOUR EMAIL (FOR NOTIFICATION):
            </label>
            <div className="relative">
              <input
                type="email"
                id="email"
                value={email}
                onChange={handleEmailChange}
                className={`retro-input w-full font-mono p-3 text-base md:text-lg ${emailError ? 'border-red-500' : ''}`}
                placeholder="your.email@example.com"
                disabled={isLoading}
              />
            </div>
            {emailError ? (
              <div className="text-sm md:text-base font-mono text-red-500">
                {emailError}
              </div>
            ) : (
              <div className="text-base md:text-lg font-mono text-retro-gray">
                Videos take 2-3 minutes to generate. We'll notify you when ready!
              </div>
            )}
          </div>

          <div className="flex justify-end mt-6">
            <button
              type="submit"
              disabled={isLoading || !prompt.trim() || !!promptError || !email.trim() || !!emailError}
              className={`retro-button-primary bg-retro-green text-lg md:text-xl px-6 py-3 ${isLoading || !prompt.trim() || !!promptError || !email.trim() || !!emailError ?
                'opacity-50 cursor-not-allowed' :
                'hover:bg-opacity-90 transition-colors'
                }`}
            >
              {isLoading ? 'PROCESSING...' : 'GENERATE VIDEO EXPLANATION'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PromptInput;
