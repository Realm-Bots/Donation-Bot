# bot.py
import os
import logging
from flask import Flask, request
from pyrogram import Client, filters, enums
from pyrogram.types import (
    Update, Message, CallbackQuery, InlineKeyboardMarkup, 
    InlineKeyboardButton, LabeledPrice
)
from pyrogram.errors import MessageNotModified

# --- CONFIG AND BASIC SETUP ---
import config

logging.basicConfig(level=logging.INFO)

# Initialize the Flask app, which is our web server
server = Flask(__name__)

# Initialize the Pyrogram client
# We use in_memory=True because Vercel has an ephemeral filesystem.
app = Client(
    "DonationMenuBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True 
)

# --- WEBHOOK ENTRY POINT ---
# This is the single URL that Telegram will send all updates to.
@server.route(f"/{config.BOT_TOKEN}", methods=["POST"])
async def webhook_handler():
    try:
        # Get the JSON data from Telegram's request
        update_json = request.get_json()
        
        # Pyrogram needs to parse this JSON into its internal Update object
        update = await app.parser.parse(update_json)

        # This is the magic part: Pyrogram's dispatcher will now find the
        # correct handler (@app.on_message, @app.on_callback_query, etc.)
        # and run it, just like it did with long polling.
        await app.process_updates(update, None)

        # Tell Telegram we successfully received the update
        return "OK", 200
    except Exception as e:
        logging.error(f"Error in webhook_handler: {e}")
        return "Error", 500

# ==============================================================================
#  !!! ALL YOUR ORIGINAL BOT LOGIC IS BELOW AND UNCHANGED !!!
# ==============================================================================

# --- Button Generation Functions ---

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

# --- Handlers ---

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        text=config.START_TEXT,
        reply_markup=get_main_menu_keyboard(),
        disable_web_page_preview=True,
        parse_mode=enums.ParseMode.MARKDOWN
    )

@app.on_callback_query()
async def menu_handler(client: Client, callback_query: CallbackQuery):
    """This function is still here and is essential! It handles all button presses."""
    data = callback_query.data
    
    try:
        if data == "main_menu":
            await callback_query.edit_message_text(
                text=config.START_TEXT,
                reply_markup=get_main_menu_keyboard(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        
        elif data == "crypto":
            await callback_query.edit_message_text(
                text=config.CRYPTO_TEXT,
                reply_markup=get_crypto_menu_keyboard(),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.MARKDOWN
            )

        elif data == "stars":
            await callback_query.edit_message_text(
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
                provider_token="",
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
        
        await message.reply_text(
            f"🎉 Thank you so much for your generous donation of **{amount} Stars** ({tier_name} Tier)! "
            "Your support means the world to us. ❤️",
            parse_mode=enums.ParseMode.MARKDOWN
        )

# --- Main Execution (No changes here) ---
async def main():
    await app.start()
    me = await app.get_me()
    logging.info(f"Bot @{me.username} started!")
    await app.idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
