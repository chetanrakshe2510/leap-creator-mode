import React, { useState, useEffect } from 'react';
import RetroHeader from '@/components/RetroHeader';
import PromptInput from '@/components/PromptInput';
import LoadingAnimation from '@/components/LoadingAnimation';
import VideoOutput from '@/components/VideoOutput';
import { useToast } from "@/hooks/use-toast";
import { generateAnimation, getAnimationStatus } from '@/api/client';

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');
  const [prompt, setPrompt] = useState('');
  const [difficultyLevel, setDifficultyLevel] = useState('');
  const [email, setEmail] = useState('');
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobFailed, setJobFailed] = useState(false);
  const { toast } = useToast();

  // Poll for job status when we have a jobId
  useEffect(() => {
    if (!jobId || videoUrl || jobFailed) return;

    const checkStatus = async () => {
      try {
        console.log("Checking status for job:", jobId);
        const status = await getAnimationStatus(jobId);
        console.log("Received status:", status);

        if (status.status === 'completed' && status.video_url) {
          setVideoUrl(status.video_url);
          setIsLoading(false);

          toast({
            title: "Explanation Video Generated",
            description: email ? `We've also sent a notification to ${email}.` : undefined,
          });
        } else if (status.status === 'failed') {
          setIsLoading(false);
          setJobFailed(true); // Mark job as failed to stop polling

          // Use the error message from the API if available
          const errorMessage = status.error || "There was an error generating your video.";

          // Create a user-friendly message based on the error
          let userFriendlyMessage = "There was an error generating your video. Please try again.";

          // Check for specific validation error patterns
          if (errorMessage.includes("too short")) {
            userFriendlyMessage = "Your input is too short. Please provide a more detailed question or topic for animation (at least 10 characters).";
          } else if (errorMessage.includes("too long")) {
            userFriendlyMessage = "Your input is too long. Please provide a more concise question or topic (less than 140 characters).";
          } else if (errorMessage.includes("doesn't appear to be a question") || errorMessage.includes("needs clarification")) {
            userFriendlyMessage = "Please rephrase your input as a clear question or topic for animation. For example: 'How do you calculate the LCM of 3 numbers?'";
          } else if (errorMessage.includes("Did you mean:")) {
            // Extract the suggested reformulation
            userFriendlyMessage = errorMessage; // Use the full message with the suggestion
          } else if (/^(hi|hello|hey|yo|what'?s up|sup|howdy|how are you|greetings)/i.test(prompt.trim())) {
            // Detect casual greetings
            userFriendlyMessage = "This appears to be a greeting rather than an educational topic. Please ask an educational question or topic that you'd like explained, such as 'What causes lightning?' or 'Explain quantum entanglement.'";
          } else if (!prompt.includes("?") && !errorMessage.includes("too short") && !errorMessage.includes("too long")) {
            // Input is not a question and not caught by other rules
            userFriendlyMessage = "Your input doesn't appear to be an educational question or topic. Please provide a clear educational question or topic that you'd like animated, like 'How do photosynthesis work?' or 'Explain the water cycle.'";
          }

          toast({
            title: "Input Needs Improvement",
            description: userFriendlyMessage,
            variant: "destructive",
          });
        }
      } catch (error) {
        console.error('Error checking status:', error);
      }
    };

    // Check immediately and then every 5 seconds
    checkStatus();
    const interval = setInterval(checkStatus, 5000);

    return () => clearInterval(interval);
  }, [jobId, videoUrl, email, toast, jobFailed]);

  const validateEmail = (email: string): boolean => {
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
  };

  const generateVideo = async (promptText: string, difficulty: string, userEmail: string) => {
    // Basic input validation
    if (!promptText || promptText.trim().length < 10) {
      toast({
        title: "Input Too Short",
        description: "Your question or topic should be at least 10 characters long to generate a meaningful animation.",
        variant: "destructive",
      });
      return;
    }

    if (promptText.trim().length > 140) {
      toast({
        title: "Input Too Long",
        description: "Your question or topic should be less than 140 characters. Please make it more concise.",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setPrompt(promptText);
    setDifficultyLevel(difficulty);
    setEmail(userEmail);
    setVideoUrl(''); // Clear any previous video
    setJobFailed(false); // Reset job failed state for new generation

    // Validate email
    if (userEmail && !validateEmail(userEmail)) {
      setIsLoading(false);
      toast({
        title: "Invalid Email",
        description: "Please enter a valid email address.",
        variant: "destructive",
      });
      return;
    }

    try {
      console.log("Sending request:", { promptText, difficulty, userEmail });
      // Call the real API
      const response = await generateAnimation(promptText, difficulty, userEmail);
      console.log("Received response:", response);
      setJobId(response.job_id);

      toast({
        title: "Animation Generation Started",
        description: "We'll notify you when it's ready.",
      });
    } catch (error) {
      setIsLoading(false);
      console.error('Error generating video:', error);
      toast({
        title: "Request Failed",
        description: error instanceof Error ? error.message : "There was an error starting the generation. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="min-h-screen bg-retro-beige text-base md:text-lg">
      <div className="container px-4 py-8 mx-auto">
        <RetroHeader />

        <PromptInput onSubmit={generateVideo} isLoading={isLoading} />

        {isLoading ? (
          <LoadingAnimation />
        ) : (
          videoUrl && <VideoOutput videoUrl={videoUrl} prompt={prompt} difficulty={difficultyLevel} jobId={jobId || ''} />
        )}

        <footer className="text-center font-mono text-base md:text-lg text-retro-gray mt-12 pb-6 animate-boot-up" style={{ animationDelay: '0.6s' }}>
          <p>© {new Date().getFullYear()} LEAP • ALL RIGHTS RESERVED</p>
          <p className="mt-2">MAKING EDUCATION ACCESSIBLE ONE MICRO LESSON AT A TIME</p>
          <p className="mt-2">
            Made with <span className="text-red-600">❤️</span> by{" "}
            <a
              href="https://www.linkedin.com/in/sid-ab/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Sid
            </a>
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
