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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_menu():
    clear_screen()
    print(BANNER)
    print("\n[1] Сканировать сеть (Nmap)")
    print("[2] Проверить email на утечки")
    print("[3] Парсить даркнет (Tor)")
    print("[4] Анализ Bitcoin-кошелька")
    print("[5] Сгенерировать фейковые данные")
    print("[6] Выход\n")

def scan_network():
    target = input("[🎯] Введите IP/домен: ")
    try:
        nm = nmap.PortScanner()
        print(f"\n[🔍] Сканирую {target}...")
        nm.scan(hosts=target, arguments='-T4 -A -v')
        
        print("\n[📊] Результаты сканирования:")
        for host in nm.all_hosts():
            print(f"\n[🖥️] Хост: {host} ({nm[host].hostname()})")
            print(f"[🔒] Состояние: {nm[host].state()}")
            
            for proto in nm[host].all_protocols():
                print(f"\n[📡] Протокол: {proto}")
                ports = nm[host][proto].keys()
                for port in sorted(ports):
                    print(f"  🚪 Порт: {port}\tСервис: {nm[host][proto][port]['name']}\tСостояние: {nm[host][proto][port]['state']}")
    except Exception as e:
        print(f"[❌] Ошибка сканирования: {e}")

def check_leaks(email):
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {"hibp-api-key": "ваш_api_ключ"}  # Замените на реальный ключ
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("\n[💀] Найдены утечки в сервисах:")
            for breach in response.json():
                print(f"  🔥 {breach['Name']} ({breach['BreachDate']})")
        else:
            print("\n[✅] Утечек не найдено!")
    except Exception as e:
        print(f"\n[❌] Ошибка: {e}")

def darknet_parser():
    print("\n[🌑] Функция в разработке...")
    # Реализация парсинга через Tor

def check_btc_wallet():
    wallet = input("\n[+] Введите BTC-адрес: ")
    try:
        response = requests.get(f"https://blockchain.info/rawaddr/{wallet}", timeout=10)
        data = response.json()
        print(f"\n[💰] Баланс: {data['final_balance'] / 100000000:.8f} BTC")
        print(f"[🔗] Транзакций: {data['n_tx']}")
    except Exception as e:
        print(f"[❌] Ошибка: {e}")

def fake_data_generator():
    ua = UserAgent()
    fake_name = f"{ua.first_name()} {ua.last_name()}"
    fake_email = f"{ua.user_name()}@protonmail.com"
    fake_address = f"{ua.random.randint(1, 200)} {ua.street_suffix()}, {ua.city()}"
    
    print("\n[🔮] Фейковые данные:")
    print(f"  👤 Имя: {fake_name}")
    print(f"  📧 Email: {fake_email}")
    print(f"  🏠 Адрес: {fake_address}")

def main():
    while True:
        show_menu()
        choice = input("\n[?] Выберите действие > ")
        
        if choice == "1":
            scan_network()
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
            print("\n[⚠️] Неверный выбор!")
        
        input("\n[↵] Нажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[🛑] Программа завершена пользователем")
        sys.exit(0)
