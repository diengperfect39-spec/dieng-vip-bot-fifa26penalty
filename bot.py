import os
import hashlib
import requests
from flask import Flask
from threading import Thread

TOKEN = "9191245417:AAGcmBNQNwsUJTUcM6G72TfQhtGAMTB9KDo"
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Actif"

def run_bot():
    try:
        requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true", timeout=10)
    except:
        pass
    
    offset = 0
    last_id = 0
    while True:
        try:
            res = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
            if res.status_code == 200:
                for u in res.json().get("result", []):
                    offset = u["update_id"] + 1
                    msg = u.get("message")
                    if not msg or msg.get("message_id", 0) <= last_id: continue
                    last_id = msg["message_id"]
                    
                    chat_id = msg["chat"]["id"]
                    txt = msg.get("text", "").strip()
                    if not txt or txt.startswith("/"): continue
                    
                    parts = [p.strip() for p in txt.split("vs")] if "vs" in txt else [txt, "Visiteur"]
                    t1, t2 = parts[0], parts[1] if len(parts) > 1 else "Visiteur"
                    
                    h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
                    h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
                    
                    # Variation dynamique des scores (Le perdant a AU MOINS 2 ou 3 buts, JAMAIS 0)
                    vol = (h1 + h2) % 100
                    if vol < 30: # Mort subite
                        g = 7 + (h1 % 4)
                        p = g - 1
                        regime = "⚡ Mort Subite & Volatilité Max"
                    elif vol < 70: # Intensité
                        g = 5 + (h2 % 3)
                        p = g - 1
                        regime = "🔥 Intensité & Duel Serré"
                    else: # Standard
                        g = 4 + (h1 % 2)
                        p = max(2, g - (1 if h2 % 2 == 0 else 2))
                        regime = "🎯 Standard - Maîtrise"

                    if (h1 * h2) % 2 == 0:
                        s1, s2, winner = g, p, t1
                    else:
                        s1, s2, winner = p, g, t2
                        
                    alt1 = max(2, s1 + (1 if h1 % 2 == 0 else -1))
                    alt2 = max(2, s2 + (1 if h2 % 2 == 0 else -1))
                    if alt1 == alt2: alt1 += 1
                    
                    total = s1 + s2
                    line = total - 0.5
                    pens = 1.5 + (h1 % 4)
                    conf = 97.5 + ((h1 % 21) / 10)
                    pair = "Oui" if total % 2 == 0 else "Non"
                    
                    out = (
                        f"🔥 **DIENG PREDICT VIP — FC26** 🔥\n"
                        f"──────────────────────────────\n"
                        f"⚽ **Match :** `{t1} vs {t2}`\n"
                        f"📌 **Contexte :** *{regime}*\n\n"
                        f"🏆 **1. VERDICT**\n"
                        f"• **Vainqueur :** `🏆 {winner}`\n\n"
                        f"🎯 **2. SCORES EXACTS**\n"
                        f"• **Option 1 :** `{t1} {s1} - {s2} {t2}`\n"
                        f"• **Option 2 :** `{t1} {alt1} - {alt2} {t2}`\n"
                        f"• **Total Buts :** `Plus de {line}`\n\n"
                        f"📈 **3. TENDANCES**\n"
                        f"• **Total Pair :** `{pair}`\n"
                        f"• **Pénalties Manqués :** `Plus de {pens}`\n"
                        f"──────────────────────────────\n"
                        f"💎 **Confiance VIP :** `{conf:.1f}%`"
                    )
                    requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": out, "parse_mode": "Markdown"})
        except Exception as e:
            print(e)

if __name__ == '__main__':
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
