import os
import hashlib
import requests
from flask import Flask
from threading import Thread
from datetime import datetime

TOKEN = "9191245417:AAGcmBNQNwsUJTUcM6G72TfQhtGAMTB9KDo"
URL = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

@app.route('/')
def home():
    return "Dieng VIP Bot - Moteur Mort Subite Actif !"

def run_bot():
    try:
        requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true", timeout=10)
    except:
        pass
    
    offset = 0
    last_msg_id = 0
    while True:
        try:
            res = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
            if res.status_code == 200:
                data = res.json()
                for update in data.get("result", []):
                    update_id = update["update_id"]
                    offset = update_id + 1
                    
                    msg = update.get("message")
                    if not msg: continue
                    msg_id = msg.get("message_id", 0)
                    if msg_id <= last_msg_id: continue
                    last_msg_id = msg_id
                    
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "").strip()
                    if not text: continue
                    
                    if text == "/start":
                        reply = "👑 **DIENG VIP BOT - FC26 PENALTY PRO** 👑\n\n✨ Envoyez une affiche (ex: `PSG vs Real Madrid`) pour obtenir une analyse VIP unique et dynamique !"
                        requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": reply, "parse_mode": "Markdown"})
                    elif not text.startswith("/"):
                        parts = [p.strip() for p in text.split("vs")] if "vs" in text else [text, "Visiteur"]
                        t1 = parts[0]
                        t2 = parts[1] if len(parts) > 1 else "Visiteur"
                        
                        # Hachage unique basé sur les noms des équipes
                        h1 = int(hashlib.md5(t1.encode()).hexdigest(), 16)
                        h2 = int(hashlib.md5(t2.encode()).hexdigest(), 16)
                        
                        # Moteur à haute amplitude : variation complète des scores de 3 à 11+ buts
                        volatility = (h1 + h2) % 100
                        
                        if volatility < 25:  
                            # Régime Mort Subite / Scores fleuves (ex: 8-7, 10-9, 11-10)
                            base_score = 7 + (h1 % 4)  # Entre 7 et 10
                            loser_score = base_score - (1 if h1 % 2 == 0 else 2)
                            winner_score = base_score
                            regime = "⚡ Alerte Mort Subite & Volatilité Maximale"
                        elif volatility < 60:  
                            # Régime Intensité Moyenne/Haute (ex: 5-4, 6-5, 7-6)
                            winner_score = 5 + (h2 % 3)  # Entre 5 et 7
                            loser_score = winner_score - 1
                            regime = "🔥 Régime Intensité & Duel Serré"
                        else:  
                            # Régime Standard / Ouvert (ex: 4-3, 6-4, 5-3)
                            winner_score = 4 + (h1 % 3)  # Entre 4 et 6
                            loser_score = winner_score - (1 if h2 % 2 == 0 else 2)
                            if loser_score < 2: loser_score = 2
                            regime = "🎯 Régime Standard - Maîtrise des Tirs"

                        # Attribution aléatoire du vainqueur
                        if (h1 * h2) % 2 == 0:
                            score_a, score_b = winner_score, max(2, loser_score)
                            winner = t1
                        else:
                            score_a, score_b = max(2, loser_score), winner_score
                            winner = t2
                            
                        # Scores alternatifs totalement dynamiques (sans jamais descendre sous 2 pour le perdant)
                        alt_a = max(2, score_a + (1 if h1 % 3 == 0 else -1))
                        alt_b = max(2, score_b + (1 if h2 % 3 == 0 else -1))
                        if alt_a == alt_b: alt_a += 1
                        
                        total_goals = score_a + score_b
                        line_goals = total_goals - 0.5
                        
                        # Indicateurs VIP variables à chaque match
                        missed_pens = 1.5 + (h1 % 4)  # Varie de 1.5 à 4.5 manqués
                        confidence = 97.2 + ((h1 % 24) / 10)  # Varie entre 97.2% et 99.5%
                        pair_str = "Oui" if total_goals % 2 == 0 else "Non"
                        
                        msg_out = (
                            f"🔥 **DIENG PREDICT VIP — ANALYSE EXPERT FC26** 🔥\n"
                            f"──────────────────────────────\n"
                            f"⚽ **Affiche :** `{t1} vs {t2}`\n"
                            f"📌 **Contexte :** *{regime}*\n\n"
                            f"🏆 **1. VERDICT & HIÉRARCHIE**\n"
                            f"• **Vainqueur Validé :** `🏆 {winner}`\n\n"
                            f"🎯 **2. SCORES EXACTS & MARCHÉS**\n"
                            f"• **Option 1 (Principal) :** `{t1} {score_a} - {score_b} {t2}`\n"
                            f"• **Option 2 (Alternatif) :** `{t1} {alt_a} - {alt_b} {t2}`\n"
                            f"• **Volume de Buts :** `Plus de {line_goals} buts`\n\n"
                            f"📈 **3. TENDANCES MARCHÉ**\n"
                            f"• **Total Pair :** `{pair_str}`\n"
                            f"• **Pénalties Manqués :** `Plus de {missed_pens} manqués`\n"
                            f"──────────────────────────────\n"
                            f"💎 **Indice de Confiance VIP :** `{confidence:.1f}%`"
                        )
                        
                        requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": msg_out, "parse_mode": "Markdown"})
        except Exception as e:
            print("Erreur:", e)

if __name__ == '__main__':
    t = Thread(target=run_bot)
    t.start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
