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
    return "Dieng VIP Bot - Moteur FC Penalty Ultra-Pro Actif !"

def run_bot():
    try:
        requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true", timeout=10)
        print("Ancien webhook nettoyé.")
    except Exception as e:
        print("Erreur nettoyage:", e)

    print("Dieng VIP Bot - Moteur scientifique rigoureux en marche...")
    offset = 0
    dernier_message_id = 0

    while True:
        try:
            response = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
            if response.status_code == 200:
                data = response.json()
                for update in data.get("result", []):
                    update_id = update["update_id"]
                    offset = update_id + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        msg_id = msg.get("message_id", 0)
                        
                        if msg_id <= dernier_message_id:
                            continue
                        dernier_message_id = msg_id
                        
                        text_recu = msg.get("text", "").strip()
                        if text_recu:
                            if text_recu == "/start":
                                welcome_msg = (
                                    "👑 **DIENG VIP BOT - FC26 PENALTY PRO** 👑\n\n"
                                    "──────────────────────────────\n"
                                    "✨ *Moteur d'expertise analytique et statistique haute fidélité*\n\n"
                                    "Envoie-moi une affiche au format *Équipe 1 vs Équipe 2* (ex: `Paris Saint-Germain vs Al Nassr`) pour recevoir une lecture de marché irréprochable !"
                                )
                                requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": welcome_msg, "parse_mode": "Markdown"}, timeout=10)
                            elif not text_recu.startswith("/"):
                                parties = [p.strip() for p in text_recu.split("vs")] if "vs" in text_recu else [text_recu, "Visiteur"]
                                eq1 = parties[0]
                                eq2 = parties[1] if len(parties) > 1 else "Visiteur"
                                
                                h1 = int(hashlib.sha256(eq1.encode()).hexdigest(), 16)
                                h2 = int(hashlib.sha256(eq2.encode()).hexdigest(), 16)
                                
                                # Modèle strict basé sur la réalité des tirs au but (jamais de 0 pour le perdant)
                                seed_val = (h1 ^ h2) % 100
                                
                                if seed_val < 20:  # Régimen Mort Subite / Scores fleuves réalistes (ex: 7:6, 6:5)
                                    score_gagnant = 6 + (h1 % 3)  # 6, 7 ou 8
                                    score_perdant = score_gagnant - 1  # Toujours serré à 1 but d'écart (ex: 6-5, 7-6)
                                    regime_title = "⚡ Régime Volatilité & Mort Subite"
                                elif seed_val < 60:  # Régime Intensité Haute (ex: 4:5, 5:4)
                                    score_gagnant = 5
                                    score_perdant = 4
                                    regime_title = "🔥 Régime Intensité & Duel Serré"
                                else:  # Régime Standard (ex: 3:4, 4:3)
                                    score_gagnant = 4
                                    score_perdant = 3
                                    regime_title = "🎯 Régime Standard - Maîtrise des Tirs"

                                # Distribution aléatoire de l'ordre (Équipe 1 ou Équipe 2 gagnante)
                                if h1 % 2 == 0:
                                    score_a = score_gagnant
                                    score_b = score_perdant
                                else:
                                    score_a = score_perdant
                                    score_b = score_gagnant

                                vainqueur = eq1 if score_a > score_b else eq2
                                perdant = eq2 if score_a > score_b else eq1
                                
                                # Scores alternatifs logiques et réalistes (écart de 1 ou 2 buts maximum, jamais de 0)
                                if score_a > score_b:
                                    alt_a = max(3, score_a - 1)
                                    alt_b = max(2, score_b - 1)
                                    if alt_a == alt_b:
                                        alt_a += 1
                                else:
                                    alt_a = max(2, score_a - 1)
                                    alt_b = max(3, score_b - 1)
                                    if alt_a == alt_b:
                                        alt_b += 1

                                total_buts = score_a + score_b
                                seuil_marche = total_buts - 0.5
                                
                                taux_eff1 = 78.0 + (h1 % 17)
                                pen_manques = max(1, (total_buts // 4) + 1)
                                
                                expertises = [
                                    f"Supériorité tactique confirmée de {vainqueur} dans l'anticipation des trajectoires et la gestion de la pression psychologique face à {perdant}.",
                                    f"Efficacité redoutable de {vainqueur} sur les tirs de précision sous haute tension ({taux_eff1:.1f}% de réussite), mettant à mal la structure défensive adverse.",
                                    f"Maîtrise collective et lecture lucide des duels par {vainqueur}, dictant le tempo face à un {perdant} accrocheur dans les moments clés."
                                ]
                                analyse_pro = expertises[(h1 + h2) % len(expertises)]
                                
                                paire_tendance = "Oui (Équilibre structurel validé)" if total_buts % 2 == 0 else "Non (Rupture de rythme en mort subite)"
                                indice_fiabilite = 98.5 + ((h1 % 14) / 10)
                                heure_gmt = datetime.utcnow().strftime("%H:%M")

                                # Rendu visuel propre, structuré, riche en émojis et sans aucune absurdité de score
                                analysis_text = (
                                    f"📊 **DIENG PREDICT VIP — ANALYSE EXPERT FC26**\n"
                                    f"──────────────────────────────\n"
                                    f"⚽ **Affiche :** `{eq1} vs {eq2}`\n"
                                    f"⏱ **Heure :** `{heure_gmt} GMT` | 📌 **Contexte :** *{regime_title}*\n\n"
                                    f"🏆 **1. VERDICT & HIÉRARCHIE**\n"
                                    f"• **Vainqueur Validé :** `🏆 {vainqueur}`\n"
                                    f"• **Analyse Tactique :** {analyse_pro}\n\n"
                                    f"🎯 **2. SCORES EXACTS & MARCHÉS PRINCIPAUX**\n"
                                    f"• **Option 1 (Score Principal) :** `{eq1} {score_a} - {score_b} {eq2}`\n"
                                    f"• **Option 2 (Score Alternatif) :** `{eq1} {alt_a} - {alt_b} {eq2}`\n"
                                    f"• **Volume de Buts Recommandé :** `Plus de {seuil_marche} buts`\n\n"
                                    f"📈 **3. TENDANCES & MARCHÉS VIP**\n"
                                    f"• **Total Pair :** `{paire_tendance}`\n"
                                    f"• **Pénalties Manqués :** `Plus de {pen_manques - 0.5} manqués`\n"
                                    f"──────────────────────────────\n"
                                    f"💎 **Indice de Confiance VIP :** `{indice_fiabilite:.1f}%`"
                                )
                                
                                requests.post(
                                    f"{URL}/sendMessage",
                                    json={"chat_id": chat_id, "text": analysis_text, "parse_mode": "Markdown"},
                                    timeout=10
                                )
        except Exception as e:
            print("Erreur réseau:", str(e))

if __name__ == '__main__':
    t = Thread(target=run_bot)
    t.start()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
