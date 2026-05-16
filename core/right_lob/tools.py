# core/right_lob/tools.py

import requests


# ----------------------------
# TOOL DETECTION ENGINE
# ----------------------------

def detect_tool(text: str):
    """
    Kullanıcının mesajından hangi tool kullanılacağını seçer
    """
    text = text.lower()

    if "hava" in text or "weather" in text:
        return "weather"

    if "ara" in text or "search" in text or "internette" in text:
        return "search"

    if "kod" in text or "çalıştır" in text:
        return "code"

    if "hafıza" in text or "memory" in text:
        return "memory"

    if text.strip() == "ping":
        return "ping"

    return "unknown"


# ----------------------------
# TOOL EXECUTOR
# ----------------------------

def execute_tool(tool: str, query: str = ""):
    """
    Tool execution layer (simulated + real routing)
    """

    # WEATHER TOOL
    if tool == "weather":
        return {
            "tool": "weather",
            "result": "☀️ Hava durumu simülasyonu: Ankara +17°C",
            "success": True
        }

    # SEARCH TOOL
    if tool == "search":
        return {
            "tool": "search",
            "result": f"🔎 '{query}' için arama simülasyonu",
            "success": True
        }

    # CODE TOOL
    if tool == "code":
        return {
            "tool": "code",
            "result": "💻 Kod çalıştırma sandbox (safe mode)",
            "success": True
        }

    # MEMORY TOOL
    if tool == "memory":
        return {
            "tool": "memory",
            "result": "🧠 Hafıza analiz edildi",
            "success": True
        }

    # PING
    if tool == "ping":
        return {
            "tool": "ping",
            "result": "pong",
            "success": True
        }

    return {
        "tool": tool,
        "result": "❌ tool not found",
        "success": False
    }
