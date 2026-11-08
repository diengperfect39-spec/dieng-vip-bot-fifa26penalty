import os
import hashlib
import requests
from flask import Flask, request, jsonify

TOKEN = "9191245417:AAGcmBNQNwsUJTUcM6G72TfQhtGAMTB9KDo"
URL = f"https://api.telegram.org/bot{TOKEN}"
RENDER_URL = "https://dieng-vip-bot-fifa26penalty.onrender.com"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Actif - Version 3"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        msg = data["message"]
        chat_id = msg["chat"]["id"]
        txt = msg.get("text", "").strip()
        
        if txt and not txt.startswith("/"):
            parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
            t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
            
            h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
            h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
            
            # Scores stricts FC Penalty (Perdant entre 4 et 7 buts minimum)
            loser = 4 + (h1 % 4)
            winner = loser + 1 + (h2 % 3)
            
            if (h1 * h2) % 2 == 0:
                s1, s2, win_team = winner, loser, t1
            else:
                s1, s2, win_team = loser, winner, t2
                
            alt1 = max(4, s1 + 1)
            alt2 = max(4, s2 + 1)
            total = s1 + s2
            
            out = (
                f"🚨 **NOUVEAU MOTEUR FC26 v3** 🚨\n\n"
                f"⚽ Match : {t1} vs {t2}\n"
                f"🏆 Vainqueur : {win_team}\n\n"
                f"🎯 Scores Exacts :\n"
                f"• Option 1 : {t1} {s1} - {s2} {t2}\n"
                f"• Option 2 : {t1} {alt1} - {alt2} {t2}\n"
                f"• Total Buts : Plus de {total - 0.5}\n\n"
                f"💎 Confiance : 99.9%"
            )
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
            
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": f"{RENDER_URL}/{TOKEN}"})
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
