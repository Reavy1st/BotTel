from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Simpan link secara global untuk sementara (bisa diubah jadi penyimpanan file/db)
saved_links = {}

# /keluar - bot keluar dari grup
def keluar(update: Update, context: CallbackContext):
    chat = update.effective_chat
    if chat.type in ['group', 'supergroup']:
        update.message.reply_text("Saya akan keluar dari grup. Sampai jumpa!")
        context.bot.leave_chat(chat.id)
    else:
        update.message.reply_text("Perintah ini hanya bisa digunakan di dalam grup.")

# /setlink <link> - simpan link
def setlink(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        update.message.reply_text("Gunakan format: /setlink <link>")
        return
    link = context.args[0]
    saved_links[update.effective_chat.id] = link
    update.message.reply_text(f"Link berhasil disimpan: {link}")

# /share <jumlah> - share link yang sudah disimpan
def share(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id not in saved_links:
        update.message.reply_text("Belum ada link yang disimpan. Gunakan /setlink terlebih dahulu.")
        return

    try:
        jumlah = int(context.args[0])
        link = saved_links[chat_id]
        for _ in range(min(jumlah, 20)):  # batas maksimal agar tidak spam berlebihan
            update.message.reply_text(link)
    except (IndexError, ValueError):
        update.message.reply_text("Gunakan format: /share <jumlah> (angka)")

def main():
    TOKEN = "7576232943:AAHKeMOlxkXTfmc7chIWJwMUIXhmsGoYeB8"  # Ganti dengan token bot-mu
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("keluar", keluar))
    dp.add_handler(CommandHandler("setlink", setlink))
    dp.add_handler(CommandHandler("share", share))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
