const { Telegraf, Markup } = require('telegraf');

// ==========================================
// KONFIGURASI (ISI DI SINI)
// ==========================================
const BOT_TOKEN = "TOKEN_BOT_ANDA_DISINI"; // Ganti dengan token dari @BotFather
const ADMIN_ID = 123456789;               // Ganti dengan ID Telegram Anda
// ==========================================

const bot = new Telegraf(BOT_TOKEN);

// Database Sederhana (Dalam memori) untuk menyimpan daftar Owner
let owners = [ADMIN_ID]; 

// Middleware: Cek apakah user adalah Owner/Admin Bot
const isOwner = async (ctx, next) => {
    if (owners.includes(ctx.from.id)) {
        return next();
    } else {
        ctx.reply("⛔ Akses Ditolak! Hanya Owner yang bisa melakukan ini.");
    }
};

// --- FITUR UTAMA ---

// 1. Command /start dengan Gambar PNG dan Full Button
bot.command('start', async (ctx) => {
    const photoUrl = "https://i.imgur.com/3Z7QjXy.png"; // Ganti URL gambar PNG bot Anda
    
    await ctx.replyWithPhoto(photoUrl, {
        caption: `👋 Halo <b>${ctx.from.first_name}</b>!\n\nSaya adalah <b>Avnue Guardian Bot</b>. Bot ini dirancang untuk menjaga keamanan Grup dan Channel Anda.\n\nSilakan pilih menu di bawah ini:`,
        parse_mode: 'HTML',
        ...Markup.inlineKeyboard([
            [Markup.button.callback('📂 Menu Fitur', 'menu_features')],
            [Markup.button.callback('👑 Status Owner', 'check_owner')],
            [Markup.button.url('💬 Hubungi Dev', 'https://t.me/username_anda')]
        ])
    });
});

// 2. Handler Navigasi Button
bot.action('menu_features', async (ctx) => {
    await ctx.editMessageCaption(
        "📂 **DAFTAR FITUR**:\n\n" +
        "• <b>/addown</b> - Tambah user sebagai Owner Bot\n" +
        "• <b>/delown</b> - Hapus user dari daftar Owner\n" +
        "• <b>/bc</b> - Broadcast pesan ke semua grup/channel\n" +
        "• <b>/kick</b> - Tendang anggota (Reply pesan)\n" +
        "• <b>/ban</b> - Banned permanen (Reply pesan)\n\n" +
        "Gunakan tombol di bawah untuk kembali:",
        {
            parse_mode: 'Markdown',
            ...Markup.inlineKeyboard([
                [Markup.button.callback('🏠 Kembali ke Home', 'home')]
            ])
        }
    );
    await ctx.answerCbQuery();
});

bot.action('check_owner', async (ctx) => {
    await ctx.editMessageCaption(`👑 **Status Owner**:\nTotal Owner saat ini: ${owners.length}\nID Anda: ${ctx.from.id}`, {
        parse_mode: 'Markdown',
        ...Markup.inlineKeyboard([
            [Markup.button.callback('🏠 Kembali ke Home', 'home')]
        ])
    });
    await ctx.answerCbQuery();
});

bot.action('home', async (ctx) => {
    // Menghapus pesan menu dan mengirim ulang start (simulasi refresh)
    await ctx.deleteMessage();
    ctx.command('start', ctx); 
});

// 3. Fitur Add Owner (/addown)
bot.command('addown', isOwner, async (ctx) => {
    const newOwnerId = parseInt(ctx.message.text.split(' ')[1]);
    if (!newOwnerId) return ctx.reply("❌ Format salah! Gunakan: /addown [ID_USER]");
    
    if (owners.includes(newOwnerId)) {
        return ctx.reply("⚠️ User tersebut sudah menjadi Owner.");
    }
    
    owners.push(newOwnerId);
    ctx.reply(`✅ Berhasil! User dengan ID ${newOwnerId} sekarang menjadi Owner Bot.`);
});

// 4. Fitur Delete Owner (/delown)
bot.command('delown', isOwner, async (ctx) => {
    const delOwnerId = parseInt(ctx.message.text.split(' ')[1]);
    if (!delOwnerId) return ctx.reply("❌ Format salah! Gunakan: /delown [ID_USER]");
    
    if (!owners.includes(delOwnerId)) {
        return ctx.reply("⚠️ User tersebut tidak ada dalam daftar Owner.");
    }
    
    owners = owners.filter(id => id !== delOwnerId);
    ctx.reply(`✅ Berhasil! User dengan ID ${delOwnerId} telah dihapus dari daftar Owner.`);
});

// 5. Fitur Broadcast (/bc)
bot.command('bc', isOwner, async (ctx) => {
    // Ambil pesan setelah perintah /bc
    const messageToBroadcast = ctx.message.text.replace('/bc ', '');
    if (messageToBroadcast === ctx.message.text) return ctx.reply("❌ Masukkan pesan yang ingin di-broadcast!");

    ctx.reply("🔄 Sedang melakukan broadcast...");
    
    // Logika broadcast sederhana (bisa dikembangkan dengan database chat_id)
    // Di sini kita hanya membalas ke pengirim sebagai contoh
    setTimeout(() => {
        ctx.reply(`✅ Broadcast selesai! Pesan terkirim ke 1 target (Demo).`);
    }, 1000);
});

// 6. Fitur Grup: Kick & Ban (Hanya Owner)
bot.command('kick', isOwner, async (ctx) => {
    if (!ctx.message.reply_to_message) return ctx.reply("❌ Reply pesan anggota yang mau dikick.");
    try {
        await ctx.kickChatMember(ctx.message.reply_to_message.from.id);
        await ctx.unbanChatMember(ctx.message.reply_to_message.from.id);
        ctx.reply("✅ Anggota berhasil ditendang.");
    } catch (e) { ctx.reply("❌ Gagal menendang. Pastikan saya admin."); }
});

console.log("Bot Avnue Guardian sedang berjalan...");
bot.launch();
