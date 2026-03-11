import subprocess
import sys

def execute_code(code: str) -> dict:
    """
    Safely runs Python code in isolated subprocess
    """
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "output": result.stdout,
                "error": None
            }
        else:
            return {
                "status": "error",
                "output": None,
                "error": result.stderr
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "output": None,
            "error": "Code took too long (10s limit)"
        }
    except Exception as e:
        return {
            "status": "error",
            "output": None,
            "error": str(e)
        }


# Test it
if __name__ == "__main__":
    print("Testing executor...")

    # Test 1 - Working code
    r1 = execute_code("print('Hello World')")
    print("Test 1:", r1)

    # Test 2 - Broken code
    r2 = execute_code("print(undefined_variable)")
    print("Test 2:", r2)
