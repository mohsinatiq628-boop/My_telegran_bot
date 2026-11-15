import os
import json
from http.server import BaseHTTPRequestHandler
import requests
from groq import Groq

TELEGRAM_TOKEN = "9180651050:AAE_QZpDvXDTLZ4CnXpcb4F0Y8hAzbRPoQA"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                user_message = update["message"]["text"]
                
                # Groq AI se reply lena
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant running on Telegram."},
                        {"role": "user", "content": user_message}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                reply = chat_completion.choices[0].message.content
                
                # Telegram par message wapas bhejna
                url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                requests.post(url, json={"chat_id": chat_id, "text": reply})
        except Exception as e:
            print(f"Error: {e}")
            
        self.send_response(200)
        self.end_headers()
        return
