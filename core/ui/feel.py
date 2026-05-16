import asyncio


# =========================
# THINK EFFECT (SIMULATION)
# =========================
async def think(update, render, text="⚙️ İşleniyor..."):
    await render(update, text)
    await asyncio.sleep(0.4)


# =========================
# SUCCESS MESSAGE STYLE
# =========================
async def success(update, render, text="✅ Tamamlandı"):
    await render(update, text)


# =========================
# ERROR MESSAGE STYLE
# =========================
async def error(update, render, text="⚠️ Bir hata oluştu"):
    await render(update, text)


# =========================
# WELCOME PERSONALITY
# =========================
def greet(name=None):
    if name:
        return f"👋 Selam {name}, buradayım."
    return "👋 Selam, buradayım."
