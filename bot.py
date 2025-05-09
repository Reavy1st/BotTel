from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import os

saved_links = {}
OWNER_FILE = "owners.txt"

# === FUNGSI OWNER ===

def load_owners():
    if not os.path.exists(OWNER_FILE):
        return set()
    with open(OWNER_FILE, 'r') as f:
        return set(int(line.strip()) for line in f if line.strip().isdigit())

def save_owner(user_id):
    with open(OWNER_FILE, 'a') as f:
        f.write(f"{user_id}\n")

owners = load_owners()

def is_owner(user_id):
    return user_id in owners

def add_owner(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not is_owner(user_id):
        update.message.reply_text("Kamu bukan owner. Akses ditolak.")
        return
    if len(context.args) < 1:
        update.message.reply_text("Gunakan format: /addown <user_id>")
        return
    try:
        new_id = int(context.args[0])
        if new_id in owners:
            update.message.reply_text("User sudah jadi owner.")
        else:
            owners.add(new_id)
            save_owner(new_id)
            update.message.reply_text(f"Berhasil menambahkan {new_id} sebagai owner.")
    except ValueError:
        update.message.reply_text("ID harus berupa angka.")

# === PERINTAH BOT ===

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hai {user.first_name}! ID Telegram kamu: {user.id}")

def keluar(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        update.message.reply_text("Akses ditolak.")
        return
    chat = update.effective_chat
    if chat.type in ['group', 'supergroup']:
        update.message.reply_text("Saya akan keluar dari grup.")
        context.bot.leave_chat(chat.id)

def setlink(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        update.message.reply_text("Akses ditolak.")
        return
    if len(context.args) < 1:
        update.message.reply_text("Gunakan format: /setlink <link>")
        return
    link = context.args[0]
    saved_links[update.effective_chat.id] = link
    update.message.reply_text(f"Link disimpan: {link}")

def share(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        update.message.reply_text("Akses ditolak.")
        return
    chat_id = update.effective_chat.id
    if chat_id not in saved_links:
        update.message.reply_text("Tidak ada link tersimpan.")
        return
    try:
        jumlah = int(context.args[0])
        link = saved_links[chat_id]
        for _ in range(min(jumlah, 20)):
            update.message.reply_text(link)
    except:
        update.message.reply_text("Gunakan: /share <jumlah>")

def allmenu(update: Update, context: CallbackContext):
    if not is_owner(update.effective_user.id):
        update.message.reply_text("Akses ditolak.")
        return
    menu = (
        "Menu:\n"
        "/addown <user_id> - Tambah owner\n"
        "/keluar - Bot keluar grup\n"
        "/setlink <link> - Simpan link\n"
        "/share <jumlah> - Bagikan link\n"
    )
    buttons = [
        [InlineKeyboardButton("Owner", callback_data='owner'),
         InlineKeyboardButton("Payment", callback_data='payment')]
    ]
    update.message.reply_text(menu, reply_markup=InlineKeyboardMarkup(buttons))

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'owner':
        query.edit_message_text("Hubungi Owner:\n@YourTelegramUsername")  # Ganti dengan username kamu
    elif query.data == 'payment':
        qris_file_id = "PASTE_FILE_ID_QRIS"  # Ganti dengan file_id QRIS kamu
        context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=qris_file_id,
            caption="Dana: 083870202221"
        )

# === MAIN ===

def main():
    TOKEN = "7803580421:AAGYLYTv3mYaWBwf9U0zjfTWpubg2QzehSg"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addown", add_owner))
    dp.add_handler(CommandHandler("keluar", keluar))
    dp.add_handler(CommandHandler("setlink", setlink))
    dp.add_handler(CommandHandler("share", share))
    dp.add_handler(CommandHandler("allmenu", allmenu))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
