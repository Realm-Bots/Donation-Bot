# bot.py
import logging
from pyrogram import Client, filters, enums, idle
from pyrogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice
)
from pyrogram.errors import MessageNotModified

import config
import database as db

# --- Basic Bot Setup ---
logging.basicConfig(level=logging.INFO)
app = Client(
    "DonationMenuBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# --- Button Generation Functions (No Change) ---
# ... (copy the 3 get_*_keyboard functions from the previous version) ...
def get_main_menu_keyboard():
    buttons = []
    for text, data in config.MAIN_MENU_BUTTONS.items():
        if data.startswith("url:"):
            buttons.append(InlineKeyboardButton(text, url=data.split(":", 1)[1]))
        elif data.startswith("callback:"):
            buttons.append(InlineKeyboardButton(text, callback_data=data.split(":", 1)[1]))
    return InlineKeyboardMarkup([buttons[i:i+2] for i in range(0, len(buttons), 2)])

def get_crypto_menu_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="main_menu")]])

def get_stars_menu_keyboard():
    buttons = []
    for amount, tier in config.STARS_TIERS.items():
        label = f"{amount} {tier}"
        callback_data = f"stars:{amount}"
        buttons.append(InlineKeyboardButton(label, callback_data=callback_data))
    keyboard_layout = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    keyboard_layout.append([InlineKeyboardButton("« Back", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard_layout)

# --- Command & Message Handlers ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    # Now sends a photo with a caption
    await message.reply_photo(
        photo=config.START_PIC_URL,
        caption=config.START_TEXT,
        reply_markup=get_main_menu_keyboard(),
        parse_mode=enums.ParseMode.MARKDOWN
    )

@app.on_message(filters.command("profile") & filters.private)
async def profile_handler(client: Client, message: Message):
    user_id = message.from_user.id
    stats = db.get_user_stats(user_id)

    if not stats:
        await message.reply_text("You haven't made any donations yet. Use /start to see how!")
        return

    profile_text = (
        "👤 **Your Donation Profile**\n\n"
        f"**User ID:** `{stats['user_id']}`\n"
        f"**Total Donation:** `⭐ {stats['total_donated']}` Stars\n"
        f"**Last Donated Tier:** `{stats['last_tier_donated']}`"
    )
    
    await message.reply_photo(
        photo=config.PROFILE_PIC_URL,
        caption=profile_text,
        parse_mode=enums.ParseMode.MARKDOWN
    )

@app.on_message(filters.command("leaderboard") & filters.private)
async def leaderboard_handler(client: Client, message: Message):
    top_donors = db.get_leaderboard()

    if not top_donors:
        await message.reply_text("The leaderboard is empty. Be the first to donate!")
        return

    leaderboard_text = "🏆 **Top 10 Donators** 🏆\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for i, donor in enumerate(top_donors):
        # Use medals for top 3, numbers for the rest
        place = medals[i] if i < 3 else f"**{i + 1}.**"
        
        # Create a mention link for the user
        user_mention = f"[{donor['first_name']}](tg://user?id={donor['user_id']})"
        
        leaderboard_text += f"{place} {user_mention} - `⭐ {donor['total_donated']}` Stars\n"
        
    await message.reply_text(leaderboard_text, parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True)


@app.on_callback_query()
async def menu_handler(client: Client, callback_query: CallbackQuery):
    # ... (This function remains exactly the same as the last version) ...
    data = callback_query.data
    
    try:
        if data == "main_menu":
            await callback_query.message.edit_caption(
                caption=config.START_TEXT,
                reply_markup=get_main_menu_keyboard(),
                parse_mode=enums.ParseMode.MARKDOWN
            )
        elif data == "crypto":
            # Can't edit a photo caption to text, so we edit the whole message
            await callback_query.message.edit_text(
                text=config.CRYPTO_TEXT,
                reply_markup=get_crypto_menu_keyboard(),
                parse_mode=enums.ParseMode.MARKDOWN
            )
        elif data == "stars":
            await callback_query.message.edit_text(
                text=config.STARS_TEXT,
                reply_markup=get_stars_menu_keyboard(),
                parse_mode=enums.ParseMode.MARKDOWN
            )
        elif data.startswith("stars:"):
            amount = int(data.split(":")[1])
            tier_name = config.STARS_TIERS.get(str(amount), "Donation")
            await client.send_invoice(
                chat_id=callback_query.from_user.id,
                title=f"{tier_name} Tier Donation",
                description=f"Thank you for donating {amount} Stars to support us!",
                payload=f"stars-donation-{callback_query.from_user.id}-{amount}",
                currency="XTR",
                prices=[LabeledPrice(f"{amount} Telegram Stars", amount)]
            )
            await callback_query.answer(f"Preparing {amount} Stars invoice...", show_alert=False)
    except MessageNotModified:
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Error in menu_handler: {e}")
        await callback_query.answer("An error occurred.", show_alert=True)


@app.on_message(filters.successful_payment)
async def successful_payment_handler(client: Client, message: Message):
    if message.successful_payment.currency == "XTR":
        amount = message.successful_payment.total_amount
        tier_name = config.STARS_TIERS.get(str(amount), "Donation")
        
        # --- DATABASE INTEGRATION ---
        db.record_donation(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            amount=amount,
            tier=tier_name
        )
        # ---------------------------

        await message.reply_text(
            f"🎉 Thank you for your donation of **{amount} Stars** ({tier_name} Tier)!\n\n"
            "Your contribution has been recorded. You can check your stats with /profile.",
            parse_mode=enums.ParseMode.MARKDOWN
        )

# --- Main Execution ---
async def main():
    await app.start()
    me = await app.get_me()
    logging.info(f"Bot @{me.username} started successfully!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
