/**
 * Interactive Transcript Audio Synchronizer for "NOS in Makkelijke Taal"
 * Supports both HTML5 <audio> elements and YouTube Iframe API.
 */
(function() {
    let mediaType = null; // 'audio' or 'youtube'
    let audioEl = null;
    let ytPlayer = null;
    let wordSpans = [];
    let pollActive = false;
    
    // Auto-scroll configuration
    const autoScrollEnabled = true;
    let lastScrollTime = 0;
    
    // Initialize word spans
    function initWordSpans() {
        wordSpans = Array.from(document.querySelectorAll("span.w"));
        console.log(`Word highlighter: found ${wordSpans.length} spans`);
        
        // Add click listener to seek to the start time of the word
        wordSpans.forEach(span => {
            span.onclick = () => {
                const start = parseFloat(span.getAttribute("data-start"));
                if (!isNaN(start)) {
                    // Apply offset to seek time so clicking a word jumps to the correct audio position
                    const offset = window.currentAudioOffset || 0;
                    seekToTime(start + offset);
                }
            };
        });
    }

    function seekToTime(seconds) {
        // Ensure time doesn't go below 0
        const targetTime = Math.max(0, seconds);
        if (mediaType === "audio" && audioEl) {
            audioEl.currentTime = targetTime;
            audioEl.play().catch(() => {});
        } else if (mediaType === "youtube" && ytPlayer && typeof ytPlayer.seekTo === "function") {
            ytPlayer.seekTo(targetTime, true);
            ytPlayer.playVideo();
        }
    }

    // High frequency time updates
    function updateHighlights(currentTime) {
        // Read offset dynamically from window.currentAudioOffset
        // If audio runs ahead of highlights, offset should be negative (e.g. -8.5s)
        const offset = window.currentAudioOffset || 0;
        const adjustedTime = currentTime - offset;
        
        let activeSpan = null;
        
        wordSpans.forEach(span => {
            const start = parseFloat(span.getAttribute("data-start"));
            const end = parseFloat(span.getAttribute("data-end"));
            
            if (!isNaN(start) && !isNaN(end) && adjustedTime >= start && adjustedTime <= end) {
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
            console.log("Local audio player detected:", audioEl.src);
            
            // Remove old listeners
            audioEl.removeEventListener("play", startPolling);
            audioEl.removeEventListener("pause", stopPolling);
            audioEl.removeEventListener("ended", stopPolling);
            audioEl.removeEventListener("seeked", onSeeked);
            
            // Add new listeners
            audioEl.addEventListener("play", startPolling);
            audioEl.addEventListener("pause", stopPolling);
            audioEl.addEventListener("ended", stopPolling);
            audioEl.addEventListener("seeked", onSeeked);
            
            // Start polling if already playing
            if (!audioEl.paused && !audioEl.ended) {
                startPolling();
            } else {
                // Initial highlight update
                updateHighlights(audioEl.currentTime);
            }
        }
    }
    
    function startPolling() {
        if (pollActive) return;
        pollActive = true;
        
        function poll() {
            if (!pollActive) return;
            if (audioEl) {
                updateHighlights(audioEl.currentTime);
                requestAnimationFrame(poll);
            }
        }
        requestAnimationFrame(poll);
    }
    
    function stopPolling() {
        pollActive = false;
    }
    
    function onSeeked() {
        if (audioEl) {
            updateHighlights(audioEl.currentTime);
        }
    }

    // --- YouTube API Setup ---
    function setupYouTube() {
        const iframe = document.querySelector(".video-thumbnail iframe");
        if (!iframe) return;
        
        const src = iframe.getAttribute("src");
        const match = src.match(/\/embed\/([^?#]+)/);
        if (!match) return;
        const videoId = match[1];
        
        mediaType = "youtube";
        console.log("YouTube iframe detected, Video ID:", videoId);
        
        if (!iframe.id) {
            iframe.id = "yt-player-iframe";
        }
        
        if (!window.YT) {
            const tag = document.createElement("script");
            tag.src = "https://www.youtube.com/iframe_api";
            const firstScriptTag = document.getElementsByTagName("script")[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
        }
        
        window.onYouTubeIframeAPIReady = window.onYouTubeIframeAPIReady || function() {
            createYTPlayer(iframe.id);
        };
        
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

    // Expose public method to re-initialize sync logic dynamically
    window.initPlayerSync = function() {
        stopPolling();
        initWordSpans();
        setupLocalAudio();
        if (!audioEl) {
            setupYouTube();
        }
    };

    // Auto-run on DOM load
    document.addEventListener("DOMContentLoaded", () => {
        window.initPlayerSync();
    });
})();
