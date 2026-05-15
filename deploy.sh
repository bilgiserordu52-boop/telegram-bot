#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Deploy başlıyor..."

cd ~/telegram-bot || exit

git add .

git commit -m "auto deploy $(date)"

git push origin main

echo "✅ GitHub push tamam"
echo "⏳ Railway otomatik güncelleyecek..."
