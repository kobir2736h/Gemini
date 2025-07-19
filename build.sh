#!/bin/bash

# bin ফোল্ডার বানাও (যেখানে yt-dlp রাখবে)
mkdir -p bin

# yt-dlp ডাউনলোড কর ./bin/yt-dlp তে
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ./bin/yt-dlp

# executable কর
chmod +x ./bin/yt-dlp

# version চেক
./bin/yt-dlp --version

echo "✅ yt-dlp installed locally in ./bin/"