/**
 * API client for interacting with the AskLeap backend
 */

// Base URL for API requests - empty string when frontend is served by the backend
const API_BASE_URL = '';

/**
 * Generate an animation from a text prompt
 */
export async function generateAnimation(prompt: string, level: string, email?: string) {
    console.log("Calling API endpoint:", `${API_BASE_URL}/api/animations/generate`);

    const response = await fetch(`${API_BASE_URL}/api/animations/generate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            prompt,
            level,
            email,
        }),
    });

    console.log("Response status:", response.status);

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("API error:", errorData);
        throw new Error(errorData.detail || 'Failed to generate animation');
    }

    return response.json();
}

/**
 * Get the status of an animation job
 */
export async function getAnimationStatus(jobId: string) {
    console.log("Checking status at:", `${API_BASE_URL}/api/animations/status/${jobId}`);

    const response = await fetch(`${API_BASE_URL}/api/animations/status/${jobId}`);

    console.log("Status response:", response.status);

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error("Status API error:", errorData);
        throw new Error(errorData.detail || 'Failed to get animation status');
    }

    return response.json();
}

/**
 * Submit feedback for an animation
 */
export async function submitFeedback(jobId: string, rating: number, comment?: string) {
    const response = await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            job_id: jobId,
            rating,
            comment,
        }),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to submit feedback');
    }

    return response.json();
}

/**
 * Download a video file
 */
export async function downloadVideo(jobId: string) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/animations/download/${jobId}`);

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Failed to download video');
        }

        const data = await response.json();

        // If we have a direct download URL (Supabase), open it in a new tab
        if (data.download_url) {
            window.open(data.download_url, '_blank');
            return { success: true };
        }

        // If we have a blob response, create a download link
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `askleap-animation-${jobId}.mp4`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        return { success: true };
    } catch (error) {
        console.error('Download error:', error);
        throw error;
    }
}

/**
 * Share a video
 */
export async function shareVideo(jobId: string, videoUrl: string) {
    try {
        // Check if the Web Share API is available
        if (navigator.share) {
            await navigator.share({
                title: 'Check out this explanation from AskLeap AI',
                text: 'I created this explanation with AskLeap AI',
                url: videoUrl,
            });
            return { success: true, shared: true };
        } else {
            // Fallback to copying the URL to clipboard
            await navigator.clipboard.writeText(videoUrl);
            return { success: true, copied: true };
        }
    } catch (error) {
        console.error('Share error:', error);
        // If clipboard write fails, return the URL for manual copying
        return { success: false, url: videoUrl };
    }
} 