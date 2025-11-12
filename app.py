from flask import Flask, render_template, request, jsonify
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from midascheck import get_pubg_name_from_midas

# إعداد Flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/getname", methods=["POST"])
def get_name():
    player_id = request.json.get("player_id")
    if not player_id:
        return jsonify({"success": False, "error": "Player ID required"})
    result = get_pubg_name_from_midas(player_id)
    return jsonify(result)

# إعداد بوت تيليجرام
BOT_TOKEN = "5775743460:AAEoTi7woOH9F7yqjjj0c29Rmjgr-Ui8NPI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! أرسل Player ID لأعرض لك الاسم الحقيقي من Midasbuy.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_id = update.message.text.strip()
    if not player_id.isdigit():
        await update.message.reply_text("⚠️ أرسل رقم Player ID فقط.")
        return
    result = get_pubg_name_from_midas(player_id)
    if result["success"]:
        await update.message.reply_text(f"✅ الاسم: {result['name']}\n🆔 ID: {result['id']}")
    else:
        await update.message.reply_text(f"⚠️ {result['error']}")

def run_bot():
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_bot.run_polling()

# تشغيل البوت في Thread منفصل
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
