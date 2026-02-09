import React, { useRef, useEffect, useState } from 'react';
import { Star } from 'lucide-react';
import { useToast } from "@/hooks/use-toast";
import { submitFeedback } from '@/api/client';

interface VideoOutputProps {
  videoUrl: string;
  prompt: string;
  difficulty?: string;
  jobId: string;
}

const VideoOutput = ({ videoUrl, prompt, difficulty = "eli5", jobId }: VideoOutputProps) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const { toast } = useToast();
  const [showFeedback, setShowFeedback] = useState(false);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [submittingFeedback, setSubmittingFeedback] = useState(false);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.load();
    }
  }, [videoUrl]);

  const handleFeedbackSubmit = async () => {
    if (rating === 0) {
      toast({
        title: "Rating Required",
        description: "Please select a rating before submitting feedback.",
        variant: "destructive"
      });
      return;
    }

    setSubmittingFeedback(true);

    try {
      await submitFeedback(jobId, rating, comment);
      toast({
        title: "Feedback Submitted",
        description: "Thank you for your feedback!",
      });
      setShowFeedback(false);
      setRating(0);
      setComment('');
    } catch (error) {
      console.error('Error submitting feedback:', error);
      toast({
        title: "Submission Failed",
        description: "There was an error submitting your feedback. Please try again.",
        variant: "destructive"
      });
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const getDifficultyLabel = (level: string) => {
    const labels = {
      'eli5': 'ELI5: Explain like I\'m 5',
      'normal': 'Normal: Simple language, minimal terms',
      'advanced': 'Advanced: Technical terminology'
    };
    return labels[level as keyof typeof labels] || 'ELI5: Explain like I\'m 5';
  };

  return (
    <div className="retro-window w-full max-w-4xl mx-auto mb-8 animate-boot-up" style={{ animationDelay: '0.4s' }}>
      <div className="retro-window-title bg-retro-green">
        <div className="flex items-center space-x-2">
          <span>VIDEO PREVIEW</span>
        </div>
        <div className="retro-window-title-buttons">
          <div className="retro-window-button bg-retro-yellow"></div>
          <div className="retro-window-button bg-retro-green"></div>
          <div className="retro-window-button bg-red-500"></div>
        </div>
      </div>

      <div className="retro-window-content p-0">
        <div className="crt-screen w-full aspect-video bg-retro-black overflow-hidden">
          <div className="scanlines"></div>
          {videoUrl ? (
            <video
              ref={videoRef}
              className="w-full h-full object-contain vhs-effect"
              controls
              autoPlay
              loop
              muted
            >
              <source src={videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-white font-mono text-center p-4">
                <p className="text-lg md:text-xl">NO VIDEO CREATED YET</p>
                <p className="text-sm md:text-base mt-2">Generate a video to see the result here</p>
              </div>
            </div>
          )}
        </div>

        {videoUrl && (
          <div className="p-6 font-mono">
            <div className="mb-6">
              <div className="text-base md:text-lg text-retro-gray uppercase mb-2">TOPIC:</div>
              <div className="bg-white border border-retro-darkgray p-3 text-lg md:text-xl mb-4">
                {prompt}
              </div>

              <div className="text-base md:text-lg text-retro-gray uppercase mb-2">EXPLANATION LEVEL:</div>
              <div className="bg-white border border-retro-darkgray p-3 text-lg md:text-xl">
                {getDifficultyLabel(difficulty)}
              </div>
            </div>

            <div className="flex flex-wrap gap-3 mt-6">
              <button
                onClick={() => setShowFeedback(!showFeedback)}
                className="retro-button flex items-center space-x-2 bg-retro-blue text-white border-none text-lg md:text-xl px-5 py-3"
              >
                <Star size={24} />
                <span>RATE VIDEO</span>
              </button>
            </div>

            {showFeedback && (
              <div className="mt-6 p-4 bg-white border border-retro-darkgray">
                <div className="text-base md:text-lg text-retro-gray uppercase mb-3">RATE THIS EXPLANATION:</div>
                <div className="flex mb-4">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      onClick={() => setRating(star)}
                      className={`p-2 ${rating >= star ? 'text-yellow-500' : 'text-gray-300'}`}
                    >
                      <Star size={36} fill={rating >= star ? 'currentColor' : 'none'} />
                    </button>
                  ))}
                </div>

                <div className="text-base md:text-lg text-retro-gray uppercase mb-2">COMMENTS (OPTIONAL):</div>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="w-full p-3 border border-retro-darkgray mb-4 font-mono text-lg md:text-xl"
                  rows={3}
                  placeholder="Tell us what you think..."
                />

                <button
                  onClick={handleFeedbackSubmit}
                  disabled={submittingFeedback}
                  className="retro-button bg-retro-blue text-white border-none text-lg md:text-xl px-5 py-3"
                >
                  {submittingFeedback ? 'SUBMITTING...' : 'SUBMIT FEEDBACK'}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoOutput;
