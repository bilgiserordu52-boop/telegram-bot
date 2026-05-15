#!/data/data/com.termux/files/usr/bin/bash

cd ~/telegram-bot

echo "👀 Watcher başladı..."

while inotifywait -e modify bot.py; do
    echo "🛠 Değişiklik algılandı"

    git add bot.py
    git commit -m "auto deploy $(date)"
    git push

    echo "🚀 GitHub'a gönderildi"
done
