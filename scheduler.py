import requests
import json
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import re

WALLET_NAME = ""
WALLET_PW = ""
BOT_TOKEN = ""
CHAT_ID = ""
EMOJIS = { "money_bag": "💰", "miner" : "⛏", "daily": "📅"}
DOCKER = True
if DOCKER == True:
    HOST_URL = "alephium"
else:
    HOST_URL = "localhost"


def get_balance():
    url = "http://{host}:12973/wallets/{wallet_name}/balances".format(host=HOST_URL,wallet_name=WALLET_NAME)
    response = requests.request("GET", url)
    answer = round(int(response.json()['totalBalance']) / 1000000000000000000,2)
    return str(answer)
    
def unlock_wallet():
    headers = {
    'accept': '*/*',
    'Content-Type': 'application/json',
    }
    data = "{" + f"\"password\": \"{WALLET_PW}\"" + "}"
    url = 'http://{host}:12973/wallets/{wallet}/unlock'.format(host=HOST_URL,wallet=WALLET_NAME)
    response = requests.post(url, headers=headers, data=data)
    
def send_message_to_telegram_group(message):
    bot_token = BOT_TOKEN
    data = {
      'chat_id': CHAT_ID,
      'text': message
        }
    url = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=bot_token)

    response = requests.post(url, data=data)

def get_chat_id():
    bot_token = BOT_TOKEN
    url = "https://api.telegram.org/bot{token}/getUpdates".format(token=bot_token)
    requests.get(url).json()
       
class BalanceHolder():
    def __init__(self):
        self.old_balance = 0

class HourlyUpdate():
    def __init__(self):
        self.balances = []

class DailyHolder():
    def __init__(self):
        self.revenues = 0.0
       
balance_holder = BalanceHolder()
hourly_balance_holder = HourlyUpdate()
daily_balance_holder = DailyHolder()

def scheduler_function():
    unlock_wallet()
    balance = get_balance()
    print("balance", balance)
    print("old_balance", balance_holder.old_balance)
    if not balance == balance_holder.old_balance:
        send_message_to_telegram_group(balance)
    balance_holder.old_balance = balance
    hourly_balance_holder.balances.append(balance)
    
## Hourly scheduler function

def calculate_revenue(array):
    try:
        hourly_revenue = float(array[-1]) - float(array[0])
        return str("{:.2f}".format(hourly_revenue))
    except:
        return "no data"
        
def get_gpu_hashrate():
    try:
        bashCommand = "docker logs docker_alephium_gpu_miner_1 --tail 2"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        stripped_string = re.findall(r"\d+\.\d+", output.decode("utf-8"))[0]
        f_convert = "{:.0f}".format(float(stripped_string))
        return f_convert
    except Exception as e:
        print(e)
        return "no data"

def create_hourly_update(hourly, hashrate, daily):
    return "Hourly update\n{bag} {money_mined} ALPH\n{hourly_ico} {daily} TOTAL ALPH TODAY".format(bag=EMOJIS['money_bag'],money_mined=hourly, hourly_ico=EMOJIS['daily'], daily=daily)

def scheduler_hourly_function():
    revenue = calculate_revenue(hourly_balance_holder.balances)
    if revenue == "no data":
        daily_balance_holder.revenues += float(0)
    else:
        daily_balance_holder.revenues += float(revenue)
    message = create_hourly_update(revenue, 0, daily_balance_holder.revenues)
    send_message_to_telegram_group(message)
    hourly_balance_holder.balances = []

def scheduler_daily_function():
    hourly_balance_holder.revenues = 0.0
    

if __name__ == '__main__':
    print("starting...")
    send_message_to_telegram_group("starting tracking...\nsending test message...")
    send_message_to_telegram_group(create_hourly_update(0,0,0))
    scheduler = BlockingScheduler()
    job = scheduler.add_job(scheduler_function, 'interval', seconds=30)
    job = scheduler.add_job(scheduler_hourly_function, 'interval', minutes=60)
    job = scheduler.add_job(scheduler_daily_function, 'interval', hours=24)
    scheduler.start()
    
    
    
    
