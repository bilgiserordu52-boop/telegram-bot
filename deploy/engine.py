import asyncio


async def deploy_module(name, message):

    print("DEPLOY:", name)

    try:
        sent = await message.reply_text(f"🚀 DEPLOY START: {name}")
    except Exception as e:
        print("REPLY ERROR:", e)
        return

    files = [
        "bot.py",
        "config.py",
        "ui/admin_panel.py",
        "deploy/engine.py",
        "core/router.py"
    ]

    total = len(files)

    for i, f in enumerate(files, start=1):

        await asyncio.sleep(0.5)

        try:
            await sent.edit_text(f"🚀 {name} {i}/{total}\n📦 {f}")
        except Exception as e:
            print("EDIT ERROR:", e)

    try:
        await sent.edit_text(f"✅ DEPLOY DONE: {name}")
    except Exception as e:
        print("FINAL ERROR:", e)
