#!/data/data/com.termux/files/usr/bin/bash

echo "👀 Watcher başladı..."

while inotifywait -r -e modify .; do
    git add .
    git commit -m "auto update"
    git push
    echo "🚀 Push atıldı"
done
