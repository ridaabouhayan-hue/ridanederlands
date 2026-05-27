/**
 * Interactive Transcript Audio Synchronizer for "NOS in Makkelijke Taal"
 * Supports both HTML5 <audio> elements and YouTube Iframe API.
 */
document.addEventListener("DOMContentLoaded", () => {
    let mediaType = null; // 'audio' or 'youtube'
    let audioEl = null;
    let ytPlayer = null;
    let wordSpans = [];
    
    // Auto-scroll configuration
    const autoScrollEnabled = true;
    let lastScrollTime = 0;
    
    // Initialize word spans
    function initWordSpans() {
        wordSpans = Array.from(document.querySelectorAll("span.w"));
        
        // Add click listener to seek to the start time of the word
        wordSpans.forEach(span => {
            span.addEventListener("click", () => {
                const start = parseFloat(span.getAttribute("data-start"));
                if (!isNaN(start)) {
                    seekToTime(start);
                }
            });
        });
    }

    function seekToTime(seconds) {
        if (mediaType === "audio" && audioEl) {
            audioEl.currentTime = seconds;
            audioEl.play().catch(() => {});
        } else if (mediaType === "youtube" && ytPlayer && typeof ytPlayer.seekTo === "function") {
            ytPlayer.seekTo(seconds, true);
            ytPlayer.playVideo();
        }
    }

    // High frequency time updates
    function updateHighlights(currentTime) {
        let activeSpan = null;
        
        wordSpans.forEach(span => {
            const start = parseFloat(span.getAttribute("data-start"));
            const end = parseFloat(span.getAttribute("data-end"));
            
            if (!isNaN(start) && !isNaN(end) && currentTime >= start && currentTime <= end) {
                span.classList.add("highlight");
                activeSpan = span;
            } else {
                span.classList.remove("highlight");
            }
        });
        
        // Auto scroll active word into center of screen if enabled
        if (autoScrollEnabled && activeSpan) {
            const now = Date.now();
            if (now - lastScrollTime > 1500) { // Throttle scroll to prevent stutter
                activeSpan.scrollIntoView({
                    behavior: "smooth",
                    block: "center"
                });
                lastScrollTime = now;
            }
        }
    }

    // --- HTML5 Audio Setup ---
    function setupLocalAudio() {
        audioEl = document.querySelector("audio");
        if (audioEl) {
            mediaType = "audio";
            console.log("Local audio player detected");
            
            // Use requestAnimationFrame for smooth updates
            function pollTime() {
                if (!audioEl.paused && !audioEl.ended) {
                    updateHighlights(audioEl.currentTime);
                }
                requestAnimationFrame(pollTime);
            }
            
            audioEl.addEventListener("play", () => {
                requestAnimationFrame(pollTime);
            });
            
            // Fallback for seeking when paused
            audioEl.addEventListener("seeked", () => {
                updateHighlights(audioEl.currentTime);
            });
        }
    }

    // --- YouTube API Setup ---
    function setupYouTube() {
        const iframe = document.querySelector(".video-thumbnail iframe");
        if (!iframe) return;
        
        // Get YouTube Video ID from iframe src
        const src = iframe.getAttribute("src");
        const match = src.match(/\/embed\/([^?#]+)/);
        if (!match) return;
        const videoId = match[1];
        
        mediaType = "youtube";
        console.log("YouTube iframe detected, Video ID:", videoId);
        
        // Add ID to iframe if missing
        if (!iframe.id) {
            iframe.id = "yt-player-iframe";
        }
        
        // Load YouTube Iframe API if not loaded
        if (!window.YT) {
            const tag = document.createElement("script");
            tag.src = "https://www.youtube.com/iframe_api";
            const firstScriptTag = document.getElementsByTagName("script")[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        }
        
        // Create player when API is ready
        window.onYouTubeIframeAPIReady = window.onYouTubeIframeAPIReady || function() {
            createYTPlayer(iframe.id);
        };
        
        // If API is already loaded
        if (window.YT && window.YT.Player) {
            createYTPlayer(iframe.id);
        }
    }

    function createYTPlayer(elementId) {
        ytPlayer = new YT.Player(elementId, {
            events: {
                onStateChange: (event) => {
                    if (event.data === YT.PlayerState.PLAYING) {
                        pollYTTime();
                    }
                }
            }
        });
    }

    function pollYTTime() {
        if (ytPlayer && ytPlayer.getPlayerState() === YT.PlayerState.PLAYING) {
            const currTime = ytPlayer.getCurrentTime();
            updateHighlights(currTime);
            requestAnimationFrame(pollYTTime);
        }
    }

    // Initialize all
    initWordSpans();
    setupLocalAudio();
    if (!audioEl) {
        setupYouTube();
    }
});
