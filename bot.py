import os
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def health():
    return 'OK', 200

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    print(f"✅ Dummy health server running on port {port}")
    app.run(host="0.0.0.0", port=port, threaded=True)

threading.Thread(target=run_health_server, daemon=True).start()




















# ChannelAutoPost – Modified for 10→10 Mirroring
# Based on ChannelAutoForwarder by @xditya
# Edited for 1-to-1 channel mirroring (fresh repost, not forward)

import logging
from telethon import TelegramClient, events, Button
from decouple import config

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("ChannelAutoPost")

log.info("Starting Channel AutoPost Bot (1→1 mirror mode)...")

# Telegram credentials from .env
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    datgbot = TelegramClient(None, apiid, apihash).start(bot_token=bottoken)
except Exception as exc:
    log.error("Environment vars missing or invalid!")
    log.error(exc)
    exit()

# -------------- YOUR 10→10 CHANNEL MAPPING HERE -----------------
# Example format:

CHANNEL_PAIRS = {
   -1003364376763: [
  -1003453679424, -1003334898579, -1003351226347, -1003434479602,
  -1003328308380, -1003439841363, -1003300638715, -1003353186794,
  -1003374169118, -1003457996231, -1003346011549, -1003437220895,
  -1003324948076, -1003266809378, -1003424178806, -1003435606064,
  -1003350491064, -1003361430706, -1003427469066, -1003459020274,
  -1003430464723, -1003368772028, -1003328485559, -1003484445612
],

-1003487998728: [
  -1003355151992, -1003308982488, -1003453541940, -1003354644536,
  -1003301158330, -1003349625776, -1003369364886, -1003313358455,
  -1003355536259, -1003324729382, -1003454198586, -1003335615999,
  -1003351848413, -1003343506885, -1003322011683, -1003360588721,
  -1003316432176, -1003423797032, -1003466875310, -1003341988364,
  -1003456612805, -1003376086582, -1003343407482, -1003436481424
],

-1003317220869: [
  -1003358338692, -1003401278858, -1003430464723, -1003482826184,
  -1003339923249, -1003299212150, -1003399823211, -1003371413619,
  -1003342448765, -1003308754101, -1003487866378, -1003078238190,
  -1003430843781, -1003310821492, -1003394872511, -1003372644321,
  -1003474648368, -1003265834770, -1003484185585, -1003212259737,
  -1003278769356, -1003185818161, -1003371010914, -1003157649448
],

-1003145685265: [
  -1003233716968, -1003469576052, -1003315615765, -1003282806902,
  -1003397402306, -1003481645221, -1003491181731, -1003484087480,
  -1003434479602, -1003390204209, -1003169400827, -1003436481424,
  -1003400746946, -1003343407482, -1003482546392, -1003426358391,
  -1003455706976, -1003400302528, -1003426305435, -1003407123071,
  -1003310768311, -1003355906179, -1003347305145, -1003377086997
],

-1003459842269: [
  -1003313834444, -1003427580244, -1003459735210, -1003308751998,
  -1003207673095, -1003377502073, -1003299618454, -1003217978013,
  -1003323011665, -1003210487720, -1003372616261, -1003399375638,
  -1003360588721, -1003428202296, -1003155551488, -1003352113611,
  -1003431875885, -1003474604403, -1003300638715, -1002962828171,
  -1003115443109, -1003324948076, -1003365862487, -1003416701554
],

-1003409103927: [
  -1003380483459, -1003401863315, -1003376406368, -1003262345441,
  -1003341630956, -1003442088709, -1003313358455, -1003401580494,
  -1003235773477, -1003450127862, -1003321578822, -1003220168548,
  -1003349342033, -1003117667346, -1003328308380, -1003302279496,
  -1003335875267, -1003403697201, -1003283523604, -1003334898579,
  -1003498155377, -1003361430706, -1003425630503, -1003311605515
],

-1003261462457: [
  -1003387921588, -1003487541147, -1003367824722, -1003358121199,
  -1003145104728, -1003389769263, -1003316826201, -1003456802218,
  -1003332113549, -1003389344657, -1003228857091, -1003399541528,
  -1003315512177, -1003424178806, -1003494101377, -1003483654506,
  -1003308982488, -1003461892070, -1003456689782, -1003301158330,
  -1003453679424, -1003355068356, -1003492324322, -1003205187661
],

-1003267373774: [
  -1003302547517, -1003435606064, -1003321235566, -1003285358916,
  -1003376086582, -1003453541940, -1003457780763, -1002775630112,
  -1003457996231, -1003464221787, -1003241121346, -1003350491064,
  -1003430751683, -1003374169118, -1003342629658, -1003499982508,
  -1003320863543, -1003313948618, -1003261199623, -1003313271747,
  -1003440972731, -1003418333366, -1003368772028, -1003341988364
],

-1002743149633: [
  -1002989120450, -1003198193915, -1003369364886, -1003323759597,
  -1003382592112, -1003358338692, -1003401278858, -1003430464723,
  -1003482826184, -1003339923249, -1003299212150, -1003399823211,
  -1003371413619, -1003342448765, -1003308754101, -1003487866378,
  -1003078238190, -1003430843781, -1003310821492, -1003394872511,
  -1003372644321, -1003474648368, -1003265834770, -1003484185585
],
    
    -1002913365577: [-1003416415176],

-1003428124148: [
  -1003212259737, -1003278769356, -1003185818161, -1003371010914,
  -1003157649448, -1003233716968, -1003469576052, -1003315615765,
  -1003282806902, -1003397402306, -1003481645221, -1003491181731,
  -1003484087480, -1003434479602, -1003390204209, -1003169400827,
  -1003436481424, -1003400746946, -1003343407482, -1003482546392,
  -1003426358391, -1003455706976, -1003400302528, -1003426305435
]
    

    
    
    
}
# ---------------------------------------------------------------

# /start command
@datgbot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`!\n\n"
        f"I’m a channel auto-post bot running in 1→1 mirror mode.\n"
        f"Messages from 10 source channels will be sent freshly to 10 targets.\n\n"
        f"Use /help for more info.",
        buttons=[
            Button.url("Repo", url="https://github.com/xditya/ChannelAutoForwarder"),
            Button.url("Developer", url="https://xditya.me"),
        ],
        link_preview=False,
    )

# /help command
@datgbot.on(events.NewMessage(pattern="/help"))
async def help_cmd(event):
    await event.reply(
        "**Help — 1→1 Channel Mirroring Bot**\n\n"
        "This bot listens to multiple source channels and sends their posts freshly to corresponding target channels.\n\n"
        "Example mapping:\n"
        "`src1 → dest1`, `src2 → dest2`, etc.\n\n"
        "No 'forwarded from' tag — posts look original.\n\n"
        "Make sure the bot is an **admin in both source and target channels.**"
    )




import asyncio
import random




@datgbot.on(events.NewMessage(incoming=True, chats=list(CHANNEL_PAIRS.keys())))
async def mirror_message(event):
    # Skip messages sent by the bot itself
    if event.out or event.message.out:
        return

    src = event.chat_id
    dests = CHANNEL_PAIRS.get(src)
    if not dests:
        return

    # Normalize targets: accept string, single ID, or list
    if isinstance(dests, str):
        dests = [int(x) for x in dests.split()]
    elif isinstance(dests, int):
        dests = [dests]

    for dest in dests:
        try:
            if event.poll:
                log.info(f"Skipping poll message in {src}")
                continue

            # Handle different message types
            if event.photo:
                await datgbot.send_file(dest, event.media.photo, caption=event.text or "", link_preview=False)
            elif event.media:
                await datgbot.send_file(dest, event.media, caption=event.text or "")
            elif event.text:
                await datgbot.send_message(
                    dest,
                    event.text,
                    formatting_entities=event.message.entities
                )
            else:
                log.info(f"Unhandled message type from {src}")

            log.info(f"✅ Mirrored message from {src} → {dest}")

            # Random delay between 5–10 seconds + jitter (±0.5s)
            delay = random.uniform(5, 10) + random.uniform(-0.5, 0.5)
            delay = max(0, delay)
            log.info(f"⏳ Waiting {delay:.2f}s before next send...")
            await asyncio.sleep(delay)

        except Exception as e:
            log.error(f"❌ Failed to mirror message from {src} → {dest}: {e}")















log.info("Bot is now running. Listening for new messages...")
datgbot.run_until_disconnected()

