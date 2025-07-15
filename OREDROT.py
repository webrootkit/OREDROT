import os
import sys
import nmap
import requests
from time import sleep
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller

# ASCII-арт в стиле webrootkit
BANNER = r"""
  ██████╗ ██████╗ ███████╗██████╗ ██████╗  ██████╗ ████████╗
 ██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗╚══██╔══╝
 ██║   ██║██████╔╝█████╗  ██║  ██║██████╔╝██║   ██║   ██║   
 ██║   ██║██╔══██╗██╔══╝  ██║  ██║██╔══██╗██║   ██║   ██║   
 ╚██████╔╝██║  ██║███████╗██████╔╝██║  ██║╚██████╔╝   ██║   
  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   
                                                             
                   by webrootkit | @webrootkit.matrix.org
"""

# Меню
def show_menu():
    os.system("clear" if os.name == "posix" else "cls")
    print(BANNER)
    print("\n[1] Сканировать сеть (Nmap)")
    print("[2] Проверить email на утечки")
    print("[3] Парсить даркнет (Tor)")
    print("[4] Анализ Bitcoin-кошелька")
    print("[5] Сгенерировать фейковые данные")
    print("[6] Выход\n")

# Генератор фейковых данных (как в Kyosuke)
def fake_data_generator():
    ua = UserAgent()
    fake_name = ua.first_name + " " + ua.last_name
    fake_email = f"{ua.username.lower()}@protonmail.com"
    fake_address = f"{ua.random.randint(1, 200)} {ua.street_suffix()}, {ua.city()}"
    
    print("\n[🔮] Фейковые данные:")
    print(f"  👤 Имя: {fake_name}")
    print(f"  📧 Email: {fake_email}")
    print(f"  🏠 Адрес: {fake_address}")

# Проверка Bitcoin-кошелька
def check_btc_wallet():
    wallet = input("\n[+] Введите BTC-адрес: ")
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{wallet}")
        data = response.json()
        print(f"\n[💰] Баланс: {data['final_balance'] / 100000000} BTC")
        print(f"[🔗] Транзакций: {data['n_tx']}")
    except Exception as e:
        print(f"[!] Ошибка: {e}")

# Главный цикл
def main():
    while True:
        show_menu()
        choice = input("\n[?] Выберите действие > ")
        
        if choice == "1":
            target = input("[🎯] Введите IP/домен: ")
            os.system(f"nmap -sV -T4 {target}")
        elif choice == "2":
            email = input("[📧] Введите email: ")
            check_leaks(email)
        elif choice == "3":
            darknet_parser()
        elif choice == "4":
            check_btc_wallet()
        elif choice == "5":
            fake_data_generator()
        elif choice == "6":
            print("\n[🖤] by webrootkit | До скорого!")
            sys.exit()
        else:
            print("\n[!] Неверный выбор!")
        
        input("\n[↵] Нажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    main()