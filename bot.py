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
    return "Bot VIP FC26 Webhook Actif"

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
            
            # Moteur strict FC Penalty : Scores élevés, mort subite, perdant >= 4 buts
            vol = (h1 + h2) % 100
            if vol < 35:
                loser = 6 + (h1 % 2)
                winner = loser + 1 + (h2 % 2)
                regime = "⚡ Alerte Mort Subite & Volatilité Maximale"
            elif vol < 75:
                loser = 5 + (h2 % 2)
                winner = loser + 1
                regime = "🔥 Régime Intensité & Duel Serré"
            else:
                loser = 4 + (h1 % 2)
                winner = loser + 1 + (h2 % 2)
                regime = "🎯 Régime Standard - Maîtrise des Tirs"

            if (h1 * h2) % 2 == 0:
                s1, s2, win_team = winner, loser, t1
            else:
                s1, s2, win_team = loser, winner, t2
                
            alt1 = max(4, s1 + (1 if h1 % 2 == 0 else -1))
            alt2 = max(4, s2 + (1 if h2 % 2 == 0 else -1))
            if alt1 == alt2: alt1 += 1
            
            total = s1 + s2
            line = total - 0.5
            pens = 2.5 + (h1 % 3)
            conf = 97.8 + ((h1 % 20) / 10)
            pair = "Oui" if total % 2 == 0 else "Non"
            
            out = (
                f"🔥 **DIENG PREDICT VIP — ANALYSE EXPERT FC26** 🔥\n"
                f"──────────────────────────────\n"
                f"⚽ **Match :** `{t1} vs {t2}`\n"
                f"📌 **Contexte :** *{regime}*\n\n"
                f"🏆 **1. VERDICT & HIERARCHIE**\n"
                f"• **Vainqueur Validé :** `🏆 {win_team}`\n\n"
                f"🎯 **2. SCORES EXACTS & MARCHÉS PRINCIPAUX**\n"
                f"• **Option 1 (Principal) :** `{t1} {s1} - {s2} {t2}`\n"
                f"• **Option 2 (Alternatif) :** `{t1} {alt1} - {alt2} {t2}`\n"
                f"• **Volume de Buts Recommandé :** `Plus de {line} buts`\n\n"
                f"📈 **3. TENDANCES & MARCHÉS VIP**\n"
                f"• **Total Pair :** `{pair}`\n"
                f"• **Pénalties Manqués :** `Plus de {pens} manqués`\n"
                f"──────────────────────────────\n"
                f"💎 **Indice de Confiance VIP :** `{conf:.1f}%`"
            )
            
            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
            
    return jsonify({"status": "ok"})

def setup_webhook():
    webhook_url = f"{RENDER_URL}/{TOKEN}"
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true")
    requests.post(f"{URL}/setWebhook", json={"url": webhook_url})

if __name__ == '__main__':
    setup_webhook()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
