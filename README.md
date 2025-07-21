# Export Unshitter for Google AI Studio

A simple Python script to clean up verbose JSON exports from Google AI Studio, removing metadata, thoughts, and other junk to create a clean conversational history.

## The Problem

When you export a chat from Google AI Studio, the resulting JSON is filled with the model's internal thoughts (I'm not even sure if it re-reads them) and a lot of metadata like`isThought`, `tokenCount`, `finishReason`, etc.

This "shit" pollutes the context when you want to feed the history back to an LLM, wastes a massive amount of tokens, and can cause you to hit API rate limits much faster.

**Example: an 80,000 token reduction on a single chat history!**

## The Solution

This script parses the exported JSON and strips it down to the bare essentials: a list of objects containing only `role` and `text`.

### Before:
```json
{
    "text": "Hi, can i...",
    "role": "user",
    "tokenCount": 49
},
{
  "text": "**Reviewing User Intent**\n\nI\u0027m focusing now on understanding the user\u0027s..blah-blah-blah",
  "role": "model",
  "isThought": true,
  "finishReason": "STOP",
  "tokenCount": 1593,
  "thinkingBudget": -1,
  "thoughtSignatures": ["", "", ""]
}, 
{
  "text": "Yes, **you can**... blah-blah-blah",
  "role": "model",
  "finishReason": "STOP",
  "tokenCount": 120
}
```
### After:
```json
{
    "text": "Hi, can i ...",
    "role": "user"
},
{
    "text": "Yes, **you can**... blah-blah-blah",
    "role": "model"
}
```

## Usage
Requires Python 3. No external libraries needed.
```bash
python main.py <input_file> <output_file.json>
```

## Examples
### [Before (view full file)](before.json)
Here is an example of a "dirty" JSON export:
```json
{
  "chunkedPrompt": {
    "chunks": [{
      "text": "Hi! just write hi!",
      "role": "user",
      "tokenCount": 7
    }, {
      "text": "**Focusing on Core Instruction**\n\nI\u0027ve zeroed in on the user\u0027s explicit command: \"just write hi!\". The initial greeting is now properly considered a conversational opener.  My analysis of this single instruction is complete, and I\u0027m ready to proceed with execution.\n\n\n**Refining Response Delivery**\n\nI\u0027ve carefully considered the user\u0027s simple request, dissecting its intent and implications. My understanding is now cemented: deliver \"hi!\" without embellishment. I\u0027ve re-evaluated my analysis and determined it\u0027s complete. My task is now to generate the required text precisely and efficiently.\n\n\n",
      "role": "model",
      "isThought": true,
      "thinkingBudget": -1,
      "thoughtSignatures": ["", ""]
    }, {
      "text": "hi!",
      "role": "model",
      "finishReason": "STOP"
    }],
  }
}
```
### [After (view full file)](after.json)
And here is the clean, unshitted result:
```json
[
  {
    "text": "Hi! just write hi!",
    "role": "user"
  },
  {
    "text": "hi!",
    "role": "model"
  }
]
```