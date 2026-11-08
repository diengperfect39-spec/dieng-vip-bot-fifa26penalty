import os
import time
import hashlib
import requests

TOKEN = "9191245417:AAGcmBNQNwsUJTUcM6G72TfQhtGAMTB9KDo"
URL = f"https://api.telegram.org/bot{TOKEN}"

try:
    requests.get(f"{URL}/deleteWebhook?drop_pending_updates=true", timeout=10)
    print("Ancien webhook nettoyé.")
except Exception as e:
    print("Erreur nettoyage:", e)

print("Dieng VIP Bot actif...")
offset = 0

while True:
    try:
        response = requests.get(f"{URL}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
        if response.status_code == 200:
            data = response.json()
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text_recu = update["message"].get("text", "").strip()
                    
                    if text_recu:
                        if text_recu == "/start":
                            welcome_msg = (
                                "👑 Bienvenue sur Dieng VIP Bot - FIFA 26 / FC Penalty 👑\n\n"
                                "Envoie-moi le nom d'un match (ex: Real vs Barça) ou d'une équipe pour générer l'analyse VIP instantanée !"
                            )
                            requests.post(f"{URL}/sendMessage", json={"chat_id": chat_id, "text": welcome_msg}, timeout=10)
                        elif not text_recu.startswith("/"):
                            parties = [p.strip() for p in text_recu.split("vs")] if "vs" in text_recu else [text_recu, "Visiteur"]
                            eq1 = parties[0]
                            eq2 = parties[1] if len(parties) > 1 else "Visiteur"
                            
                            hash_bytes = hashlib.sha256(text_recu.encode()).digest()
                            v1 = hash_bytes[0]
                            v3 = hash_bytes[2]
                            
                            scenarios = [
                                {"s1": 2, "s2": 3, "gagnant": eq2, "total": "Plus de 4.5 buts", "paire": "Non", "pen": "Moins de 2.5 manqués"},
                                {"s1": 3, "s2": 4, "gagnant": eq2, "total": "Plus de 6.5 buts", "paire": "Non", "pen": "Plus de 2.5 manqués"},
                                {"s1": 4, "s2": 5, "gagnant": eq2, "total": "Plus de 8.5 buts", "paire": "Oui", "pen": "Séance sous haute tension"},
                                {"s1": 4, "s2": 3, "gagnant": eq1, "total": "Plus de 6.5 buts", "paire": "Non", "pen": "Maîtrise des gardiens"},
                                {"s1": 3, "s2": 2, "gagnant": eq1, "total": "Plus de 4.5 buts", "paire": "Non", "pen": "Efficacité redoutable"}
                            ]
                            
                            choix = scenarios[v1 % len(scenarios)]
                            alt_s1 = (choix["s1"] + 1) % 6
                            alt_s2 = (choix["s2"] + 1) % 6
                            if alt_s1 == choix["s1"]: 
                                alt_s1 += 1

                            confiance = 97.8 + (v3 % 19) / 10

                            analysis_text = (
                                f"👑 DIENG PREDICT VIP - ANALYSE EXPERT FIFA 26 👑\n\n"
                                f"⚽ Match : {eq1} vs {eq2}\n"
                                f"📊 Contexte : Analyse Dynamique & Forme des Tirs au But\n\n"
                                f"1. Verdict & Hiérarchie :\n"
                                f"• Vainqueur Validé : {choix['gagnant']}\n"
                                f"• Analyse : Stabilité des frappes et gestion de la pression.\n\n"
                                f"2. Scores Exacts & Marchés Clés :\n"
                                f"• Option 1 (Principal) : {eq1} {choix['s1']} - {choix['s2']} {eq2}\n"
                                f"• Option 2 (Alternatif) : {eq1} {alt_s1} - {alt_s2} {eq2}\n"
                                f"• Volume de buts : {choix['total']}\n\n"
                                f"3. Tendances Marché :\n"
                                f"• Total Pair : {choix['paire']}\n"
                                f"• Pénalties : {choix['pen']}\n\n"
                                f"📈 Indice de Confiance VIP : {confiance:.1f}%"
                            )
                            
                            requests.post(
                                f"{URL}/sendMessage",
                                json={"chat_id": chat_id, "text": analysis_text},
                                timeout=10
                            )
    except Exception as e:
        print("Erreur réseau:", str(e))
        time.sleep(3)
