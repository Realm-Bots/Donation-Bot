# # Made By @NaapaExtraa For @Realm_Bots
import os
from dotenv import load_dotenv

load_dotenv()

# Add these values on .env file
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID", 0))

# --- PICTURES ---
START_PIC_URL = "https://graph.org/file/34891a7555dcdbf29068e-402ea87b8c7fdc8f23.jpg"
PROFILE_PIC_URL = "https://graph.org/file/37486760ded5cd4097437-51cf00c61fe05cec37.jpg"
OWNER_ID = 7099729191 

START_TEXT = """
**Yᴏᴜ ᴄᴀɴ sᴜᴘᴘᴏʀᴛ @TeamMayhem ʙʏ ᴅᴏɴᴀᴛɪɴɢ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ʟɪɴᴋ ʙᴇʟᴏᴡ.
Dᴏɴᴀᴛɪᴏɴs ᴡɪʟʟ ʙᴇ ᴜsᴇᴅ ғᴏʀ ᴏᴜʀ ʙᴏᴛs sᴇʀᴠᴇʀ ʀᴇɴᴛᴀʟ ᴄᴏsᴛs.

Tʜᴀɴᴋs ғᴏʀ ʏᴏᴜʀ ɪɴᴛᴇʀᴇsᴛ ɪɴ ᴅᴏɴᴀᴛɪᴏɴ 🙏**
"""

CRYPTO_TEXT = f"""
**Mᴀɪɴ Cʀʏᴘᴛᴏ Aᴅᴅʀᴇss:**

**BTC:** `135G6kyKpfwZbHXUYu4gsJaoJPBnrDDSbQ`

**TON:** `UQCwKMw3WvaEvZ9SIsmc4Mxuz4Yu_-5SsFb2JUEH70Lz0ssx`

**OPBNB:** `0x456945634e4d9d9b9a6069f72a869963281aa40e`

**ɪғ ʏᴏᴜ ɴᴇᴇᴅ ᴀɴᴏᴛʜᴇʀ ᴄʀʏᴘᴛᴏ ᴀᴅᴅʀᴇss, ᴘʟᴇᴀsᴇ [ᴄᴏɴᴛᴀᴄᴛ ᴍʏ ᴍᴀsᴛᴇʀ ʜᴇʀᴇ](tg://user?id={OWNER_ID}).**
"""

STARS_TEXT = "**ʜᴏᴡ ᴍᴀɴʏ sᴛᴀʀs ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏɴᴀᴛᴇ?**"

STARS_CUSTOM_TEXT = """
**ᴏᴋᴀʏ, ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴄᴜsᴛᴏᴍ ᴀᴍᴏᴜɴᴛ ᴏғ sᴛᴀʀs ʏᴏᴜ ᴡɪsʜ ᴛᴏ ᴅᴏɴᴀᴛᴇ ɴᴏᴡ.**
"""

# --- BUTTONS ---
MAIN_MENU_BUTTONS = {
    "ᴄʀʏᴘᴛᴏ": "callback:crypto",
    "ᴛᴇʟᴇɢʀᴀᴍ sᴛᴀʀs": "callback:stars"
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
