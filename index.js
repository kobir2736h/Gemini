const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// yt-dlp লোকাল path
const ytdlpPath = './bin/yt-dlp';

// Root route (test)
app.get("/", (req, res) => {
  res.send("✅ Video Downloader API is running!");
});

// POST /api/download route
app.post('/api/download', (req, res) => {
  const { url } = req.body;

  if (!url) return res.status(400).json({ error: 'URL is required' });

  // yt-dlp কমান্ড লোকাল path দিয়ে চালাও
  exec(`${ytdlpPath} -f best -g "${url}"`, (err, stdout, stderr) => {
    if (err || !stdout.trim()) {
      return res.status(500).json({ error: stderr || 'Failed to get video URL' });
    }

    const videoUrl = stdout.trim().split('\n')[0];

    res.json({
      status: 'success',
      videoUrl
    });
  });
});

app.listen(port, () => {
  console.log(`🚀 Server running on port ${port}`);
});