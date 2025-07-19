#!/bin/bash
# --------------------------------------
# 📦 yt-dlp installer for Linux server
# ✅ Use in Render, Replit, Railway, etc.
# --------------------------------------

echo "🔄 Installing yt-dlp..."

# Download yt-dlp binary to global bin directory
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp

# Make it executable
chmod a+rx /usr/local/bin/yt-dlp

# Test the installation
yt-dlp --version
echo "✅ yt-dlp installed successfully!"