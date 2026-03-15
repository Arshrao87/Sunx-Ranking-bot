from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from collections import defaultdict

points = defaultdict(int)
daily = defaultdict(int)

SPECIAL_WORD = "MonkeyKingForPeace"
DAILY_LIMIT = 25

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user = update.message.from_user.id
    text = update.message.text.lower()

    if daily[user] >= DAILY_LIMIT:
        return

    if len(text) >= 12:
        points[user] += 1
        daily[user] += 1

    if SPECIAL_WORD in text:
        points[user] += 5

async def show_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    p = points.get(user, 0)
    await update.message.reply_text(f"⭐ Your points: {p}")

async def show_rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ranking = sorted(points.items(), key=lambda x: x[1], reverse=True)
    text = "🏆 Group Ranking\n\n"
    for i,(u,p) in enumerate(ranking[:10]):
        text += f"{i+1}. {p} points\n"
    await update.message.reply_text(text)

app = ApplicationBuilder().token("8497986868:AAE_QQDhW_oCHEXKsNS3YAuhCmSvkHj9k-s").build()

app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^p$"), show_points))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^r$"), show_rank))
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()
