from core.features.engine import execute

print("🟣 PHASE 20 FULL TEST START\n")

tests = [
    "ping",
    "hava durumu",
    "internette ara yapay zeka",
    "kod çalıştır",
    "hafıza"
]

for t in tests:
    print("INPUT:", t)
    print(execute(t))
    print("-" * 50)

print("\n🟢 PHASE 20 FULL TEST END")
