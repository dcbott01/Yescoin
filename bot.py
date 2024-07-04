import requests
import time
import json
import sys
import random
from colorama import Fore, Style, init

init(autoreset=True)

# Function to print the welcome message
def print_welcome_message():
    print(r"""
 █ NAZARA █
    """)
    print(Fore.GREEN + Style.BRIGHT + "YesCoin BOT")
    print(Fore.GREEN + Style.BRIGHT + "Update Link: https://github.com")

# Function to load tokens from file
def load_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

# List of available colors for dynamic printing
available_colors = [Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

# Function to get headers for API requests
def get_headers(token):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://www.yescoin.gold',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.yescoin.gold/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'token': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

# Function to collect coins
def collect_coin(token, amount):
    url = 'https://api.yescoin.gold/game/collectCoin'
    headers = get_headers(token)
    data = json.dumps(amount)
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error collecting coins: {e}")
        return None

# Function to fetch account info
def fetch_account_info(token):
    try:
        url = 'https://api.yescoin.gold/account/getAccountInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching account info: {e}")
        return None

# Function to fetch game info
def fetch_game_info(token):
    try:
        url = 'https://api.yescoin.gold/game/getGameInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game info: {e}")
        return None

# Function to use special box
def use_special_box(token):
    url = 'https://api.yescoin.gold/game/recoverSpecialBox'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{Fore.GREEN + Style.BRIGHT}\rChest  : Activating...", end="", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\rChest  : Failed to activate", end="", flush=True)
            return False
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}\rChest  : Error", flush=True)
        return False

# Function to collect from special box
def collect_from_special_box(token, box_type, coin_count):
    url = 'https://api.yescoin.gold/game/collectSpecialBoxCoin'
    headers = get_headers(token)
    data = json.dumps({"boxType": box_type, "coinCount": coin_count})
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            if result['data']['collectStatus']:
                print(f"{random.choice(available_colors) + Style.BRIGHT}\rChest  : Collected {result['data']['collectAmount']} Coins", flush=True)
                return True, result['data']['collectAmount']
            else:
                print(f"{Fore.RED + Style.BRIGHT}\rChest  : No chest available          ", flush=True)
                return True, 0
        else:
            print(f"{Fore.RED + Style.BRIGHT}\rChest  : Failed to collect coins: {result['message']}", end="", flush=True)
            return False, 0
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED + Style.BRIGHT}\rChest  : Error: {e}", flush=True)
        return False, 0

# Function to attempt collecting special box coins
def attempt_collect_special_box(token, box_type, initial_coin_count):
    coin_count = initial_coin_count
    while coin_count > 0:
        success, collected_amount = collect_from_special_box(token, box_type, coin_count)
        if success:
            return collected_amount
        coin_count -= 10
    print(f"{Fore.RED + Style.BRIGHT}\rChest  : Unable to collect any coins after adjustments", flush=True)
    return 0

# Function to fetch account build info
def fetch_account_build_info(token):
    try:
        url = 'https://api.yescoin.gold/build/getAccountBuildInfo'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching account build info: {e}")
        return None

# Function to fetch squad info
def fetch_squad_info(token):
    url = 'https://api.yescoin.gold/squad/mySquad'
    headers = get_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching squad info: {e}")
        return None

# Function to join squad
def join_squad(token, squad_link):
    url = 'https://api.yescoin.gold/squad/joinSquad'
    headers = get_headers(token)
    data = json.dumps({"squadTgLink": squad_link})
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error joining squad: {e}")
        return None

# Function to recover coin pool
def recover_coin_pool(token):
    url = 'https://api.yescoin.gold/game/recoverCoinPool'
    headers = get_headers(token)
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            print(f"{random.choice(available_colors) + Style.BRIGHT}\rRecovery  : Success", flush=True)
            return True
        else:
            print(f"{Fore.RED + Style.BRIGHT}\rRecovery  : Failed", flush=True)
            return False
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED + Style.BRIGHT}\rRecovery  : Error: {e}", flush=True)
        return False

# Function to get user nickname
def get_my_user_nick(token):
    try:
        url = 'https://api.yescoin.gold/account/getRankingList?index=1&pageSize=1&rankType=1&userLevel=1'
        headers = get_headers(token)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'myUserNick' in data['data'] and data['data']['myUserNick']:
            return data['data']['myUserNick']
        else:
            return "no nickname"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching my user nick: {e}")
        return "no nickname"

# Main function
def main():
    tokens = load_tokens('tokens.txt')
    while True:
        print_welcome_message()
        for index, token in enumerate(tokens):
            nickname = get_my_user_nick(token)
            print(f"{Fore.BLUE + Style.BRIGHT}\n========[{Fore.WHITE + Style.BRIGHT} Account {index + 1} | {nickname} {Fore.BLUE + Style.BRIGHT}]========")
            
            # Fetch squad info
            print(f"{random.choice(available_colors)+Style.BRIGHT}\rSquad  : Getting...", end="", flush=True)
            squad_info = fetch_squad_info(token)
            if squad_info and squad_info['data']['isJoinSquad']:
                squad_title = squad_info['data']['squadInfo']['squadTitle']
                squad_members = squad_info['data']['squadInfo']['squadMembers']
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rSquad  : {squad_title} | {squad_members} Members")
            else:
                print(f"{Fore.YELLOW + Style.BRIGHT}\rSquad  : Not Joined Squad. Joining...", end="", flush=True)
                time.sleep(3)
                join_result = join_squad(token, "t.me/garapjajananchat")
                if join_result:
                    print(f"{random.choice(available_colors) + Style.BRIGHT}\rSquad  : Welcome Pemulung! {nickname} -", flush=True)
                else:
                    print(f"{random.choice(available_colors) + Style.BRIGHT}\rSquad  : Failed to join Squad.", flush=True)
            
            # Fetch account balance
            print(f"{random.choice(available_colors)+Style.BRIGHT}\rBalance  : Getting...", end="", flush=True)
            balance = fetch_account_info(token)
            if balance is None:
                print(f"{Fore.RED}\rBalance  : Failed to get balance", flush=True)
            else:
                balance = balance.get('data', {}).get('currentAmount', 0)
                balance = f"{balance:,}".replace(',', '.')
                print(f"{random.choice(available_colors) + Style.BRIGHT}\rBalance  : {balance}", flush=True)
            
            # Fetch game info
            print(f"{random.choice(available_colors)+Style.BRIGHT}\r[ Game Info ] : Getting...", end="", flush=True)
            game_info = fetch_account_build_info(token)
            if game_info is None:
                print(f"{Fore.RED}\r[ Game Info ] : Failed to get data", flush=True)
            else:
                special_box_left_recovery_count = game_info['data'].get('specialBoxLeftRecoveryCount', 0)
                coin_pool_left_recovery_count = game_info['data'].get('coinPoolLeftRecoveryCount', 0)
                single_coin_value = game_info['data'].get('singleCoinValue', 0)
                single_coin_level = game_info['data'].get('singleCoinLevel', 0)
                coin_pool_recovery_speed = game_info['data'].get('coinPoolRecoverySpeed', 0)
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rBooster  : Chest {special_box_left_recovery_count} | Recovery {coin_pool_left_recovery_count}", flush=True)
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rMultivalue  : Level {single_coin_value}", flush=True)
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rCoin Limit  : Level {single_coin_level}", flush=True)
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rFill Rate  : Level {coin_pool_recovery_speed}", flush=True)
            
            # Fetch game info (continued)
            print(f"{random.choice(available_colors)+Style.BRIGHT}\rGame Info  : Getting...", end="", flush=True)
            collect_info = fetch_game_info(token)
            if collect_info is None:
                print(f"{Fore.RED}\rGame Info  : Failed to get data", flush=True)
            else:
                single_coin_value = collect_info['data'].get('singleCoinValue', 0)
                coin_pool_left_count = collect_info['data'].get('coinPoolLeftCount', 0)
                print(f"{random.choice(available_colors) + Style.BRIGHT}\rCoin Left  : {coin_pool_left_count}", flush=True)
                
                # Collect coins
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rCollect  : Collecting Coins...", end="", flush=True)
                if coin_pool_left_count > 0:
                    amount = coin_pool_left_count // single_coin_value
                    collect_result = collect_coin(token, amount)
                    if collect_result and collect_result.get('code') == 0:
                        collected_amount = collect_result['data']['collectAmount']
                        print(f"{random.choice(available_colors) + Style.BRIGHT}\rCollect  : Collected {collected_amount}", flush=True)
                    else:
                        print(f"{random.choice(available_colors)+Style.BRIGHT}\rCollect  : Failed to collect coins", flush=True)
            
            # Activate special box
            print(f"{random.choice(available_colors)+Style.BRIGHT}\rChest  : Activating...", end="", flush=True)
            if game_info and game_info['data'].get('specialBoxLeftRecoveryCount', 0) > 0:
                if use_special_box(token):
                    print(f"{random.choice(available_colors)+Style.BRIGHT}\rChest  : Collecting...", end="", flush=True)
                    collected_amount = attempt_collect_special_box(token, 2, 240)  # Example: box_type=2, coin_count=250
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rChest  : No chest available", flush=True)
            
            # Recover coin pool
            time.sleep(2)
            print(f"{random.choice(available_colors)+Style.BRIGHT}\rRecovery  : Trying to recover...", end="", flush=True)
            game_info = fetch_account_build_info(token)
            if game_info and game_info['data'].get('coinPoolLeftRecoveryCount', 0) > 0:
                if recover_coin_pool(token):
                    # After recovery, attempt to collect coins again
                    collect_info = fetch_game_info(token)
                    if collect_info:
                        coin_pool_left_count = collect_info['data'].get('coinPoolLeftCount', 0)
                        if coin_pool_left_count > 0:
                            amount = coin_pool_left_count // game_info['data'].get('singleCoinValue', 1)
                            collect_result = collect_coin(token, amount)
                            if collect_result and collect_result.get('code') == 0:
                                collected_amount = collect_result['data']['collectAmount']
                                print(f"{Fore.GREEN + Style.BRIGHT}\rCollect  : Successfully collected {collected_amount} coins", flush=True)
                            else:
                                print(f"{Fore.RED + Style.BRIGHT}\rCollect  : Failed to collect coins", flush=True)
            else:
                print(f"{random.choice(available_colors)+Style.BRIGHT}\rRecovery  : No recovery available", flush=True)
            
            # Attempt to collect free chest
            time.sleep(2)
            print(f"{random.choice(available_colors)+Style.BRIGHT}\rFree Chest  : Trying to collect...", end="", flush=True)
            attempt_collect_special_box(token, 1, 230)  # Example: box_type=1, coin_count=230
            time.sleep(2)
        
        # Waiting for the next claim time
        print(f"\n{random.choice(available_colors)+Style.BRIGHT}========={Fore.WHITE+Style.BRIGHT}All accounts processed successfully{Fore.GREEN+Style.BRIGHT}=========", end="", flush=True)
        wait_time = 300  # 5 minutes in seconds
        for sec in range(wait_time, 0, -1):
            mins, secs = divmod(sec, 60)
            sys.stdout.write(f"\r{Fore.CYAN}Waiting for next claim time in {Fore.WHITE}{mins} minutes {secs} seconds")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\rNext claim time has arrived!                                                        \n")

if __name__ == '__main__':
    main()
