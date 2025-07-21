import sys
import json
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    role: str

if len(sys.argv) < 3:
    print("Usage: python unshit.py <filename> <output_file>")
    sys.exit(1)

filename = sys.argv[1]
with open(filename, 'r') as f:
    current_chunk = None
    try:
        data = json.load(f)
        history = data['chunkedPrompt']['chunks']
        res = []
        for h in history:
            if not h.get('isThought') and h.get('text'):
                chunk = Chunk(text=h['text'], role=h['role'])
                current_chunk = chunk
                res.append(chunk)
        output_file = sys.argv[2]
        with open(output_file, 'w') as f:
            f.write(json.dumps([chunk.__dict__ for chunk in res], indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error processing file {e} at chunk {current_chunk}")
        sys.exit(1)

print(f"Processed {len(res)} chunks from {filename} and saved to {output_file}.")
