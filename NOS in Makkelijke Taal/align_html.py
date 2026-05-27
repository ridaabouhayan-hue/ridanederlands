import json
import os
import re
import sys
from html.parser import HTMLParser

class TranscriptAligner(HTMLParser):
    def __init__(self, whisper_words):
        super().__init__()
        self.whisper_words = whisper_words
        self.w_idx = 0
        self.output = []
        
        # State tracking
        self.in_paragraph = False
        self.in_quote_text = False
        self.in_vocab = False
        self.vocab_attrs = {}
        self.vocab_text_buffer = []
        
        # Tags stack
        self.tags_stack = []

    def normalize(self, word):
        # Remove punctuation and lowercase
        return re.sub(r'[^\w\s]', '', word).lower()

    def find_best_match(self, html_word, window=8):
        norm_html = self.normalize(html_word)
        if not norm_html:
            return None, 0
            
        # Try to find the word in a sliding window
        for offset in range(window):
            curr_idx = self.w_idx + offset
            if curr_idx >= len(self.whisper_words):
                break
            norm_whisper = self.normalize(self.whisper_words[curr_idx]["word"])
            if norm_html == norm_whisper or norm_html in norm_whisper or norm_whisper in norm_html:
                return self.whisper_words[curr_idx], offset
                
        # Fallback: if not found, return the next word and advance by 0
        if self.w_idx < len(self.whisper_words):
            return self.whisper_words[self.w_idx], 0
        return None, 0

    def get_timestamps_for_text(self, text):
        # Split text into words and spaces/punctuation
        tokens = re.split(r'(\s+)', text)
        result_tokens = []
        
        for token in tokens:
            if not token.strip():
                # Just whitespace, output as-is
                result_tokens.append(token)
                continue
                
            # It's a word! Clean it up
            # Check if there's trailing punctuation we should separate
            word_match = re.match(r'^([^\w]*)(.*?)([^\w]*)$', token)
            if word_match:
                leading, core_word, trailing = word_match.groups()
            else:
                leading, core_word, trailing = "", token, ""
                
            if core_word:
                match_word, offset = self.find_best_match(core_word)
                if match_word:
                    # Advance the pointer
                    self.w_idx += offset + 1
                    start = match_word["start"]
                    end = match_word["end"]
                    result_tokens.append(f'{leading}<span class="w" data-start="{start}" data-end="{end}">{core_word}</span>{trailing}')
                else:
                    result_tokens.append(token)
            else:
                result_tokens.append(token)
                
        return "".join(result_tokens)

    def handle_starttag(self, tag, attrs):
        self.tags_stack.append((tag, attrs))
        attr_dict = dict(attrs)
        
        # Check if we are entering a target container
        if tag == 'p':
            # Check if inside text-content or topic-card (we assume all <p> inside body are transcript)
            self.in_paragraph = True
        elif tag == 'span' and attr_dict.get('class') == 'quote-text':
            self.in_quote_text = True
        elif tag == 'span' and attr_dict.get('class') == 'vocab':
            self.in_vocab = True
            self.vocab_attrs = attr_dict
            self.vocab_text_buffer = []
            return # Don't output the opening span yet, we will output it in handle_data or handle_endtag

        # Construct tag string
        attr_str = "".join([f' {k}="{v}"' for k, v in attrs])
        self.output.append(f'<{tag}{attr_str}>')

    def handle_endtag(self, tag):
        if self.tags_stack:
            self.tags_stack.pop()
            
        if tag == 'p':
            self.in_paragraph = False
        elif tag == 'span' and self.in_quote_text:
            self.in_quote_text = False
        elif tag == 'span' and self.in_vocab:
            self.in_vocab = False
            # Process the buffered vocab text as a single unit or word
            vocab_text = "".join(self.vocab_text_buffer)
            # Find timestamp for the vocab word
            match_word, offset = self.find_best_match(vocab_text)
            
            # Construct vocab tag with timestamps
            attr_str = "".join([f' {k}="{v}"' for k, v in self.vocab_attrs.items() if k != 'class'])
            if match_word:
                self.w_idx += offset + 1
                start = match_word["start"]
                end = match_word["end"]
                self.output.append(f'<span class="vocab w" data-start="{start}" data-end="{end}"{attr_str}>{vocab_text}</span>')
            else:
                self.output.append(f'<span class="vocab"{attr_str}>{vocab_text}</span>')
            return

        self.output.append(f'</{tag}>')

    def handle_data(self, data):
        if self.in_vocab:
            self.vocab_text_buffer.append(data)
            return
            
        if self.in_paragraph or self.in_quote_text:
            # We are inside a transcript block! Wrap words in spans
            wrapped = self.get_timestamps_for_text(data)
            self.output.append(wrapped)
        else:
            # Outside transcript, output as-is
            self.output.append(data)

    def handle_entityref(self, name):
        self.output.append(f'&{name};')

    def handle_charref(self, name):
        self.output.append(f'&#{name};')

    def handle_comment(self, data):
        self.output.append(f'<!--{data}-->')

    def handle_decl(self, decl):
        self.output.append(f'<!{decl}>')

    def get_html(self):
        return "".join(self.output)

def main():
    if len(sys.argv) < 3:
        print("Gebruik: python align_html.py [html_bestand] [timestamps_json_bestand]")
        print("Voorbeeld: python align_html.py transcript_nos_26mei.html nos_fragment_timestamps.json")
        sys.exit(1)
        
    html_file = sys.argv[1]
    json_file = sys.argv[2]
    
    if not os.path.exists(html_file):
        print(f"FOUT: HTML bestand '{html_file}' niet gevonden.")
        sys.exit(1)
    if not os.path.exists(json_file):
        print(f"FOUT: JSON bestand '{json_file}' niet gevonden.")
        sys.exit(1)
        
    print(f"Inlezen van timestamps uit: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        whisper_words = json.load(f)
        
    print(f"Inlezen van HTML uit: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    print("Uitlijnen van woorden...")
    parser = TranscriptAligner(whisper_words)
    parser.feed(html_content)
    aligned_html = parser.get_html()
    
    # Write to a new file
    output_file = html_file.rsplit('.', 1)[0] + "_aligned.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(aligned_html)
        
    print(f"Klaar! Uitgelijnd HTML bestand opgeslagen als: {output_file}")
    print(f"Verwerkte woorden uit Whisper: {parser.w_idx} / {len(whisper_words)}")

if __name__ == '__main__':
    main()
