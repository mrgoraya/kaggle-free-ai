# Kaggle Free AI — Qwen3.5 + OpenCode + Claude Code

Kaggle ke **free GPU** par Qwen3.5 (35B) chalao aur apne laptop ke **OpenCode** ya **Claude Code** (9router ke zariye) se use karo. Coding + ffmpeg video editing, bilkul free.

## Zaroorat

- Kaggle account (phone verified)
- Laptop par Node.js aur ffmpeg
- OpenCode: `npm install -g opencode-ai`
- (Optional) 9router + Claude Code: `npm install -g 9router @anthropic-ai/claude-code`

## Step 1: Kaggle par model chalao

1. Kaggle par naya notebook banao.
2. Settings mein **Accelerator: GPU T4 x2** aur **Internet: On** karo.
3. [`kaggle_qwen_cell.py`](kaggle_qwen_cell.py) ka poora code **ek hi cell** mein paste karo aur Run dabao.
4. 5–10 minute baad output mein aap ka URL aayega, jaise:
   `https://xxxx.trycloudflare.com/v1`

Settings (script ke top par):

| Setting | Default | Kab change karein |
|---|---|---|
| `MODEL` | `qwen3.5:35b-a3b` | Out of memory ho to `qwen3.5:9b` |
| `CONTEXT` | `131072` (128K) | `ollama ps` mein CPU dikhe to `65536` |

## Step 2: OpenCode connect karo

1. [`opencode.example.json`](opencode.example.json) ko copy karo yahan:
   - Mac/Linux: `~/.config/opencode/opencode.json`
   - Windows: `C:\Users\<name>\.config\opencode\opencode.json`
2. `baseURL` mein apna Kaggle URL daalo (end mein `/v1` zaroor ho).
3. `opencode` chalao → `/models` → **Qwen3.5 35B (Kaggle)** select karo.

## Step 3 (optional): Claude Code via 9router

1. `9router` chalao → dashboard `http://localhost:20128`.
2. **Providers → Add Anthropic Compatible** → name `kaggle`, Base URL = aap ka Kaggle tunnel URL.
3. **Add API Key** → kuch bhi likho (jaise `ollama`).
4. Available Models mein `qwen3.5:35b-a3b` add karo → test karo (green tick).
5. **CLI Tools → Claude Code** → slots mein `kg-prod/qwen3.5:35b-a3b` (ya jo naam 9router dikhaye) select karo → **Apply**.
6. Terminal mein `claude` chalao.

## Zaroori baatein

- Kaggle har hafte ~30 ghante free GPU deta hai; session ~12 ghante baad band ho jaata hai.
- Har naye session mein **naya URL** milta hai — OpenCode aur 9router dono mein update karo.
- Tunnel URL kisi ke saath share mat karo; us par password nahi hota.
- Kaam khatam ho to cell **Stop** karo aur session band karo.
