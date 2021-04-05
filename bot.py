import sys, io, logging, json, math, httpx, time
from babel.numbers import format_currency
from telegram import ParseMode, MessageEntity, ChatAction, Update, Bot
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, run_async
from telegram.utils.helpers import escape_markdown

BOT_TOKEN = 'PUTYOURTELEGRAMBOTTOKENHERE'
ETHER_API = 'PUTYOURETHERSCANAPIKEYHERE'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
client = httpx.Client()

@run_async
def start(update, context):
    msg_start = io.StringIO()
    print(
        '\n','*','Type','*',',',
        '\n/gas to see the current gas value',
        '\n/prices to see the current prices(in USD and IDR) of ETH, AXS, SLP'
        '\n',
        '\n','*','Info','*',' :',
        '\n','[Gas Tracker Source](https://etherscan.io/apis)',
        '\n','[ETH Price(in USD) Source](https://etherscan.io/apis)',
        '\n','[ETH Price(in IDR) Source](https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=idr)',
        '\n','[AXS Price Source](https://api.coingecko.com/api/v3/simple/price?ids=axie-infinity&vs_currencies=usd)',
        '\n','[SLP Price Source](https://api.coingecko.com/api/v3/simple/price?ids=small-love-potion&vs_currencies=usd)',
        sep="",file=msg_start
        )
    mstart = msg_start.getvalue()
    update.message.reply_text(quote=True, text=mstart, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def gtracker():
    gas_url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=' + ETHER_API
    time.sleep(0.2)
    gas_response = client.get(gas_url)
    gas_data = json.loads(gas_response.text)
    gas_result = gas_data["result"]
    gtracker.gas_low = gas_result["SafeGasPrice"]
    gtracker.gas_avg = gas_result["ProposeGasPrice"]
    gtracker.gas_high = gas_result["FastGasPrice"]
    #GasEsT
    tgas_url = 'https://api.etherscan.io/api?module=gastracker&action=gasestimate&gasprice='
    tgas_url2 = '000000000&apikey='
    tlgas_url = tgas_url + str(gtracker.gas_low) + tgas_url2 + ETHER_API
    time.sleep(0.2)
    tlgas_response = client.get(tlgas_url)
    tlgas_data = json.loads(tlgas_response.text)
    tlgas_s = tlgas_data["result"]
    gtracker.tlgas_sec = int(tlgas_s)
    tagas_url = tgas_url + str(gtracker.gas_avg) + tgas_url2 + ETHER_API
    time.sleep(0.2)
    tagas_response = client.get(tagas_url)
    tagas_data = json.loads(tagas_response.text)
    tagas_s = tagas_data["result"]
    gtracker.tagas_sec = int(tagas_s)
    thgas_url = tgas_url + str(gtracker.gas_high) + tgas_url2 + ETHER_API
    time.sleep(0.2)
    thgas_response =  client.get(thgas_url)
    thgas_data = json.loads(thgas_response.text)
    thgas_s = thgas_data["result"]
    gtracker.thgas_sec = int(thgas_s)
gtracker()

@run_async
def gas(update, context):
    gtracker()
    msg_gas = io.StringIO()
    print(
        '=====================',
        '\n','*','GAS TRACKER','*',
        '\n=====================',
        '\n','*','LOW','*',' ~ ',gtracker.tlgas_sec,'s = ','```',gtracker.gas_low,'```',' Gwei',
        '\n','*','AVG','*',' ~ ',gtracker.tagas_sec,'s = ','```',gtracker.gas_avg,'```',' Gwei',
        '\n','*','HIGH','*',' ~ ',gtracker.thgas_sec,'s = ','```',gtracker.gas_high,'```',' Gwei',
        '\n=====================',
        sep="",file=msg_gas
        )
    mgas = msg_gas.getvalue()
    update.message.reply_text(quote=True, text=mgas, parse_mode=ParseMode.MARKDOWN)

@run_async
def ptracker():
        #PriceUSD
        peth_url = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + ETHER_API
        time.sleep(0.2)
        peth_response = client.get(peth_url)
        peth_data = json.loads(peth_response.text)
        peth_result = peth_data["result"]
        pethr = peth_result["ethusd"]
        ptracker.peth = format_currency(pethr, 'USD', locale="en_GB")
        paxs_url = 'https://api.coingecko.com/api/v3/simple/price?ids=axie-infinity&vs_currencies=usd'
        paxs_response = client.get(paxs_url)
        paxs_data = json.loads(paxs_response.text)
        paxs_result = paxs_data["axie-infinity"]
        paxsr = paxs_result["usd"]
        ptracker.paxs = format_currency(paxsr, 'USD', locale="en_GB")
        pslp_url = 'https://api.coingecko.com/api/v3/simple/price?ids=small-love-potion&vs_currencies=usd'
        pslp_response =  client.get(pslp_url)
        pslp_data = json.loads(pslp_response.text)
        pslp_result = pslp_data["small-love-potion"]
        pslpr = pslp_result["usd"]
        ptracker.pslp = format_currency(pslpr, 'USD', locale="en_GB")
        #PriceIDR
        pethid_url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=idr'
        pethid_response = client.get(pethid_url)
        pethid_data = json.loads(pethid_response.text)
        pethid_result = pethid_data["ethereum"]
        pethidr = pethid_result["idr"]
        ptracker.pethid = format_currency(pethidr, 'IDR', locale="id_ID")
        paxsid_url = 'https://api.coingecko.com/api/v3/simple/price?ids=axie-infinity&vs_currencies=idr'
        paxsid_response = client.get(paxsid_url)
        paxsid_data = json.loads(paxsid_response.text)
        paxsid_result = paxsid_data["axie-infinity"]
        paxsidr = paxsid_result["idr"]
        ptracker.paxsid = format_currency(paxsidr, 'IDR', locale="id_ID")
        pslpid_url = 'https://api.coingecko.com/api/v3/simple/price?ids=small-love-potion&vs_currencies=idr'
        pslpid_response =  client.get(pslpid_url)
        pslpid_data = json.loads(pslpid_response.text)
        pslpid_result = pslpid_data["small-love-potion"]
        pslpidr = pslpid_result["idr"]
        ptracker.pslpid = format_currency(pslpidr, 'IDR', locale="id_ID")
ptracker()

@run_async
def prices(update, context):
    ptracker()
    msg_price = io.StringIO()
    print(
        '====================', 
        '\n','*','PRICES TRACKER','*',
        '\n====================',
        '\n','*','ETH','*',' = ',ptracker.peth,
        '\n','*','AXS','*',' = ',ptracker.paxs,
        '\n','*','SLP','*',' = ',ptracker.pslp,
        '\n====================',
        '\n','*','ETH','*',' = ',ptracker.pethid,
        '\n','*','AXS','*',' = ',ptracker.paxsid,
        '\n','*','SLP','*',' = ',ptracker.pslpid,
        '\n====================',
        sep="",file=msg_price
        )
    mprice = msg_price.getvalue()
    update.message.reply_text(quote=True, text=mprice, parse_mode=ParseMode.MARKDOWN)

@run_async
def error(context, update):
    logger.warning('Update "%s" caused error "%s"', context, update.error)

def run():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('gas', gas))
    dispatcher.add_handler(CommandHandler('prices', prices))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
run()
