#!/usr/bin/env python3
# Fix HANDOFF.md to keep only 10 session blocks

with open('research/HANDOFF.md', 'r') as f:
    handoff_content = f.read()

# Split into session blocks
lines = handoff_content.strip().split('\n')
session_blocks = []
current_block = []
for line in lines:
    if line.startswith('**Session ') and line.endswith(' note.**'):
        if current_block:
            session_blocks.append('\n'.join(current_block))
        current_block = [line]
    else:
        current_block.append(line)
if current_block:
    session_blocks.append('\n'.join(current_block))

# Keep only last 10 (drop oldest)
session_blocks = session_blocks[-10:]

# Write back
new_handoff = '\n\n'.join(session_blocks) + '\n'

with open('research/HANDOFF.md', 'w') as f:
    f.write(new_handoff)

print(f"HANDOFF.md fixed: {len(session_blocks)} session blocks kept")
for i, block in enumerate(session_blocks):
    first_line = block.split('\n')[0]
    print(f"  {i+1}. {first_line[:80]}...")

# Also update notes_count in campaign_state.json if needed
import json
with open('research/campaign_state.json', 'r') as f:
    campaign_state = json.load(f)

if campaign_state['notes_count'] != 10:
    campaign_state['notes_count'] = 10
    with open('research/campaign_state.json', 'w') as f:
        json.dump(campaign_state, f, separators=(', ', ': '))
    print("campaign_state.json notes_count updated to 10")
else:
    print("campaign_state.json notes_count already 10")