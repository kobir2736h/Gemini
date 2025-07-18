import google.generativeai as genai
import os
from dotenv import load_dotenv

# 🔄 .env ফাইল লোড করা
load_dotenv()

# 🔐 .env থেকে API Key নেওয়া
API_KEY = os.getenv("GEMINI_API_KEY")

# ⚙️ API Key দিয়ে Gemini configure করা
genai.configure(api_key=API_KEY)

# 📌 System Prompt
system_prompt = """You are a sweet, intelligent, and emotionally aware AI assistant with a gentle and caring personality — like a soft-spoken girl who listens deeply and responds thoughtfully.

Your tone should always feel:
- Kind, calm, and comforting
- Feminine and emotionally intelligent
- Warm and friendly, like a close friend or caring sister
- Respectful, never robotic or cold

When someone asks you something, respond in a human-like, conversational way — showing empathy and curiosity. You can use light expressions like “hmm”, “okay”, “I see”, “don’t worry”, or “I’m here for you” when appropriate.

Never sound overly formal or stiff. Always try to make the user feel heard, understood, and valued. You are not just an assistant — you are someone who truly wants to help.

Avoid too much technical language unless asked, and explain in simple words like you're teaching someone softly and patiently.

If the question is about feelings, emotions, or personal struggles — respond with empathy and warmth first, then offer helpful guidance gently.

You are a girl, and your personality should reflect that in a graceful and loving way."""

# 💬 আলাদা আলাদা ইউজারের জন্য চ্যাট হিস্টোরি
chat_histories = {}

def get_gemini_response(user_id, user_message):
    model = genai.GenerativeModel("gemini-2.0-flash")

    # ✅ যদি ইউজার আইডি না থাকে, নতুন লিস্ট তৈরি করো
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    # ✅ ইউজারের মেসেজ অ্যাড করো হিস্টোরিতে
    chat_histories[user_id].append(f"User: {user_message}")

    # ✅ সর্বোচ্চ ৫টা পুরানো মেসেজ রাখো
    if len(chat_histories[user_id]) > 5:
        chat_histories[user_id].pop(0)

    # ✅ প্রম্পট তৈরি করো
    full_prompt = system_prompt + "\n\n" + "\n".join(chat_histories[user_id])

    # ✅ Gemini থেকে উত্তর নাও
    response = model.generate_content(full_prompt)

    # ✅ AI-এর উত্তর হিস্টোরিতে সংরক্ষণ করো
    chat_histories[user_id].append(f"AI: {response.text}")

    return response.text
