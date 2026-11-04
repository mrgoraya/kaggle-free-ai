# Kaggle Free AI — Qwen3.5 + OpenCode

Run Qwen3.5 (35B) on Kaggle's **free GPU** and use it from **OpenCode** on your laptop. Coding and ffmpeg video editing, completely free.

## Files in this repo

| File | What to do with it |
|---|---|
| **[`kaggle_qwen_cell.py`](kaggle_qwen_cell.py)** | **This is the script you copy into Kaggle.** Open it, copy everything, paste into one Kaggle cell. |
| [`opencode.example.json`](opencode.example.json) | The OpenCode config for your laptop (Step 2). |
| `README.md` | This guide. |

**How to copy the script:** click [`kaggle_qwen_cell.py`](kaggle_qwen_cell.py) above, then click the **Copy raw file** button (the two-squares icon at the top right of the code). That copies the whole script in one click.

## Requirements

- A Kaggle account (phone verified)
- Node.js and ffmpeg on your laptop
- OpenCode: `npm install -g opencode-ai`

## Step 1: Run the model on Kaggle

1. Create a new notebook on Kaggle.
2. In Settings, set **Accelerator: GPU T4 x2** and **Internet: On**.
3. Open [`kaggle_qwen_cell.py`](kaggle_qwen_cell.py), click **Copy raw file**, paste it into **a single cell**, and click Run.
4. After 5–10 minutes, the output shows your URL, for example:
   `https://xxxx.trycloudflare.com/v1`

Settings (at the top of the script):

| Setting | Default | When to change it |
|---|---|---|
| `MODEL` | `qwen3.5:35b-a3b` | Use `qwen3.5:9b` if you run out of memory |
| `CONTEXT` | `131072` (128K) | Use `65536` if `ollama ps` shows any CPU usage |

## Step 2: Connect OpenCode

1. Open [`opencode.example.json`](opencode.example.json), click **Copy raw file**, and save it as a new file here:
   - Mac/Linux: `~/.config/opencode/opencode.json`
   - Windows: `C:\Users\<name>\.config\opencode\opencode.json`
2. Put your Kaggle URL in `baseURL` (it must end with `/v1`).
3. Run `opencode`, type `/models`, and select **Qwen3.5 35B (Kaggle)**.

## Important notes

- Kaggle gives about 30 hours of free GPU per week; each session stops after about 12 hours.
- Every new session gives you a **new URL**, so update it in `opencode.json`.
- Don't share your tunnel URL; it has no password.
- When you're done, stop the cell and stop the Kaggle session.
