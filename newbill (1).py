import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime

# ================= CONFIGURATION =================
BOT_TOKEN = "8872257351:AAF86ixX8dPLk0VcDVVxaqhIqzOAO1bInMk"
ADMIN_ID = 7082848228

bot = telebot.TeleBot(BOT_TOKEN)

# ================= IN-MEMORY DATABASE =================
db = {
    "users": {},          
    "bills": {},          
    "exchanges": {},      
    "settings": {
        "binance_id": "1237643552",
        "bep20_address": "0x117c3d27b503be86260545caa6f49f0a2c89223f",
        "usdt_rate": "96.00",
        "support_user": "@ImNova18",
        "maintenance": False
    }
}
bill_counter = 1
exchange_counter = 1

# ================= MAIN MENUS =================
def get_main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("💸 Send Bill"), 
        KeyboardButton("🔮 Exchange")
    )
    markup.add(
        KeyboardButton("📄 Pay History"), 
        KeyboardButton("🎧 Support")
    )
    if user_id == ADMIN_ID:
        markup.add(KeyboardButton("🌀 ADMIN PANNEL"))
    return markup

# ================= COMMANDS =================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in db["users"]:
        username_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        db["users"][user_id] = {
            "username": username_display,
            "joined": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    
    if db["settings"]["maintenance"] and user_id != ADMIN_ID:
        bot.send_message(message.chat.id, "🛠 The bot is currently under maintenance. Please try again later.")
        return

    welcome_text = (
        "👋 Welcome To VaultPay!\n\n"
        "The All-In-One Platform For Bills, Payments & Exchange.\n"
        "✨ Fast • Secure • Reliable\n"
        "Choose an option from the menu below to get started.\n\n"
        "💸 Send Bill — Create & Send Professional Bills.\n"
        "🔮 Exchange — Exchange Your Crypto Funds.\n"
        "📄 Pay History — View Your Transaction History.\n"
        "🎧 Support — Get Help From Support Team.\n\n"
        "Thank You For Choosing VaultPay! 💙"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(user_id))

# ================= MAIN BUTTON HANDLERS =================
@bot.message_handler(func=lambda message: message.text == "💸 Send Bill")
def send_bill_menu(message):
    text = (
        "💸 SEND BILL:\n"
        "Create and send a professional bill in seconds.\n\n"
        "📌 Quick Guide:\n"
        "1️⃣ Enter Your UserName\n"
        "2️⃣ Enter Your Amount\n"
        "3️⃣ Enter Your Qr Number / Account Name\n"
        "4️⃣ Confirm & Send\n\n"
        "✨ Features & Rules:\n"
        "• 🧾 If You Have Done Qr Work Then Enter Qr Number\n"
        "• 📄 Enter Account Name If Done Comment Work\n"
        "• 💳 Gives A Special I'd To Track Payments \n"
        "• 📅 Due Date Support\n"
        "• 📊 Payment Status Tracking\n\n"
        "👇 Select an option below to continue."
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("➕ Create Bill", callback_data="bill_create"))
    markup.add(InlineKeyboardButton("📂 My Bills", callback_data="bill_my"))
    markup.add(InlineKeyboardButton("🔙 Back", callback_data="menu_back"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🔮 Exchange")
def exchange_menu(message):
    text = (
        "🔮 EXCHANGE\n\n"
        "Welcome to VaultPay Exchange.\n"
        "Instantly exchange your crypto funds with a fast and secure process.\n\n"
        "💱 Supported Exchange\n"
        "• USDT → INR ✅️ \n"
        "• BINANCE → UPI ✅️ \n\n"
        "📌 Quick Guide\n"
        "1️⃣ Enter the amount to exchange.\n"
        "2️⃣ Send your payment/wallet details.\n"
        "3️⃣ Wait for admin verification.\n"
        "4️⃣ Receive your exchanged funds.\n\n"
        "⚡ Fast Processing • 🔒 Secure Transactions • 💎 Trusted Service\n\n"
        "👇 Choose an option below to continue."
    )
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("💸 USDT TO INR", callback_data="exch_usdt"))
    markup.add(InlineKeyboardButton("📈 Live Rates", callback_data="exch_rates"))
    markup.add(InlineKeyboardButton("📋 My Orders", callback_data="exch_orders"))
    markup.add(InlineKeyboardButton("🔙 Back", callback_data="menu_back"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📄 Pay History")
def pay_history(message):
    user_id = message.from_user.id
    history = []
    
    for bid, b in db["bills"].items():
        if b["user_id"] == user_id:
            history.append(f"💸 Bill #{bid} | Status: {b['status']}")
            
    for eid, e in db["exchanges"].items():
        if e["user_id"] == user_id:
            history.append(f"🔮 Exch #{eid} | Status: {e['status']}")

    if not history:
        text = (
            "📄 PAY HISTORY\n\n"
            "View your complete transaction history in one place.\n\n"
            "📋 History Includes:\n"
            "• 💸 Bill Payments\n"
            "• 🔮 Exchange Transactions\n"
            "• 💰 Amount\n"
            "• 📅 Date & Time\n"
            "• 📊 Status (Completed / Pending / Rejected)\n\n"
            "No transactions found? Your payment history will appear here after your first successful transaction."
        )
    else:
        text = "📄 PAY HISTORY\n\n" + "\n".join(history)
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda message: message.text == "🎧 Support")
def support_menu(message):
    support = db["settings"]["support_user"]
    text = (
        "🎧 SUPPORT\n\n"
        "Need help? Our support team is here for you.\n"
        f"📩 Contact Support: {support}\n\n"
        "Please include:\n"
        "• 🆔 Order/Bill ID (if applicable)\n"
        "• 📸 Screenshot (if required)\n"
        "• 📝 Brief description of your issue\n\n"
        "⏰ Support Hours: 24/7\n"
        "We aim to respond as quickly as possible. 💙"
    )
    bot.send_message(message.chat.id, text)

# ================= ADMIN PANEL =================
@bot.message_handler(func=lambda message: message.text == "🌀 ADMIN PANNEL" and message.from_user.id == ADMIN_ID)
def admin_panel(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📢 BROADCAST", callback_data="admin_broadcast"),
        InlineKeyboardButton("📸 PENDING PROOFS", callback_data="admin_pending_exch")
    )
    markup.add(
        InlineKeyboardButton("💸 PENDING BILLS", callback_data="admin_pending_bills"),
        InlineKeyboardButton("👥 USERS", callback_data="admin_users")
    )
    markup.add(
        InlineKeyboardButton("📊 STATISTICS", callback_data="admin_stats"),
        InlineKeyboardButton("⚙️ SETTINGS", callback_data="admin_settings")
    )
    bot.send_message(message.chat.id, "🌀 ADMIN PANNEL\nChoose an option below:", reply_markup=markup)

# ================= CALLBACK QUERIES (SUB-BUTTONS) =================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Stops the loading animation on the button!
    bot.answer_callback_query(call.id) 
    
    global bill_counter, exchange_counter
    user_id = call.from_user.id
    
    if call.data == "menu_back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Main Menu:", reply_markup=get_main_menu(user_id))

    # --- BILL CALLBACKS ---
    elif call.data == "bill_create":
        text = (
            "• ➕ Create Bill\n"
            "• 🧾 Let's Create Your bill.\n"
            "• Please Send The Following Details In This Format:\n\n"
            "👤 Your UserName:\n"
            "💰 Amount:\n"
            "📝 Work Name:\n"
            "🪪 Qr I'd / Account Name:\n"
            "📛 Upi I'd / Binance I'd:\n\n"
            "📌 Once submitted, your bill will be generated automatically and assigned a unique Bill I'd 🌀"
        )
        msg = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(msg, process_bill_submission)

    elif call.data == "bill_my":
        paid = sum(1 for b in db["bills"].values() if b["user_id"] == user_id and b["status"] == "APPROVED")
        pend = sum(1 for b in db["bills"].values() if b["user_id"] == user_id and b["status"] == "PENDING")
        canc = sum(1 for b in db["bills"].values() if b["user_id"] == user_id and b["status"] == "REJECTED")
        
        text = (
            "📂 Your Bills Dashboard -\n"
            "Here you can view all your generated bills.\n\n"
            f"🟢 Paid Bills: {paid}\n"
            f"🟡 Pending Bills: {pend}\n"
            f"🔴 Cancelled Bills: {canc}\n\n"
            "Select a bill to view its complete details or track its payment status."
        )
        bot.send_message(call.message.chat.id, text)

    # --- EXCHANGE CALLBACKS ---
    elif call.data == "exch_usdt":
        binance_id = db['settings']['binance_id']
        bep20 = db['settings']['bep20_address']
        text = (
            "💸 USDT → INR EXCHANGE\n\n"
            "To proceed with your exchange, please complete the steps below:\n\n"
            "📤 SEND USDT HERE - \n"
            f"🆔 BINANCE ID: `{binance_id}`\n"
            f"📄 BEP 20 ADDRESS: `{bep20}`\n\n"
            "After sending the USDT, submit the following:\n\n"
            "💰 USDT AMOUNT:\n"
            "🏦 YOUR UPI ID:\n"
            "📸 TRANSACTION SCREENSHOT: (Send this as a photo with the details in caption)\n\n"
            "⚠️ IMPORTANT:\n"
            "• Ensure the screenshot clearly shows the successful transaction.\n"
            "• Incorrect or incomplete details may delay your exchange."
        )
        msg = bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_exchange_submission)

    elif call.data == "exch_rates":
        rate = db["settings"]["usdt_rate"]
        text = (
            "📈 LIVE RATES\n\n"
            "View the latest exchange rates before placing your order.\n\n"
            f"💵 USDT → INR: ₹{rate}\n\n"
            "⏱️ Rates are updated regularly and may change based on market conditions.\n\n"
            "🔄 Tap Refresh to get the latest rate."
        )
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔄 Refresh", callback_data="exch_rates"))
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        except:
            pass # Ignore if rate hasn't changed to prevent API errors

    elif call.data == "exch_orders":
        orders = [f"📦 Order ID: #{eid} | 💰 Amount | 📊 Status: {e['status']}" for eid, e in db["exchanges"].items() if e["user_id"] == user_id]
        if not orders:
            text = "📋 MY ORDERS\n\nView all your exchange requests in one place.\n\nNo orders found."
        else:
            text = "📋 MY ORDERS\n\n" + "\n\n".join(orders)
        bot.send_message(call.message.chat.id, text)

    # --- ADMIN CALLBACKS ---
    elif call.data == "admin_broadcast":
        msg = bot.send_message(call.message.chat.id, "📢 Send the message, photo, video, or document you want to broadcast:")
        bot.register_next_step_handler(msg, process_broadcast)

    elif call.data == "admin_pending_bills":
        pend = len([b for b in db["bills"].values() if b["status"] == "PENDING"])
        app = len([b for b in db["bills"].values() if b["status"] == "APPROVED"])
        rej = len([b for b in db["bills"].values() if b["status"] == "REJECTED"])
        tot = len(db["bills"])
        text = (
            "📄 PENDING BILLS\n\n"
            "Review and manage all submitted bills from one place.\n\n"
            "📊 Dashboard\n"
            f"• 📥 Total Bills: {tot}\n"
            f"• 🟡 Pending Bills: {pend}\n"
            f"• 🟢 Approved Bills: {app}\n"
            f"• 🔴 Rejected Bills: {rej}\n\n"
        )
        bot.send_message(call.message.chat.id, text)
        for bid, b in db["bills"].items():
            if b["status"] == "PENDING":
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("APPROVE ✅️", callback_data=f"b_app_{bid}"),
                    InlineKeyboardButton("REJECT ❌️", callback_data=f"b_rej_{bid}")
                )
                bot.send_message(call.message.chat.id, f"Bill #{bid}\n{b['details']}", reply_markup=markup)

    elif call.data == "admin_pending_exch":
        pend = len([e for e in db["exchanges"].values() if e["status"] == "PENDING"])
        comp = len([e for e in db["exchanges"].values() if e["status"] == "APPROVED"])
        rej = len([e for e in db["exchanges"].values() if e["status"] == "REJECTED"])
        tot = len(db["exchanges"])
        text = (
            "📦 PENDING ORDERS\n\n"
            "Manage all exchange requests from one place.\n\n"
            "📊 Dashboard\n"
            f"• 📥 Total Orders: {tot}\n"
            f"• 🟡 Pending Orders: {pend}\n"
            f"• 🟢 Completed Orders: {comp}\n"
            f"• 🔴 Rejected Orders: {rej}\n\n"
        )
        bot.send_message(call.message.chat.id, text)
        for eid, e in db["exchanges"].items():
            if e["status"] == "PENDING":
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("APPROVE ✅️", callback_data=f"e_app_{eid}"),
                    InlineKeyboardButton("REJECT ❌️", callback_data=f"e_rej_{eid}")
                )
                if e.get("photo_id"):
                    bot.send_photo(call.message.chat.id, e["photo_id"], caption=f"Exchange #{eid}\n{e['details']}", reply_markup=markup)
                else:
                    bot.send_message(call.message.chat.id, f"Exchange #{eid}\n{e['details']}", reply_markup=markup)

    elif call.data == "admin_users":
        text = f"👥 USERS\nTotal active users: {len(db['users'])}"
        bot.send_message(call.message.chat.id, text)

    elif call.data == "admin_stats":
        text = (
            "📊 BOT STATISTICS\n\n"
            "View your bot's overall performance.\n\n"
            "📈 Overview\n"
            f"• 👥 Total Users: {len(db['users'])}\n"
            f"• 💸 Total Bills: {len(db['bills'])}\n"
            f"• 🔮 Total Exchanges: {len(db['exchanges'])}\n"
        )
        bot.send_message(call.message.chat.id, text)

    elif call.data == "admin_settings":
        text = (
            "⚙️ SETTINGS:\n"
            "Manage your bot configuration from one place.\n\n"
            "Available Settings:\n"
            "• 🆔 Update Binance ID - /update_id\n"
            "• 💱 Update USDT → INR Rate - /update_rate\n"
            "• 🏦 Update UPI ID - /update_upi_id\n"
            "• 🎧 Change Support Username - /update_support\n"
            "• 🔧 Maintenance Mode - /maintenance_on & /maintenance_off\n"
        )
        bot.send_message(call.message.chat.id, text)

    # --- ADMIN APPROVAL ACTIONS ---
    elif call.data.startswith("b_app_") or call.data.startswith("b_rej_"):
        action, bid = call.data.split("_")[1], int(call.data.split("_")[2])
        if bid in db["bills"]:
            if action == "app":
                db["bills"][bid]["status"] = "APPROVED"
                text = (
                    "✅ BILL APPROVED\n\n"
                    "YOUR BILL HAS BEEN SUCCESSFULLY APPROVED.\n\n"
                    f"🆔 BILL ID: #{bid:04d}\n"
                    "📅 STATUS: APPROVED\n\n"
                    "THANK YOU FOR USING VAULTPAY."
                )
                bot.edit_message_text(f"Bill #{bid} APPROVED", call.message.chat.id, call.message.message_id)
            else:
                db["bills"][bid]["status"] = "REJECTED"
                support = db["settings"]["support_user"]
                text = (
                    "❌ BILL REJECTED\n\n"
                    "YOUR BILL REQUEST HAS BEEN REJECTED.\n\n"
                    f"🆔 BILL ID: #{bid:04d}\n"
                    f"📌 REASON: ASK FROM ADMIN | {support}\n\n"
                    "PLEASE CORRECT THE DETAILS AND SUBMIT AGAIN."
                )
                bot.edit_message_text(f"Bill #{bid} REJECTED", call.message.chat.id, call.message.message_id)
            bot.send_message(db["bills"][bid]["user_id"], text)

    elif call.data.startswith("e_app_") or call.data.startswith("e_rej_"):
        action, eid = call.data.split("_")[1], int(call.data.split("_")[2])
        if eid in db["exchanges"]:
            if action == "app":
                db["exchanges"][eid]["status"] = "APPROVED"
                text = f"✅ EXCHANGE #{eid:04d} APPROVED successfully."
            else:
                db["exchanges"][eid]["status"] = "REJECTED"
                text = f"❌ EXCHANGE #{eid:04d} REJECTED."
            
            try:
                bot.edit_message_caption(f"Exchange #{eid} {db['exchanges'][eid]['status']}", call.message.chat.id, call.message.message_id)
            except:
                bot.edit_message_text(f"Exchange #{eid} {db['exchanges'][eid]['status']}", call.message.chat.id, call.message.message_id)
                
            bot.send_message(db["exchanges"][eid]["user_id"], text)

# ================= NEXT STEP HANDLERS =================
def process_bill_submission(message):
    global bill_counter
    user_id = message.from_user.id
    bid = bill_counter
    db["bills"][bid] = {
        "user_id": user_id,
        "details": message.text,
        "status": "PENDING"
    }
    bill_counter += 1
    
    bot.send_message(message.chat.id, "✅ Your bill has been submitted and forwarded to the admin.")
    
    # Grab username safely
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("APPROVE ✅️", callback_data=f"b_app_{bid}"),
        InlineKeyboardButton("REJECT ❌️", callback_data=f"b_rej_{bid}")
    )
    admin_text = f"Bill\nUsername: {username}\nPayment id #{bid:04d}\n\nDetails:\n{message.text}"
    bot.send_message(ADMIN_ID, admin_text, reply_markup=markup)

def process_exchange_submission(message):
    global exchange_counter
    user_id = message.from_user.id
    eid = exchange_counter
    
    details = message.caption if message.caption else message.text
    photo_id = message.photo[-1].file_id if message.photo else None
    
    db["exchanges"][eid] = {
        "user_id": user_id,
        "details": details,
        "photo_id": photo_id,
        "status": "PENDING"
    }
    exchange_counter += 1
    
    bot.send_message(message.chat.id, "✅ Your exchange request has been submitted for review.")
    
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("APPROVE ✅️", callback_data=f"e_app_{eid}"),
        InlineKeyboardButton("REJECT ❌️", callback_data=f"e_rej_{eid}")
    )
    
    admin_text = f"Exchange Request #{eid:04d}\nUser: {username}\n\n{details}"
    if photo_id:
        bot.send_photo(ADMIN_ID, photo_id, caption=admin_text, reply_markup=markup)
    else:
        bot.send_message(ADMIN_ID, admin_text, reply_markup=markup)

def process_broadcast(message):
    for u_id in db["users"]:
        try:
            bot.copy_message(chat_id=u_id, from_chat_id=message.chat.id, message_id=message.message_id)
        except Exception:
            pass # User might have blocked the bot
    bot.send_message(message.chat.id, "✅ Broadcast completed successfully.")

# ================= SETTING COMMANDS (ADMIN ONLY) =================
@bot.message_handler(commands=['update_id', 'update_rate', 'update_upi_id', 'update_support', 'maintenance_on', 'maintenance_off'])
def admin_settings_commands(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    if not message.text: # Safety check in case admin sends a photo by mistake
        return
        
    cmd = message.text.split()[0]
    val = message.text.replace(cmd, "").strip()
    
    if cmd == "/update_id" and val:
        db["settings"]["binance_id"] = val
        bot.send_message(message.chat.id, "✅ Binance ID updated.")
    elif cmd == "/update_rate" and val:
        db["settings"]["usdt_rate"] = val
        bot.send_message(message.chat.id, "✅ USDT Rate updated.")
    elif cmd == "/update_support" and val:
        db["settings"]["support_user"] = val
        bot.send_message(message.chat.id, "✅ Support username updated.")
    elif cmd == "/maintenance_on":
        db["settings"]["maintenance"] = True
        bot.send_message(message.chat.id, "✅ Maintenance mode turned ON.")
    elif cmd == "/maintenance_off":
        db["settings"]["maintenance"] = False
        bot.send_message(message.chat.id, "✅ Maintenance mode turned OFF.")
    else:
        bot.send_message(message.chat.id, "⚠️ Invalid format. Use: /command value")

# ================= START POLLING =================
print("VaultPay Bot is running...")
bot.infinity_polling()
