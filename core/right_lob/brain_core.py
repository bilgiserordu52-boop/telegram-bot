# core/right_lob/brain_core.py

class BrainCore:
    def __init__(self):
        self.tool_map = {
            "weather": ["hava", "weather", "yağmur", "sıcaklık"],
            "search": ["ara", "internette", "google", "search"],
            "code": ["kod", "çalıştır", "python", "script"],
            "memory": ["hafıza", "memory", "geçmiş"]
        }

    def detect_intent(self, text: str):
        text = text.lower()

        best_tool = "default"
        best_score = 0

        for tool, keywords in self.tool_map.items():
            score = sum(1 for k in keywords if k in text)

            if score > best_score:
                best_tool = tool
                best_score = score

        confidence = min(1.0, 0.4 + (best_score * 0.2))

        return {
            "tool": best_tool,
            "confidence": round(confidence, 2),
            "score": best_score
        }

    def decide(self, text: str):
        intent = self.detect_intent(text)

        return {
            "selected_tool": intent["tool"],
            "confidence": intent["confidence"],
            "intent_score": intent["score"]
        }
