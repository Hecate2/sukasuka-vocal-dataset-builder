"""Split a trilingual SRT (Japanese / Chinese / English per-block) into
three language-specific SRT files preserving timing and producing
sequential indices per output file.

Usage:
  python tools/split_bilingual_srt.py <input.srt>

Outputs (same folder as input):
  <basename>.ja.srt  (Japanese)
  <basename>.zh.srt  (Chinese)
  <basename>.en.srt  (English)

This script is conservative: a language output only gets a block if
that language line exists for the block.
"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python split_bilingual_srt.py <input.srt>")
    sys.exit(2)

inp = Path(sys.argv[1])
if not inp.exists():
    print(f"File not found: {inp}")
    sys.exit(1)

text = inp.read_text(encoding='utf-8')
blocks = [b.strip() for b in text.split('\n\n') if b.strip()]

outs = {
    'ja': [],
    'zh': [],
    'en': [],
}

for b in blocks:
    lines = b.splitlines()
    if len(lines) < 2:
        continue
    idx = lines[0].strip()
    timecode = lines[1].strip()
    body = lines[2:]
    # body expected: [ja, zh, en] but may be shorter/longer
    if len(body) >= 1 and body[0].strip():
        outs['ja'].append((timecode, body[0].rstrip()))
    if len(body) >= 2 and body[1].strip():
        outs['zh'].append((timecode, body[1].rstrip()))
    if len(body) >= 3 and body[2].strip():
        outs['en'].append((timecode, body[2].rstrip()))

# write outputs with sequential indices
for code, items in outs.items():
    out_path = inp.with_name(inp.stem + f'.{code}.srt')
    with out_path.open('w', encoding='utf-8') as f:
        for i, (timecode, txt) in enumerate(items, start=1):
            f.write(f"{i}\n")
            f.write(f"{timecode}\n")
            f.write(f"{txt}\n\n")
    print(f"Wrote {out_path} ({len(items)} blocks)")
