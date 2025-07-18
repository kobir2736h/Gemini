from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# 🔄 .env ফাইল থেকে ভেরিয়েবল লোড করা
load_dotenv()

app = Flask(__name__, template_folder="templates")

# 🔐 .env থেকে API key নেওয়া
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Gemini API Call Function
def get_gemini_response(user_input):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    payload = {
        "contents": [
            {
                "parts": [{"text": user_input}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload, params=params)

    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response")
    else:
        return f"Error: {response.json()}"

# ✅ Home Route
@app.route("/")
def home():
    return render_template("index.html")

# ✅ API Route
@app.route("/chat", methods=["GET"])
def chat():
    user_message = request.args.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_text = get_gemini_response(user_message)

    return jsonify({"reply": response_text})

# ✅ Run Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
