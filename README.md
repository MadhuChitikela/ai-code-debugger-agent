# 🤖 AI Code Debugger Agent

> Autonomous AI agent that fixes broken Python code — no human needed.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange)
![Gradio](https://img.shields.io/badge/UI-Gradio-red)

---

## 🎯 What It Does

Paste broken code + error message → AI analyzes, fixes, and explains — automatically.

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq LLaMA 3.3 + Gemini Fallback |
| Framework | LangChain |
| UI | Gradio |
| Database | SQLite |
| Deployment | HuggingFace Spaces |

## 🚀 How to Run Locally

```bash
git clone https://github.com/MadhuChitikela/ai-code-debugger-agent
cd ai-code-debugger-agent
pip install -r requirements.txt
```

Create `.env` file:
```
GROQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

Run:
```bash
python main.py
```

## 💡 Example

Input:
```python
def greet():
    print(massage)
greet()
```
Error: `NameError: name 'massage' is not defined`

Output: Fixed code + explanation ✅

## 🏗️ Architecture

```
User Input (broken code + error)
          ↓
   Multi-Model LLM
   (Groq → Gemini fallback)
          ↓
   Fix Generated
          ↓
   SQLite Logged
          ↓
   Result Displayed
```

## 📊 Features

- ✅ Auto fixes Python + JavaScript errors
- ✅ Multi-model fallback (7 models across 2 providers)
- ✅ Session history + analytics dashboard
- ✅ Professional dark UI
- ✅ All sessions logged to SQLite
