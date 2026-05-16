from core.screen import screen
from core.ui.spa import build_ui


@screen("home")
async def home(update, render):

    title, kb = build_ui("🏠 ANA MENÜ", [
        [
            {"text": "👤 Profil", "data": "profil"},
            {"text": "📊 Durum", "data": "durum"}
        ],
        [
            {"text": "⚙️ Ayarlar", "data": "ayarlar"},
            {"text": "❓ Yardım", "data": "yardım"}
        ]
    ])

    await render(title, kb)


@screen("profil")
async def profil(update, render):

    title, kb = build_ui("👤 PROFİL", [
        [{"text": "📄 Bilgiler", "data": "info"}],
        [{"text": "🔙 Geri", "data": "back"}]
    ])

    await render(title, kb)


@screen("durum")
async def durum(update, render):

    title, kb = build_ui("📊 DURUM", [
        [{"text": "🚀 Sistem", "data": "system"}],
        [{"text": "🔙 Geri", "data": "back"}]
    ])

    await render(title, kb)


@screen("ayarlar")
async def ayarlar(update, render):

    title, kb = build_ui("⚙️ AYARLAR", [
        [{"text": "🔐 Güvenlik", "data": "security"}],
        [{"text": "🎨 UI", "data": "ui"}],
        [{"text": "🔙 Geri", "data": "back"}]
    ])

    await render(title, kb)


@screen("yardım")
async def yardım(update, render):

    title, kb = build_ui("❓ YARDIM", [
        [{"text": "📖 Komutlar", "data": "cmd"}],
        [{"text": "💬 Destek", "data": "support"}],
        [{"text": "🔙 Geri", "data": "back"}]
    ])

    await render(title, kb)
