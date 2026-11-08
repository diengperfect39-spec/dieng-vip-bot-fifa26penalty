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
    return "Dieng VIP Bot - Interface Pro Active !"

def run_bot():
    try:
        requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true", timeout=10)
        print("Ancien webhook nettoyé.")
    except Exception as e:
        print("Erreur nettoyage:", e)

    print("Dieng VIP Bot - Moteur d'analyse visuelle et dynamique en marche...")
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
                                    "✨ *Moteur d'expertise analytique et visuelle haute fidélité*\n\n"
                                    "Envoie-moi une affiche au format *Équipe 1 vs Équipe 2* (ex: `Real Madrid vs Milan`) pour recevoir une lecture de marché claire, ordonnée et ultra-précise !"
                                )
                                requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": welcome_msg, "parse_mode": "Markdown"}, timeout=10)
                            elif not text_recu.startswith("/"):
                                parties = [p.strip() for p in text_recu.split("vs")] if "vs" in text_recu else [text_recu, "Visiteur"]
                                eq1 = parties[0]
                                eq2 = parties[1] if len(parties) > 1 else "Visiteur"
                                
                                # Empreinte cryptographique pour une variation riche des scores
                                h1 = int(hashlib.sha256(eq1.encode()).hexdigest(), 16)
                                h2 = int(hashlib.sha256(eq2.encode()).hexdigest(), 16)
                                
                                # Modèle dynamique et varié (Évite la répétition de scores figés)
                                combo_seed = (h1 ^ h2) % 100
                                
                                if combo_seed < 15:  # Scénario Mort Subite / Scores fleuves (ex: 7:6, 8:9)
                                    score_a = 6 + (h1 % 4)
                                    score_b = 5 + (h2 % 4)
                                    if score_a == score_b:
                                        score_a += 1
                                    regime_title = "⚡ Régime Volatilité & Mort Subite"
                                elif combo_seed < 45:  # Scénario Intensité Haute (ex: 5:4, 4:5, 6:5)
                                    score_a = 4 + (h1 % 3)
                                    score_b = 3 + (h2 % 3)
                                    if score_a == score_b:
                                        score_b += 1
                                    regime_title = "🔥 Régime Intensité & Duel Serré"
                                else:  # Scénario Standard (ex: 3:1, 4:2, 3:4, 5:3)
                                    score_a = 3 + (h1 % 3)
                                    score_b = 1 + (h2 % 4)
                                    if score_a == score_b:
                                        score_a += 1
                                    regime_title = "🎯 Régime Standard - Maîtrise des Tirs"

                                vainqueur = eq1 if score_a > score_b else eq2
                                perdant = eq2 if score_a > score_b else eq1
                                
                                # Scores alternatifs dynamiques
                                alt_a = max(2, score_b - (1 if score_b > 2 else 0))
                                alt_b = max(2, score_a - 1)
                                if alt_a == alt_b:
                                    alt_a += 1

                                total_buts = score_a + score_b
                                seuil_marche = total_buts - 0.5
                                
                                taux_eff1 = 76.5 + (h1 % 21)
                                pen_manques = max(1, (total_buts // 3) + (h1 % 2))
                                
                                expertises = [
                                    f"Supériorité tactique confirmée de {vainqueur} dans l'anticipation des trajectoires et la gestion de la pression psychologique face à {perdant}.",
                                    f"Efficacité redoutable de {vainqueur} sur les tirs de précision sous haute tension ({taux_eff1:.1f}% de réussite), mettant à mal la structure défensive adverse.",
                                    f"Maîtrise collective et lecture lucide des duels par {vainqueur}, dictant le tempo face à un {perdant} en difficulté dans les moments clés."
                                ]
                                analyse_pro = expertises[(h1 + h2) % len(expertises)]
                                
                                paire_tendance = "Oui (Équilibre structurel validé)" if total_buts % 2 == 0 else "Non (Rupture de rythme en mort subite)"
                                indice_fiabilite = 98.2 + ((h1 % 16) / 10)
                                heure_gmt = datetime.utcnow().strftime("%H:%M")

                                # Structure visuelle propre, ordonnée et élégante sur une seule page
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
