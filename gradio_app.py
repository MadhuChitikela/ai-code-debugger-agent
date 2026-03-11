import gradio as gr
from agent import debug_code
from database import get_all_logs, get_stats, clear_history

# ═══════════════════════════════════════════════════════════════════
#  DESIGN: Terminal-Noir × Premium SaaS
#  Deep blacks · Electric cyan · Monospaced precision
#  Feels like: Vercel × Linear × VSCode had a baby
# ═══════════════════════════════════════════════════════════════════

CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Bricolage+Grotesque:wght@400;500;600;700;800&display=swap');

:root {
  /* LIGHT: Clean Glass Light Blue */
  --bg0:       #f0f9ff;
  --bg-gradient: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  --bg1:       rgba(255, 255, 255, 0.7);
  --bg2:       rgba(255, 255, 255, 0.5);
  --bg3:       rgba(255, 255, 255, 0.8);
  --border:    rgba(255, 255, 255, 0.6);
  --border2:   rgba(14, 165, 233, 0.15);
  --cyan:      #0284c7;
  --cyan-dim:  rgba(2, 132, 199, 0.10);
  --cyan-glow: rgba(2, 132, 199, 0.22);
  --green:     #16a34a;
  --green-dim: rgba(22, 163, 74, 0.09);
  --red:       #ef4444;
  --text:      #0f172a;
  --text2:     #334155;
  --text3:     #475569;
  --mono:      'DM Mono', monospace;
  --sans:      'Bricolage Grotesque', sans-serif;
  --r:         12px;
  --r2:        16px;
  --glass-blur: blur(16px);
}

.dark {
  /* DARK: Not too dark (Slate Mode) */
  --bg0:       #0f172a;
  --bg-gradient: none;
  --bg1:       #1e293b;
  --bg2:       #334155;
  --bg3:       #475569;
  --border:    rgba(255,255,255,0.08);
  --border2:   rgba(255,255,255,0.12);
  --cyan:      #38bdf8;
  --cyan-dim:  rgba(56, 189, 248, 0.10);
  --cyan-glow: rgba(56, 189, 248, 0.22);
  --green:     #34d399;
  --green-dim: rgba(52, 211, 153, 0.09);
  --red:       #f87171;
  --text:      #f8fafc;
  --text2:     #cbd5e1;
  --text3:     #94a3b8;
  --glass-blur: none;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body { 
  background-color: var(--bg0) !important;
  background-image: var(--bg-gradient) !important;
  background-attachment: fixed !important;
}
footer, .svelte-1ipelgc { display: none !important; }

.gradio-container {
  background: transparent !important;
  font-family: var(--sans) !important;
  max-width: 100% !important;
  padding: 0 !important;
  overflow-x: hidden !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

/* ── Topbar ── */
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 32px; height: 56px;
  background: var(--bg1); border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100; 
  backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);
}
.logo { display: flex; align-items: center; gap: 10px; }
.logo-mark {
  width: 28px; height: 28px; background: var(--cyan);
  border-radius: 6px; display: flex; align-items: center; justify-content: center;
  font-family: var(--mono); font-size: 11px; font-weight: 500; color: #fff;
  box-shadow: 0 2px 8px var(--cyan-glow);
}
.logo-name { font-size: 15px; font-weight: 700; color: var(--text); letter-spacing: -0.02em; }
.topbar-right { display: flex; align-items: center; gap: 16px; }
.pill-green {
  display: flex; align-items: center; gap: 6px;
  background: var(--green-dim); border: 1px solid rgba(0,255,136,0.18);
  border-radius: 100px; padding: 5px 12px;
  font-family: var(--mono); font-size: 11px; color: var(--green); font-weight: 500;
}
.dot-green {
  width: 6px; height: 6px; background: var(--green);
  border-radius: 50%; animation: blink 2.2s ease-in-out infinite; box-shadow: 0 0 6px var(--green);
}
@keyframes blink {
  0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.8)}
}
.ver { font-family: var(--mono); font-size: 11px; color: var(--text3); }

/* ── Hero ── */
.hero {
  padding: 50px 32px 40px; background: transparent;
  position: relative; overflow: hidden;
}
.eyebrow {
  font-family: var(--mono); font-size: 11px; letter-spacing: .15em;
  text-transform: uppercase; color: var(--cyan); margin-bottom: 16px; font-weight: 600;
}
.h1 {
  font-size: 48px; font-weight: 800; line-height: 1.05;
  letter-spacing: -.03em; color: var(--text); margin-bottom: 16px;
}
.h1 em { font-style: normal; color: var(--cyan); }
.hdesc { font-size: 16px; color: var(--text2); line-height: 1.6; max-width: 540px; }
.steps { display: flex; align-items: center; gap: 8px; margin-top: 24px; flex-wrap: wrap; }
.chip {
  display: flex; align-items: center; gap: 6px;
  background: var(--bg1); border: 1px solid var(--border);
  border-radius: 100px; padding: 6px 14px;
  font-family: var(--mono); font-size: 11px; color: var(--text2);
  backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);
}
.chip-n {
  width: 16px; height: 16px; background: var(--cyan-dim); border-radius: 50%;
  display:flex; align-items:center; justify-content:center;
  font-size: 10px; color: var(--cyan); font-weight: 600;
}
.arr { color: var(--text3); font-size: 12px; }

/* ── Tabs ── */
div.tabs > div.tab-nav {
  background: transparent !important; border-bottom: 1px solid var(--border2) !important;
  padding: 0 32px !important; gap: 0 !important;
}
div.tabs > div.tab-nav > button {
  font-family: var(--sans) !important; font-size: 14px !important;
  font-weight: 600 !important; color: var(--text3) !important;
  padding: 14px 20px !important; border: none !important;
  border-bottom: 2px solid transparent !important;
  background: transparent !important; border-radius: 0 !important;
  margin: 0 !important; transition: all .2s !important;
}
div.tabs > div.tab-nav > button:hover { color: var(--text2) !important; }
div.tabs > div.tab-nav > button.selected {
  color: var(--cyan) !important; border-bottom-color: var(--cyan) !important;
}

/* ── Tab Body ── */
.tabitem { background: transparent !important; padding: 32px !important; }

/* ── Section Divider ── */
.sdiv {
  display: flex; align-items: center; gap: 12px; margin-bottom: 16px;
}
.slbl {
  font-family: var(--mono); font-size: 11px; letter-spacing: .12em;
  text-transform: uppercase; color: var(--text3); white-space: nowrap; font-weight: 600;
}
.sline { flex: 1; height: 1px; background: var(--border2); }

/* ── Form Elements ── */
.block { background: transparent !important; }
.block > label > span {
  font-family: var(--mono) !important; font-size: 11px !important;
  font-weight: 600 !important; letter-spacing: .1em !important;
  text-transform: uppercase !important; color: var(--text3) !important;
  margin-bottom: 8px !important; display: block !important;
}
textarea, input[type="text"], .wrap-inner {
  background: var(--bg1) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important; color: var(--text) !important;
  font-family: var(--mono) !important; font-size: 13.5px !important;
  line-height: 1.7 !important; padding: 16px !important;
  transition: all .2s !important;
  caret-color: var(--cyan) !important;
  backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);
  box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
  position: relative; z-index: 10;
}
textarea:focus, input[type="text"]:focus {
  border-color: var(--cyan) !important;
  box-shadow: 0 0 0 3px var(--cyan-dim) !important;
  outline: none !important; background: var(--bg1) !important;
}
textarea::placeholder { color: var(--text3) !important; font-size: 13px !important; }
.wrap { background: transparent !important; }

/* ── Buttons ── */
button.primary, button.lg {
  background: var(--cyan) !important; color: #fff !important;
  border: none !important; border-radius: var(--r) !important;
  font-family: var(--sans) !important; font-weight: 700 !important;
  font-size: 15px !important; letter-spacing: -.01em !important;
  padding: 16px 32px !important; cursor: pointer !important;
  transition: all .2s !important;
  box-shadow: 0 4px 14px var(--cyan-glow) !important;
  width: 100% !important;
}
button.primary:hover {
  filter: brightness(1.1) !important;
  box-shadow: 0 6px 20px rgba(2,132,199,.3) !important;
  transform: translateY(-2px) !important;
}
button.primary:active { transform: translateY(0) !important; }

button.secondary {
  background: var(--bg1) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important; color: var(--text2) !important;
  font-family: var(--sans) !important; font-weight: 600 !important; font-size: 14px !important;
  transition: all .2s !important;
  backdrop-filter: var(--glass-blur);
}
button.secondary:hover {
  background: var(--bg3) !important; color: var(--text) !important;
}

/* ── Output Code ── */
.out-code textarea {
  background: var(--bg1) !important;
  border-color: rgba(22, 163, 74, .3) !important;
  color: var(--text) !important; font-size: 13.5px !important;
  font-weight: 500 !important;
}
.out-code textarea:focus {
  border-color: var(--green) !important;
  box-shadow: 0 0 0 3px var(--green-dim) !important;
}
.dark .out-code textarea { color: #9dffc8 !important; border-color: rgba(0,255,136,.14) !important;}

/* ── Thinking trace ── */
.trace-box {
  background: var(--bg1) !important; border: 1px solid var(--border) !important;
  border-left: 4px solid var(--cyan) !important;
  border-radius: var(--r) !important; padding: 20px !important;
  backdrop-filter: var(--glass-blur); box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
}

/* ── Copy btn ── */
.copy-text-button {
  background: var(--bg3) !important; border: 1px solid var(--border2) !important;
  border-radius: 6px !important; color: var(--text2) !important;
}

/* ── Markdown ── */
.prose, .prose * { color: var(--text) !important; font-family: var(--sans) !important; }
.prose h3 {
  font-size: 11px !important; font-weight: 700 !important;
  letter-spacing: .12em !important; text-transform: uppercase !important;
  color: var(--text3) !important; margin: 24px 0 12px !important;
  padding-bottom: 8px !important; border-bottom: 1px solid var(--border2) !important;
}
.prose h4 { font-size: 15px !important; font-weight: 800 !important; margin: 24px 0 10px !important; color: var(--text) !important; }
.prose table { width: 100% !important; border-collapse: collapse !important; font-size: 14px !important; }
.prose thead tr { background: var(--bg2) !important; }
.prose th {
  padding: 12px 18px !important; text-align: left !important;
  font-size: 11px !important; font-weight: 700 !important;
  letter-spacing: .1em !important; text-transform: uppercase !important;
  color: var(--text3) !important; border-bottom: 1px solid var(--border2) !important;
  font-family: var(--mono) !important;
}

/* ── Custom HTML Dashboard Cards ── */
.dash-card {
  background: var(--bg1); border: 1px solid var(--border);
  border-radius: var(--r); padding: 20px;
  backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
  margin-bottom: 16px; transition: transform 0.2s;
}
.dash-card:hover { transform: translateY(-2px); border-color: var(--cyan-dim); }
.dash-stat-row {
  display: flex; justify-content: space-between; padding: 12px 0;
  border-bottom: 1px solid var(--border2);
}
.dash-stat-row:last-child { border-bottom: none; }
.dash-lbl { color: var(--text2); font-size: 13px; font-weight: 500; font-family: var(--sans); }
.dash-val { color: var(--text); font-size: 14px; font-weight: 700; font-family: var(--mono); }
.dash-val.cyan { color: var(--cyan); }

.hist-item {
  background: var(--bg2); border: 1px solid var(--border2);
  border-left: 3px solid var(--border2);
  border-radius: 8px; padding: 14px 16px; margin-bottom: 10px;
  display: flex; flex-direction: column; gap: 6px;
}
.hist-item.success { border-left-color: var(--green); }
.hist-item.failed { border-left-color: var(--red); }
.hist-top { display: flex; justify-content: space-between; align-items: center; }
.hist-id { font-family: var(--mono); font-size: 11px; font-weight: 600; color: var(--cyan); }
.hist-time { font-family: var(--mono); font-size: 10px; color: var(--text3); }
.hist-err { font-family: var(--mono); font-size: 12px; color: var(--text); background: var(--bg3); padding: 4px 8px; border-radius: 4px; border: 1px solid var(--border2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
.hist-bot { display: flex; justify-content: space-between; align-items: center; margin-top: 4px;}
.hist-badge { font-size: 10px; font-family: var(--mono); font-weight: 600; padding: 2px 8px; border-radius: 100px; }
.hist-badge.success { background: var(--green-dim); color: var(--green); }
.hist-badge.failed { background: rgba(239, 68, 68, 0.1); color: var(--red); }
.hist-dur { font-family: var(--mono); font-size: 10px; color: var(--text3); }

.prose td {
  padding: 14px 18px !important; border-bottom: 1px solid var(--border2) !important;
  color: var(--text) !important; font-family: var(--mono) !important;
  font-size: 13px !important; background: var(--bg1) !important;
}
.prose tr:last-child td { border-bottom: none !important; }
.prose tr:hover td { background: var(--bg2) !important; transition: background .15s; }
.prose code {
  background: var(--bg2) !important; border: 1px solid var(--border) !important;
  border-radius: 6px !important; padding: 2px 8px !important;
  font-family: var(--mono) !important; font-size: 12.5px !important; color: var(--cyan) !important;
}
.prose pre {
  background: var(--bg1) !important; border: 1px solid var(--border) !important;
  border-radius: var(--r) !important; padding: 20px !important; overflow-x: auto !important;
  backdrop-filter: var(--glass-blur);
}
.prose pre code {
  background: none !important; border: none !important;
  color: var(--cyan) !important; padding: 0 !important;
}
.dark .prose pre code { color: #a8c0ff !important; }

.prose strong { color: var(--text) !important; font-weight: 800 !important; }
.prose hr { border: none !important; border-top: 1px solid var(--border2) !important; margin: 24px 0 !important; }
.prose p { color: var(--text2) !important; line-height: 1.7 !important; margin-bottom: 14px !important; }
.prose em { color: var(--text2) !important; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.tabitem > * { animation: fadeUp .3s ease forwards; }
"""

# ── Helpers ───────────────────────────────────────────────────────
def fix_my_code(broken_code, error_message, language):
    if not broken_code.strip():
        return "⚠  Please paste your broken code first.", "_Waiting for input..._", render_stats(), render_history()
    if not error_message.strip():
        error_message = "Unknown error — analyze and fix"
    try:
        result, thinking = debug_code(broken_code, error_message, language)
        return result, thinking, render_stats(), render_history()
    except Exception as e:
        return f"❌  Agent error:\n\n{str(e)}", "_Agent encountered an error._", render_stats(), render_history()


def render_stats():
    s = get_stats()
    return f"""
<div class="dash-card">
  <div class="dash-stat-row"><span class="dash-lbl">Total Sessions</span><span class="dash-val">{s['total']}</span></div>
  <div class="dash-stat-row"><span class="dash-lbl">Successful Fixes</span><span class="dash-val">{s['success']}</span></div>
  <div class="dash-stat-row"><span class="dash-lbl">Failed Attempts</span><span class="dash-val" style="color:var(--red);">{s['failed']}</span></div>
  <div class="dash-stat-row"><span class="dash-lbl">Success Rate</span><span class="dash-val cyan">{s['success_rate']}</span></div>
  <div class="dash-stat-row"><span class="dash-lbl">Avg Fix Time</span><span class="dash-val">{s['avg_time']}</span></div>
</div>
"""

def render_history():
    logs = get_all_logs()
    if not logs:
        return "<div class='dash-card' style='text-align:center; color:var(--text3);'>_No sessions yet. Run your first debug above!_</div>"
    
    out = ""
    for log in logs[:10]: # Limit to 10 latest for cleaner UI
        id_, ts, err, status, t = log
        status_cls = "success" if status == "success" else "failed"
        badge_text = "FIXED" if status == "success" else "FAILED"
        
        # Clean the error message to fit beautifully in the card
        clean_err = str(err).replace("\\n", " ").replace("\\r", "").replace("|", "-")
        
        out += f"""
        <div class="hist-item {status_cls}">
            <div class="hist-top">
                <span class="hist-id">Session #{id_}</span>
                <span class="hist-time">{ts}</span>
            </div>
            <div class="hist-err">{clean_err}</div>
            <div class="hist-bot">
                <span class="hist-badge {status_cls}">{badge_text}</span>
                <span class="hist-dur">{t}s execution</span>
            </div>
        </div>
        """
    return out


# ── App ───────────────────────────────────────────────────────────
with gr.Blocks(
    title="AI Code Debugger — Autonomous Agent",
    css=CSS,
    theme=gr.themes.Base(
        primary_hue="cyan",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Bricolage Grotesque")],
        font_mono=[gr.themes.GoogleFont("DM Mono")],
    )
) as app:

    # ── Topbar ────────────────────────────────────────────────────
    gr.HTML("""
    <div class="topbar">
      <div class="logo">
        <div class="logo-mark">AI</div>
        <span class="logo-name">Code Debugger Agent</span>
      </div>
      <div class="topbar-right">
        <div class="pill-green"><span class="dot-green"></span>Agent Online</div>
        <span class="ver">LLaMA 3.3 · ReAct · v1.0</span>
      </div>
    </div>
    """)

    # ── Hero ──────────────────────────────────────────────────────
    gr.HTML("""
    <div class="hero">
      <div class="eyebrow">// Autonomous Debugging Agent</div>
      <h1 class="h1">Break it. <em>We'll fix it.</em></h1>
      <p class="hdesc">
        Paste broken code and the error. The agent autonomously analyzes,
        searches, patches, and validates — until it runs.
      </p>
      <div class="steps">
        <div class="chip"><span class="chip-n">1</span>Analyze</div>
        <span class="arr">→</span>
        <div class="chip"><span class="chip-n">2</span>Search</div>
        <span class="arr">→</span>
        <div class="chip"><span class="chip-n">3</span>Patch</div>
        <span class="arr">→</span>
        <div class="chip"><span class="chip-n">4</span>Validate</div>
        <span class="arr">→</span>
        <div class="chip"><span class="chip-n">5</span>Return Fix</div>
      </div>
    </div>
    """)

    # ── Tabs ──────────────────────────────────────────────────────
    with gr.Tabs():

        # ──── TAB 1: DEBUGGER ────
        with gr.Tab("⚡  Debugger"):
            with gr.Row(equal_height=False):

                with gr.Column(scale=5):
                    gr.HTML('<div class="sdiv"><span class="slbl">Input</span><div class="sline"></div></div>')
                    language = gr.Dropdown(
                        choices=["Python", "JavaScript"],
                        value="Python", label="Language"
                    )
                    code_input = gr.Textbox(
                        label="Broken Code",
                        placeholder="# Paste your broken code here…\\ndef greet():\\n    print(massage)\\n\\ngreet()",
                        lines=13, max_lines=24,
                    )
                    error_input = gr.Textbox(
                        label="Error Message",
                        placeholder="NameError: name 'massage' is not defined",
                        lines=3,
                    )
                    fix_btn = gr.Button("⚡  Start Debug Session", variant="primary", size="lg")

                with gr.Column(scale=5):
                    gr.HTML('<div class="sdiv"><span class="slbl">Solution</span><div class="sline"></div></div>')
                    output = gr.Textbox(
                        label="Fixed Code + Explanation",
                        lines=13, max_lines=24,
                        buttons=["copy"],
                        elem_classes="out-code",
                        placeholder="✓  Patched code appears here…",
                        interactive=False,
                    )
                    gr.HTML('<div class="sdiv" style="margin-top:20px"><span class="slbl">Agent Trace</span><div class="sline"></div></div>')
                    thinking = gr.Markdown(
                        value="_Agent reasoning steps stream here after you click Fix..._",
                        elem_classes="trace-box"
                    )

            gr.HTML('<div class="sdiv" style="margin-top:32px"><span class="slbl">Session Data</span><div class="sline"></div></div>')
            with gr.Row():
                with gr.Column(scale=2):
                    stats_out = gr.HTML(value=render_stats())
                with gr.Column(scale=3):
                    history_out = gr.HTML(value=render_history())

            fix_btn.click(
                fn=fix_my_code,
                inputs=[code_input, error_input, language],
                outputs=[output, thinking, stats_out, history_out]
            )

        # ──── TAB 2: ANALYTICS ────
        with gr.Tab("📊  Analytics"):
            gr.HTML('<div class="sdiv"><span class="slbl">Performance</span><div class="sline"></div></div>')
            with gr.Row():
                with gr.Column(scale=2):
                    a_stats = gr.HTML(value=render_stats())
                with gr.Column(scale=3):
                    a_hist = gr.HTML(value=render_history())
            with gr.Row():
                refresh_btn = gr.Button("↺  Refresh", variant="secondary", size="sm")
                clear_btn = gr.Button("🗑️  Clear History", variant="secondary", size="sm")
            
            refresh_btn.click(fn=lambda: (render_stats(), render_history()), outputs=[a_stats, a_hist])
            
            def handle_clear():
                clear_history()
                return render_stats(), render_history(), render_stats(), render_history()
            
            clear_btn.click(
                fn=handle_clear, 
                outputs=[a_stats, a_hist, stats_out, history_out]
            )

        # ──── TAB 3: EXAMPLES ────
        with gr.Tab("📋  Examples"):
            gr.Markdown("""
### Quick Start Examples

---

#### 01 · NameError
```python
def greet():
    print(massage)
greet()
```
**Error:** `NameError: name 'massage' is not defined`

---

#### 02 · SyntaxError
```python
def add(a, b):
    return a + b
print(add(1, 2)
```
**Error:** `SyntaxError: invalid syntax`

---

#### 03 · TypeError
```python
age = "25"
result = age + 5
print(result)
```
**Error:** `TypeError: can only concatenate str (not "int") to str`

---

#### 04 · IndexError
```python
fruits = ["apple", "banana"]
print(fruits[5])
```
**Error:** `IndexError: list index out of range`

---

#### 05 · ZeroDivisionError
```python
def avg(total, count):
    return total / count
print(avg(100, 0))
```
**Error:** `ZeroDivisionError: division by zero`

---

#### 06 · JavaScript · ReferenceError
```javascript
function greet(name) {
    console.log(`Hello ${usrname}`)
}
greet("Alice")
```
**Error:** `ReferenceError: usrname is not defined`
            """)

        # ──── TAB 4: DOCS ────
        with gr.Tab("📖  Docs"):
            gr.Markdown("""
### How the Agent Works

Uses the **ReAct (Reasoning + Acting)** pattern — same architecture powering
production AI agents at Vercel, Linear, and top AI startups.

---

#### Decision Loop

```
INPUT  →  broken code + error message
THINK  →  What error type is this?
ACT    →  analyze_error(error_message)
THINK  →  What fix should I search for?
ACT    →  search_stackoverflow(query)
THINK  →  Apply fix to the code
ACT    →  run_python_code(fixed_code)
CHECK  →  Did it work?
          YES → return solution
          NO  → loop back (max 10 attempts)
```

---

#### Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Agent | LangChain AgentExecutor |
| Pattern | ReAct (Reason + Act) |
| Search | Tavily Search API |
| Runner | Python subprocess sandbox |
| Memory | LangChain ConversationBufferMemory |
| Storage | SQLite session logs |
| UI | Gradio Blocks |

---

#### Why This Project Gets You Hired

> Agentic AI is the **#1 most demanded skill** in AI engineering in 2026.
> This project proves you can build autonomous systems — not just chatbots.
> ReAct pattern + Tool use + Memory + Deployment = top 1% fresher portfolio.
            """)

    # ── Footer ────────────────────────────────────────────────────
    gr.HTML("""
    <div style="padding:18px 32px;border-top:1px solid var(--border);
        display:flex;align-items:center;justify-content:space-between;background:var(--bg1);
        backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur);">
      <span style="font-family:var(--mono);font-size:11px;color:var(--text3);letter-spacing:.05em;">
        AI Code Debugger Agent &nbsp;·&nbsp; ReAct Pattern &nbsp;·&nbsp; LangChain + Groq + Gradio
      </span>
      <span style="font-family:var(--mono);font-size:11px;color:var(--text3);letter-spacing:.05em;">
        Fresher Portfolio Project · 2026
      </span>
    </div>
    """)


if __name__ == "__main__":
    app.launch(inbrowser=True)
