import re

with open(r'h:\Mijn Drive\HTML FILES\PRAAT JE MEE NIEUW\thema-8-1-2ster.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update T values
def shift_step_text(match):
    # match is the whole "sXnum: '...'" string
    string = match.group(0)
    
    # We need to replace the /13, van 13, of 13 etc with 15
    string = re.sub(r'13', '15', string)
    
    # Shift numbers >= 5 by adding 2
    def shift_num(m):
        num = int(m.group(0))
        if num >= 5 and num < 15:
            return str(num + 2)
        return m.group(0)
        
    # Find the current step number and shift it using regex lookbehind or direct replacement of digits
    # Since step number is first digit or part of "Stap X", "Adım X", we can just replace the first \d+ if it's < 14
    
    parts = string.split(':')
    key = parts[0]
    val = ':'.join(parts[1:])
    
    # regex to find digit before " / 15", " van 15", " of 15" or just find digits in the string
    # we know val looks like "'Stap 5 van 15 ...'"
    def repl_val(m):
        n = int(m.group(1))
        if n >= 5 and n <= 13:
            return str(n + 2)
        return str(n)
        
    val = re.sub(r'(?<!s)(\d+)(?=\s+(van|of|/|من|مرحله|из)\s+15)', repl_val, val)
    # Also for pashto/arabic it might be right to left, let's just shift ANY standalone digit that equals the expected one
    
    return string

# We will just write a custom JS function to append the step num so we don't have to regex fragile RTL translations!
