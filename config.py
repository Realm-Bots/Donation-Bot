# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- REQUIRED ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI") # <-- NEW
# ----------------

# --- PICTURES ---
# Replace these with direct links to your images
START_PIC_URL = "https://graph.org/file/ab1c4882db6a02add069e-2d59575f154d39acda.jpg"
PROFILE_PIC_URL = "https://graph.org/file/ab1c4882db6a02add069e-2d59575f154d39acda.jpg"

# --- TEXTS ---
OWNER_ID = 123456789 

START_TEXT = """
**Yᴏᴜ ᴄᴀɴ sᴜᴘᴘᴏʀᴛ @TeamMayhem ʙʏ ᴅᴏɴᴀᴛɪɴɢ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ʟɪɴᴋ ʙᴇʟᴏᴡ.
Dᴏɴᴀᴛɪᴏɴs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴏᴜʀ ʙᴏᴛs sᴇʀᴠᴇʀ ʀᴇɴᴛᴀʟ ᴄᴏsᴛs.

Tʜᴀɴᴋs ғᴏʀ ʏᴏᴜʀ ɪɴᴛᴇʀᴇsᴛ ɪɴ ᴅᴏɴᴀᴛɪᴏɴ 🙏**
"""

CRYPTO_TEXT = f"""
**Mᴀɪɴ Cʀʏᴘᴛᴏ Aᴅᴅʀᴇss:**

**BTC:** `1DxGWYXeSMqqpouJeHEqHsLuxGv1ydkCoe`

If you need another crypto address, please [contact my master here](tg://user?id={OWNER_ID}).
"""

STARS_TEXT = "**How many stars do you want to donate?**"

# --- BUTTONS ---
MAIN_MENU_BUTTONS = {
    "Crypto": "callback:crypto",
    "Dana": "url:https://link.dana.id/qr/yourcode",
    "Trakteer": "url:https://trakteer.id/yourusername",
    "Telegram Stars": "callback:stars",
    "Github Sponsors": "url:https://github.com/sponsors/yourusername",
    "Paypal": "url:https://paypal.me/yourusername"
}

STARS_TIERS = {
    "5": " sᴛᴀʀᴛᴇʀ",
    "10": " ᴡᴀʀʀɪᴏʀ",
    "25": " ɢᴜᴀʀᴅɪᴀɴ",
    "50": " ᴄʜᴀᴍᴘɪᴏɴ",
    "100": " ᴍʏᴛʜɪᴄ",
    "200": " ʟᴇɢᴇɴᴅ",
    "500": " ᴇᴛᴇʀɴᴀʟ",
    "1000": " sᴜᴘʀᴇᴍᴇ"
}
