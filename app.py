from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
import youtube_dl

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_gemini_response(user_input):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    payload = {
        "contents": [
            {"parts": [{"text": user_input}]}
        ]
    }

    response = requests.post(url, headers=headers, json=payload, params=params)
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
    else:
        return f"Error: {response.text}"

def search_youtube_video_by_id(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json().get("items"):
        item = response.json()["items"][0]
        title = item["snippet"]["title"]
        description = item["snippet"]["description"]
        url = f"https://youtu.be/{video_id}"
        return {"title": title, "description": description, "url": url}
    else:
        return {"error": "Video not found"}

@app.route("/chat")
def chat():
    user_message = request.args.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    reply = get_gemini_response(user_message)
    return jsonify({"reply": reply})

@app.route("/video")
def video():
    video_id = request.args.get("videoid")
    if not video_id:
        return jsonify({"error": "No videoid provided"}), 400
    video_info = search_youtube_video_by_id(video_id)
    return jsonify(video_info)

@app.route("/audio")
def audio():
    video_id = request.args.get("videoid")
    if not video_id:
        return jsonify({"error": "No videoid provided"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'skip_download': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info.get('title', 'No title')
            duration = info.get('duration', 0)

        return jsonify({
            "title": title,
            "duration": duration,
            "audio_url": audio_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)