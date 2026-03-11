import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from database import init_db, save_log

load_dotenv()
init_db()

# ── ALL Models ───────────────────────────────────────────────────
ALL_MODELS = [
    {"provider": "groq",   "model": "gemma2-9b-it"},
    {"provider": "groq",   "model": "llama-3.1-8b-instant"},
    {"provider": "groq",   "model": "mixtral-8x7b-32768"},
    {"provider": "groq",   "model": "llama3-8b-8192"},
    {"provider": "groq",   "model": "llama-3.3-70b-versatile"},
    {"provider": "gemini", "model": "gemini-2.0-flash"},
    {"provider": "gemini", "model": "gemini-1.5-flash"},
]


def get_working_llm():
    for entry in ALL_MODELS:
        provider = entry["provider"]
        model    = entry["model"]
        try:
            print(f"🔄 Trying [{provider}] {model}...")

            if provider == "groq":
                llm = ChatGroq(
                    model=model,
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                    temperature=0
                )
            else:
                llm = ChatGoogleGenerativeAI(
                    model=model,
                    google_api_key=os.getenv("GEMINI_API_KEY"),
                    temperature=0
                )

            # Quick test
            llm.invoke("Say OK")
            print(f"✅ Working: [{provider}] {model}")
            return llm, provider, model

        except Exception as e:
            err = str(e)
            if any(x in err for x in ["429", "rate_limit", "quota", "decommission"]):
                print(f"⚠️  [{provider}] {model} rate limited, trying next...")
                time.sleep(0.3)
                continue
            else:
                print(f"❌  [{provider}] {model} error: {err[:80]}")
                continue

    return None, None, None


def debug_code(broken_code: str, error_message: str, language: str = "Python"):
    """
    Direct LLM call — no agent, no tools, no iteration limit.
    Fast, reliable, works on ALL free models.
    """
    start = time.time()

    # Get working model
    llm, provider, model_name = get_working_llm()

    if llm is None:
        return (
            "⏳ All models rate limited.\n\nWait 10-60 mins and try again.",
            "_All providers exhausted._"
        )

    # Build messages
    system_msg = SystemMessage(content="""You are an expert Python debugging assistant.
When given broken code and an error message:
1. Identify exactly what is wrong
2. Fix the code
3. Explain the fix clearly

Always respond in this format:

FIXED CODE:
```python
[the complete fixed code here]
```

EXPLANATION:
[clear explanation of what was wrong and how you fixed it]""")

    user_msg = HumanMessage(content=f"""Please fix this broken {language} code.

BROKEN CODE:
```{language.lower()}
{broken_code}
```

ERROR MESSAGE:
{error_message}

Give me the fixed code and explain what was wrong.""")

    # Thinking log
    thinking = f"""### 🧠 Agent Thinking Process

**Step 1 — 🔍 Model Selected**
- Provider: `{provider}`
- Model: `{model_name}`

**Step 2 — 📋 Analyzing Error**
- Error: `{error_message}`
- Language: `{language}`

**Step 3 — 🔧 Generating Fix**
- Sending to LLM for direct analysis...

**Step 4 — ✅ Response Received**
- Fix generated successfully!
"""

    try:
        print(f"🔧 Debugging with [{provider}] {model_name}...")
        response = llm.invoke([system_msg, user_msg])
        fixed_code = response.content
        time_taken = time.time() - start

        print(f"✅ Fixed in {round(time_taken, 2)}s")

        save_log(
            broken_code=broken_code,
            error_msg=error_message,
            fixed_code=fixed_code,
            status="success",
            time_taken=round(time_taken, 2)
        )

        return fixed_code, thinking

    except Exception as e:
        time_taken = time.time() - start
        err_msg = str(e)

        save_log(
            broken_code=broken_code,
            error_msg=error_message,
            fixed_code=None,
            status="failed",
            time_taken=round(time_taken, 2)
        )

        if "429" in err_msg or "rate_limit" in err_msg or "quota" in err_msg:
            return (
                "⏳ Rate limit reached.\nWait 10-60 minutes and try again.",
                "_Rate limit hit during generation._"
            )

        return f"❌ Error:\n{err_msg}", thinking
