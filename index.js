const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Root route - API running test
app.get("/", (req, res) => {
  res.send("✅ Video Downloader API is running!");
});

// POST /api/download
app.post('/api/download', (req, res) => {
  const { url } = req.body;

  // Input check
  if (!url) {
    return res.status(400).json({ error: '❌ URL is missing in request body' });
  }

  // yt-dlp command to get direct video link
  exec(`yt-dlp -f best -g "${url}"`, (err, stdout, stderr) => {
    if (err || !stdout.trim()) {
      return res.status(500).json({ error: stderr || "⚠️ Failed to fetch video link" });
    }

    // stdout = direct video URL
    const videoUrl = stdout.trim().split('\n')[0];

    res.json({
      status: "success",
      videoUrl
    });
  });
});

// Start server
app.listen(port, () => {
  console.log(`🚀 Server is running on port ${port}`);
});