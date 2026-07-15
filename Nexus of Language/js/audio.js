/* Nexus of Language — audio playback, three-tier fallback:
   1) pre-generated ElevenLabs mp3 in audio/<slug>.mp3 (best quality, correct
      male/female voice baked in at generation time)
   2) Google Translate TTS (nl) — a gender-appropriate browser voice can't be
      chosen here, but it's only a fallback
   3) browser SpeechSynthesisUtterance, picking a male/female nl voice when
      one is available
   opts: { id?, text, lang?, gender? }  gender = 'm' | 'f' (default 'f'). */

const Audio_ = (() => {
  function slugify(text) {
    return String(text)
      .toLowerCase()
      .replace(/[.,?!;:()'"\/\\:*<>|]/g, '')
      .trim()
      .replace(/\s+/g, '_');
  }

  function pickVoice(lang, gender) {
    if (!('speechSynthesis' in window)) return null;
    const voices = window.speechSynthesis.getVoices() || [];
    const langPrefix = lang.slice(0, 2);
    const matching = voices.filter(v => v.lang && v.lang.toLowerCase().startsWith(langPrefix));
    if (!matching.length) return null;
    const wantMale = gender === 'm';
    const nameHints = wantMale
      ? ['male', 'man', 'xander', 'daan', 'ruben', 'diederik']
      : ['female', 'vrouw', 'lotte', 'femke', 'ellen', 'saskia'];
    const hinted = matching.find(v => nameHints.some(h => v.name.toLowerCase().includes(h)));
    return hinted || matching[0];
  }

  function speakBrowser(text, lang, gender) {
    if (!('speechSynthesis' in window)) return;
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = lang === 'nl' ? 'nl-NL' : 'en-US';
    utter.rate = 0.85; // a touch slower for NT2 clarity
    const v = pickVoice(utter.lang, gender);
    if (v) utter.voice = v;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utter);
  }

  function speakGoogleTTS(text, lang, onFail) {
    const url = `https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=${lang}&q=${encodeURIComponent(text)}`;
    const a = new Audio(url);
    a.onerror = () => onFail();
    a.play().catch(() => onFail());
  }

  function playAudio(opts) {
    const text = opts.text || '';
    const lang = opts.lang || 'nl';
    const gender = opts.gender === 'm' ? 'm' : 'f';
    const id = opts.id || slugify(text);
    if (!text && !id) return;

    const fallback = () => {
      if (text) speakGoogleTTS(text, lang, () => speakBrowser(text, lang, gender));
    };
    const mp3 = new Audio(`audio/${id}.mp3`);
    mp3.onerror = fallback;
    mp3.play().catch(fallback);
  }

  // Some browsers populate voices asynchronously; nudge them to load.
  if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => {};
    try { window.speechSynthesis.getVoices(); } catch (e) {}
  }

  return { playAudio, slugify };
})();
