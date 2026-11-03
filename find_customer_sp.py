import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('proof-tap-signin-walkthrough.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'CUSTOMER SMARTPHONE', text, re.I):
    pos = m.start()
    line = text[:pos].count('\n') + 1
    print(f"Line {line}: {text[pos-50:pos+80].replace(chr(10), ' ')}")
