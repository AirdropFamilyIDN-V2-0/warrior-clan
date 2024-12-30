import requests
import json
from datetime import datetime, timedelta
from time import sleep
from colorama import Fore

mining_url = "https://srv.warriorclan.online/mining"
balance_url = "https://srv.warriorclan.online/wallet/balance"
claim_url = "https://srv.warriorclan.online/mining"  

def read_accounts(file_path="data.txt"):
    with open(file_path, "r") as file:
        accounts = file.readlines()
    return [account.strip() for account in accounts]

def check_balance(account_token, account_number):
    headers = {
        "Authorization": f"Bearer {account_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(balance_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            points = data["data"]["points"]
            coins = data["data"]["coins"]
            diamonds = data["data"]["diamonds"]
            usdt = data["data"]["usdt"]

            print(f"{Fore.GREEN}[{datetime.now()}] Account {account_number} balance:")
            print(f"  Points   : {points}")
            print(f"  Coins    : {coins}")
            print(f"  Diamonds : {diamonds}")
            print(f"  USDT     : {usdt}")
            print(f"{Fore.YELLOW}[{datetime.now()}] -------------------------------------")
        else:
            print(f"{Fore.RED}[{datetime.now()}] Error fetching balance for Account {account_number}: {response.text}")
    except requests.RequestException as e:
        print(f"{Fore.RED}[{datetime.now()}] Error: {str(e)}")

def get_mining_status(account_token):
    headers = {
        "Authorization": f"Bearer {account_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(mining_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            last_mining = data["data"].get("lastMining")
            if last_mining:
                print(f"{Fore.YELLOW}[{datetime.now()}] Last mining timestamp: {last_mining}")
            else:
                print(f"{Fore.GREEN}[{datetime.now()}] No active mining session.")
            return data
        else:
            print(f"{Fore.RED}[{datetime.now()}] Error fetching mining status: {response.text}")
            return None
    except requests.RequestException as e:
        print(f"{Fore.RED}[{datetime.now()}] Error: {str(e)}")
        return None

def start_mining(account_token, account_number):
    headers = {
        "Authorization": f"Bearer {account_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    payload = {
        "progress": 100, 
        "clientHash": account_token,  
    }

    mining_status = get_mining_status(account_token)
    if not mining_status or mining_status["data"].get("lastMining"):
        print(f"{Fore.RED}[{datetime.now()}] Mining already in progress for account {account_number}.")
        return False  

    try:
        response = requests.put(mining_url, headers=headers, json=payload)
        
        response.raise_for_status()  
        data = response.json()

        if data["statusCode"] == 200:
            print(f"{Fore.GREEN}[{datetime.now()}] Mining started successfully for account {account_number}.")
            return True
        else:
            print(f"{Fore.RED}[{datetime.now()}] Error starting mining for account {account_number}: {data}")
            return False
        
    except requests.RequestException as e:
        print(f"{Fore.RED}[{datetime.now()}] Error: {str(e)}")
        return False

def claim_mining(account_token, account_number):
    headers = {
        "Authorization": f"Bearer {account_token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
        "progress": 100,
        "clientHash": account_token,
    }

    mining_status = get_mining_status(account_token)
    if not mining_status:
        print(f"{Fore.RED}[{datetime.now()}] Could not fetch mining status for Account {account_number}.")
        return False

    last_mining = mining_status["data"].get("lastMining")
    if last_mining is not None:
        print(f"{Fore.GREEN}[{datetime.now()}] Mining session completed. Claiming rewards for Account {account_number}...")
        try:
            response = requests.post(claim_url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"{Fore.GREEN}[{datetime.now()}] Mining claimed successfully for account {account_number}.")
                print(f"  Points: {data['data']['reward']['points']}")
                return True
            else:
                print(f"{Fore.RED}[{datetime.now()}] Error claiming mining for account {account_number}: {response.text}")
                return False
        except requests.RequestException as e:
            print(f"{Fore.RED}[{datetime.now()}] Error: {str(e)}")
            return False
    else:
        print(f"{Fore.YELLOW}[{datetime.now()}] Mining still in progress, cannot claim yet for account {account_number}.")
        return False

def countdown_timer(seconds):
    print(f"{Fore.YELLOW}[{datetime.now()}] Countdown started for {seconds // 60} minutes ({seconds} seconds).")
    while seconds:
        mins, secs = divmod(seconds, 60)
        time_format = f"{mins:02}:{secs:02}"
        print(f"{Fore.CYAN}[{datetime.now()}] Time Remaining: {time_format}", end='\r') 
        sleep(1)
        seconds -= 1
    print(f"{Fore.GREEN}[{datetime.now()}] Countdown completed. Proceeding to next step.")


def run_bot():
    accounts = read_accounts()
    account_number = 1 

    print(f"{Fore.CYAN}[{datetime.now()}] =====  AirDropFamilyIDN  ====")
    print(f"{Fore.GREEN}[{datetime.now()}] = WARRIOR CLAN AUTO MINING =")
    print(f"{Fore.YELLOW}[{datetime.now()}] = Join VIP For Bot Premium =")
    print(f"{Fore.RED}[{datetime.now()}] ========= ADFMIDN ===========")

    while True: 
        for account_token in accounts:
            print(f"\n{Fore.CYAN}[{datetime.now()}] Logging in for Account {account_number}...")

            check_balance(account_token, account_number)

            print(f"{Fore.CYAN}[{datetime.now()}] Trying to claim mining for Account {account_number}...\n")
            claim_successful = claim_mining(account_token, account_number)

            if claim_successful:
                print(f"{Fore.GREEN}[{datetime.now()}] Claim successful! Now starting new mining for Account {account_number}...\n")
                start_successful = start_mining(account_token, account_number)

                if start_successful:
                    print(f"{Fore.GREEN}[{datetime.now()}] Mining started successfully for Account {account_number}.")
                else:
                    print(f"{Fore.RED}[{datetime.now()}] Mining failed for Account {account_number}.")
            else:
                print(f"{Fore.RED}[{datetime.now()}] Claim failed or not possible. Trying to start mining for Account {account_number}...\n")
                start_successful = start_mining(account_token, account_number)

                if not start_successful:
                    print(f"{Fore.RED}[{datetime.now()}] Mining failed. Trying to claim mining for Account {account_number}...\n")
                    claim_mining(account_token, account_number)
            
            print(f"{Fore.YELLOW}[{datetime.now()}] Waiting for mining process to complete for Account {account_number}...\n")
            sleep(2)  

            account_number += 1  
        
        print(f"{Fore.YELLOW}[{datetime.now()}] All accounts processed. Starting 10-minute countdown before retrying...")
        countdown_timer(600)  
        account_number = 1


if __name__ == "__main__":
    run_bot()

