from core.features.engine import execute

print("🟣 PHASE 21 FULL BRAIN TEST START\n")

tests = [
    "ping",
    "hava durumu",
    "internette ara yapay zeka",
    "kod çalıştır",
    "hafıza",
    "neden öğreniyorsun",
    "kendini geliştir",
    "ne yapabiliyorsun"
]

for t in tests:
    print("➡ INPUT:", t)
    result = execute(t)
    print("⬅ OUTPUT:", result)
    print("-" * 60)

print("\n🟢 PHASE 21 TEST END")
