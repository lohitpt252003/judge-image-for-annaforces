import re
import os

# Forbidden keywords per language
FORBIDDEN = {
    "python": [
        r"\bimport\s+os\b",
        r"\bimport\s+subprocess\b",
        r"\bimport\s+shutil\b",
        r"\bimport\s+socket\b",
        r"\bimport\s+ctypes\b",
        r"\bimport\s+pathlib\b",
        r"\bfrom\s+os\b",
        r"\bopen\s*\(",
    ],
    "c": [
        r"#\s*include\s*<unistd\.h>",
        r"#\s*include\s*<sys\/",   # blocks sys/socket.h, sys/wait.h etc.
        r"#\s*include\s*<dlfcn\.h>",
        r"system\s*\(",
        r"popen\s*\(",
        r"fork\s*\(",
        r"exec",
    ],
    "c++": [
        r"#\s*include\s*<unistd\.h>",
        r"#\s*include\s*<sys\/",
        r"#\s*include\s*<dlfcn\.h>",
        r"system\s*\(",
        r"popen\s*\(",
        r"fork\s*\(",
        r"exec",
        r"#\s*include\s*<filesystem>",  # optional (lets them explore disk)
    ],
}

def check_code_safety(file_path: str, language: str) -> dict:
    """
    Scans the source file for blacklisted imports/includes.
    Returns {success: bool, reason: str}
    """
    language = language.lower()
    if language not in FORBIDDEN:
        return {"success": True, "reason": "Language not checked"}

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
    except Exception as e:
        return {"success": False, "reason": f"Cannot read file: {e}"}

    for pattern in FORBIDDEN[language]:
        if re.search(pattern, code):
            return {"success": False, "reason": f"Blocked keyword matched: {pattern}"}

    return {"success": True, "reason": "Code passed static check"}
