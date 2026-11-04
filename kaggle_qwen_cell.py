# =====================================================================
#  Qwen3.5 on Kaggle GPU  ->  OpenCode / Claude Code (9router) on laptop
#  ONE CELL SCRIPT - copy everything and paste into a single Kaggle cell
# =====================================================================
#  Before running (right sidebar -> Settings):
#    - Accelerator : GPU T4 x2
#    - Internet    : On   (needs a phone-verified Kaggle account)
#
#  What this cell does:
#    1. Installs Ollama (runs the model) and cloudflared (makes a public link)
#    2. Starts the Ollama server with a 128K context window
#    3. Downloads Qwen3.5 (~22 GB) and loads it onto the GPUs
#    4. Opens a Cloudflare tunnel and prints your public URL
#    5. Keeps the cell running so the session does not go idle,
#       and restarts Ollama / the tunnel if they crash
#
#  To stop: click the Stop (square) button on the cell, then stop the session
#  so you don't waste your weekly GPU hours.
# =====================================================================


# ---------------- SETTINGS (change only these two) ----------------
MODEL = "qwen3.5:35b-a3b"   # out of memory? use "qwen3.5:9b"
CONTEXT = "131072"          # 128K tokens. If `ollama ps` shows CPU, use "65536"
HEARTBEAT_MINUTES = 5       # how often the keep-alive loop prints a status line
# ------------------------------------------------------------------

import subprocess, os, time, re, urllib.request, datetime


def sh(cmd):
    """Run a shell command and show it in the output."""
    print(f"\n>>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def ollama_alive():
    """True if the Ollama server answers on port 11434."""
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=5)
        return True
    except Exception:
        return False


# ---------------- STEP 1: install tools ----------------
# zstd + pciutils are needed by the Ollama installer on Kaggle
sh("sudo apt-get install -y zstd pciutils > /dev/null 2>&1")
# Official Ollama installer
sh("curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1")
# cloudflared = free Cloudflare tunnel, no account needed
if not os.path.exists("cloudflared"):
    sh("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/"
       "cloudflared-linux-amd64 -O cloudflared && chmod +x cloudflared")


# ---------------- STEP 2: start the Ollama server ----------------
env = os.environ.copy()
env.update({
    "OLLAMA_HOST": "0.0.0.0:11434",        # listen on all addresses
    "OLLAMA_CONTEXT_LENGTH": CONTEXT,      # model memory (context window)
    "OLLAMA_KEEP_ALIVE": "-1",             # never unload the model from GPU
    "OLLAMA_FLASH_ATTENTION": "1",         # faster + uses less memory
    "OLLAMA_KV_CACHE_TYPE": "q8_0",        # halves the memory used by context
})


def start_ollama():
    """Start `ollama serve` in the background and wait until it is ready."""
    subprocess.Popen(["ollama", "serve"], env=env,
                     stdout=open("ollama.log", "a"), stderr=subprocess.STDOUT)
    for _ in range(60):
        if ollama_alive():
            return True
        time.sleep(1)
    return False


start_ollama()
print("\nOllama server is running")


# ---------------- STEP 3: download + load the model ----------------
sh(f"ollama pull {MODEL}")               # downloads ~22 GB (first time each session)
sh(f'ollama run {MODEL} "say hi"')       # loads the model onto the GPUs
sh("ollama ps")                          # should show 100% GPU and your CONTEXT


# ---------------- STEP 4: open the tunnel ----------------
def start_tunnel():
    """Start a Cloudflare quick tunnel and return its public URL (or None)."""
    open("tunnel.log", "w").close()      # clear the old log
    proc = subprocess.Popen(
        ["./cloudflared", "tunnel", "--url", "http://localhost:11434",
         "--http-host-header", "localhost:11434"],
        stdout=open("tunnel.log", "a"), stderr=subprocess.STDOUT)
    for _ in range(60):
        m = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", open("tunnel.log").read())
        if m:
            return proc, m.group(0)
        time.sleep(1)
    return proc, None


def show_url(url):
    print("\n" + "=" * 60)
    if url:
        print("PASTE THIS URL INTO:")
        print("  - OpenCode : opencode.json -> baseURL   (keep /v1 at the end)")
        print("  - 9router  : kaggle provider -> Edit -> Base URL\n")
        print(f"   {url}/v1")
        print(f"\nModel name: {MODEL}")
    else:
        print("Tunnel failed. Check tunnel.log")
    print("=" * 60, flush=True)


tunnel_proc, url = start_tunnel()
show_url(url)


# ---------------- STEP 5: keep-alive loop ----------------
# This loop keeps the cell "busy", so Kaggle doesn't treat the session as idle.
# It also checks every minute that Ollama and the tunnel are still alive and
# restarts them if needed. If the tunnel restarts, a NEW URL is printed.
# Note: Kaggle still stops every session after ~12 hours, and the weekly
# GPU limit (~30 hours) keeps counting while this runs.
print(f"\nKeep-alive started. Status every {HEARTBEAT_MINUTES} min. "
      "Click Stop on this cell to end it.", flush=True)

minutes = 0
try:
    while True:
        time.sleep(60)
        minutes += 1

        # Restart Ollama if it crashed
        if not ollama_alive():
            print("Ollama stopped - restarting...", flush=True)
            start_ollama()
            subprocess.run(f'ollama run {MODEL} "hi"', shell=True)

        # Restart the tunnel if it died (you will get a new URL)
        if tunnel_proc.poll() is not None:
            print("Tunnel stopped - restarting...", flush=True)
            tunnel_proc, url = start_tunnel()
            show_url(url)

        # Short status line so you can see it's alive
        if minutes % HEARTBEAT_MINUTES == 0:
            now = datetime.datetime.now().strftime("%H:%M")
            print(f"[{now}] alive | running {minutes} min | {url}/v1", flush=True)
except KeyboardInterrupt:
    print("\nKeep-alive stopped. Ollama and the tunnel keep running "
          "until you stop the session.")
