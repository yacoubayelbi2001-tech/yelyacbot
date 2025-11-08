import os
import telebot
from threading import Thread
from flask import Flask

# ========================
# 💬 MESSAGES DU BOT
# ========================
WELCOME_MSG = (
    "👋 Bienvenue sur *YelyacBot* !\n\n"
    "Je suis ton assistant automatique Telegram. "
    "Utilise /help pour découvrir ce que je peux faire pour toi."
)

HELP_MSG = (
    "📋 *Commandes disponibles :*\n"
    "/start - Accueil\n"
    "/help - Liste des commandes\n"
    "/about - À propos du bot\n"
    "/contact - Contacter l’administrateur\n"
    "/services - Voir les services disponibles"
)

ABOUT_MSG = (
    "🤖 *YelyacBot* est un bot développé pour automatiser certaines tâches et "
    "faciliter la communication. Il est géré par Yacoub (@YEL_Yac)."
)

CONTACT_MSG = (
    "📩 *Contact administrateur :*\n"
    "👉 [@YEL_Yac](https://t.me/YEL_Yac)\n\n"
    "Envoie-moi un message directement sur Telegram."
)

SERVICES_MSG = (
    "🛠️ *Services proposés :*\n"
    "1️⃣ Support et assistance\n"
    "2️⃣ Infos et actualités\n"
    "3️⃣ Réponses automatiques personnalisées"
)

# ========================
# ⚙️ COMMANDES DU BOT
# ========================
def setup_bot():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("❌ BOT_TOKEN manquant — configure-le dans Render (Environment Variables)")

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def start_handler(message):
        bot.reply_to(message, WELCOME_MSG, parse_mode='Markdown')

    @bot.message_handler(commands=['help'])
    def help_handler(message):
        bot.reply_to(message, HELP_MSG, parse_mode='Markdown')

    @bot.message_handler(commands=['about'])
    def about_handler(message):
        bot.reply_to(message, ABOUT_MSG, parse_mode='Markdown')

    @bot.message_handler(commands=['contact'])
    def contact_handler(message):
        bot.reply_to(message, CONTACT_MSG, parse_mode='Markdown')

    @bot.message_handler(commands=['services'])
    def services_handler(message):
        bot.reply_to(message, SERVICES_MSG, parse_mode='Markdown')

    @bot.message_handler(func=lambda m: True)
    def fallback_handler(message):
        bot.reply_to(message, "Je n’ai pas compris 🤔\nEssaie /help pour voir les commandes disponibles.")

    return bot

bot = setup_bot()

# ========================
# FLASK POUR RENDRE LE SERVICE COMPATIBLE
# ========================
app = Flask(name)

@app.route("/")
def health():
    return "YelyacBot OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ========================
# LANCEMENT DU BOT ET DU FLASK
# ========================
if name == "main":
    # Démarrer Flask dans un thread pour détecter le port par Render
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    print("✅ YelyacBot est en ligne et prêt à répondre !")
    bot.infinity_polling(timeout=60, long_polling_timeout=60)




