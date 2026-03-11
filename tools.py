import os
import subprocess
from langchain.tools import tool
from executor import execute_code
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def run_python_code(code: str) -> str:
    """Run Python code to test if it works. Input must be valid Python code string."""
    result = execute_code(code)
    if result["status"] == "success":
        return f"SUCCESS: Code works! Output: {result['output']}"
    else:
        return f"FAILED: {result['error']}"


@tool
def search_stackoverflow(query: str) -> str:
    """Search web for Python error fix. Input should be the error type like 'NameError fix'."""
    try:
        results = tavily_client.search(
            query=f"python {query} fix solution",
            max_results=2
        )
        output = "Solutions found:\n"
        for i, r in enumerate(results["results"], 1):
            output += f"{i}. {r['title']}: {r['content'][:200]}\n"
        return output
    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def analyze_error(error_message: str) -> str:
    """Analyze Python error type and meaning. Input should be the error message."""
    error_types = {
        "NameError": "Variable used before being defined. Fix: define the variable first.",
        "TypeError": "Wrong data type used. Fix: convert to correct type.",
        "IndexError": "List index out of range. Fix: check list length before accessing.",
        "KeyError": "Dictionary key not found. Fix: check key exists first.",
        "SyntaxError": "Invalid Python syntax. Fix: check brackets, colons, indentation.",
        "ImportError": "Module not found. Fix: pip install the missing module.",
        "AttributeError": "Object missing property. Fix: check object type and available methods.",
        "ValueError": "Wrong value passed. Fix: validate input before passing.",
        "ZeroDivisionError": "Dividing by zero. Fix: check denominator is not zero.",
        "IndentationError": "Wrong indentation. Fix: use consistent spaces or tabs."
    }

    for error_type, explanation in error_types.items():
        if error_type in error_message:
            return f"Error: {error_type}. {explanation}"

    return f"Unknown error: {error_message}. Search for solution online."
