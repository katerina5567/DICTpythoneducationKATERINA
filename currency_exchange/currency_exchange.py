import requests

def currency_exchange():
    # Отримуємо базову валюту (наприклад, USD)
    base_currency = input("Введіть код вашої валюти: ").lower()
    
    # Створюємо кеш. За умовою Етапу 4, USD та EUR мають бути там (якщо вони не є базовою валютою)
    cache = {}
    
    # Функція для отримання даних з API
    def get_rates(currency_code):
        url = f"http://www.floatrates.com/daily/{currency_code}.json"
        response = requests.get(url)
        return response.json()

    # Початкове заповнення кешу для USD та EUR (якщо це можливо)
    try:
        rates_data = get_rates(base_currency)
        if base_currency != 'usd':
            cache['usd'] = rates_data['usd']['rate']
        if base_currency != 'eur':
            cache['eur'] = rates_data['eur']['rate']
    except Exception as e:
        print("Помилка при підключенні до сервісу.")
        return

    while True:
        # Введення цільової валюти
        target_currency = input("Введіть валюту для отримання (або порожньо для виходу): ").lower()
        if not target_currency:
            break
            
        # Введення суми
        try:
            amount = float(input("Введіть суму грошей: "))
        except ValueError:
            print("Будь ласка, введіть число.")
            continue

        print("Checking the cache...")
        
        if target_currency in cache:
            print("It is in the cache!")
            rate = cache[target_currency]
        else:
            print("Sorry, but it is not in the cache!")
            # Якщо в кеші немає, робимо запит і додаємо в кеш
            try:
                # Оскільки ми вже завантажили повний список курсів для base_currency раніше, 
                # ми можемо просто взяти його з rates_data
                if target_currency in rates_data:
                    rate = rates_data[target_currency]['rate']
                    cache[target_currency] = rate
                else:
                    print("Такої валюти не знайдено в API.")
                    continue
            except Exception:
                print("Помилка оновлення даних.")
                continue

        # Розрахунок
        result = round(amount * rate, 2)
        print(f"You received {result} {target_currency.upper()}.")

if __name__ == "__main__":
    currency_exchange()