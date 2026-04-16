import sqlite3
import random

class BankingSystem:
    def __init__(self):
        # Етап 3: Ініціалізація БД
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.create_table()
        self.current_card = None

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS card (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                pin TEXT NOT NULL,
                balance INTEGER DEFAULT 0
            );
        ''')
        self.conn.commit()

    def luhn_algorithm(self, card_number_15):
        """Реалізація Етапу 2: Обчислення контрольної цифри Луна"""
        digits = [int(d) for d in card_number_15]
        
        # Крок 1-3: Множимо непарні позиції на 2 та віднімаємо 9, якщо > 9
        for i in range(len(digits)):
            if (i + 1) % 2 != 0:
                digits[i] *= 2
                if digits[i] > 9:
                    digits[i] -= 9
        
        # Крок 4-5: Знаходимо суму та контрольну цифру
        total_sum = sum(digits)
        checksum = (10 - (total_sum % 10)) % 10
        return str(checksum)

    def is_luhn_valid(self, card_number):
        if len(card_number) != 16:
            return False
        return card_number[-1] == self.luhn_algorithm(card_number[:-1])

    def create_account(self):
        # Етап 1: Генерація IIN (400000) + Account Identifier (9 цифр)
        iin = "400000"
        while True:
            account_id = ''.join([str(random.randint(0, 9)) for _ in range(9)])
            temp_card = iin + account_id
            checksum = self.luhn_algorithm(temp_card)
            full_card = temp_card + checksum
            
            # Перевірка на унікальність в БД
            self.cur.execute('SELECT number FROM card WHERE number = ?', (full_card,))
            if not self.cur.fetchone():
                break
        
        pin = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        
        # Збереження в БД
        self.cur.execute('INSERT INTO card (number, pin) VALUES (?, ?)', (full_card, pin))
        self.conn.commit()
        
        print("\nYour card has been created")
        print(f"Your card number:\n{full_card}")
        print(f"Your card PIN:\n{pin}\n")

    def login(self):
        print("\nEnter your card number:")
        card_num = input(">")
        print("Enter your PIN:")
        pin_num = input(">")

        self.cur.execute('SELECT number, pin, balance FROM card WHERE number = ? AND pin = ?', (card_num, pin_num))
        account = self.cur.fetchone()

        if account:
            print("\nYou have successfully logged in!")
            self.current_card = card_num
            self.account_menu()
        else:
            print("\nWrong card number or PIN!\n")

    def account_menu(self):
        while self.current_card:
            # Етап 4: Розширене меню аккаунта
            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
            choice = input(">")

            if choice == '1':
                self.cur.execute('SELECT balance FROM card WHERE number = ?', (self.current_card,))
                print(f"\nBalance: {self.cur.fetchone()[0]}\n")
            
            elif choice == '2':
                print("\nEnter income:")
                income = int(input(">"))
                self.cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (income, self.current_card))
                self.conn.commit()
                print("Income was added!\n")

            elif choice == '3':
                self.do_transfer()

            elif choice == '4':
                self.cur.execute('DELETE FROM card WHERE number = ?', (self.current_card,))
                self.conn.commit()
                self.current_card = None
                print("\nThe account has been closed!\n")

            elif choice == '5':
                self.current_card = None
                print("\nYou have successfully logged out!\n")

            elif choice == '0':
                print("\nBye!")
                exit()

    def do_transfer(self):
        print("\nTransfer")
        print("Enter card number:")
        target_card = input(">")

        # Перевірки з Етапу 4
        if target_card == self.current_card:
            print("You can't transfer money to the same account!\n")
            return

        if not self.is_luhn_valid(target_card):
            print("Probably you made a mistake in the card number. Please try again!\n")
            return

        self.cur.execute('SELECT balance FROM card WHERE number = ?', (target_card,))
        if not self.cur.fetchone():
            print("Such a card does not exist.\n")
            return

        print("Enter how much money you want to transfer:")
        amount = int(input(">"))

        self.cur.execute('SELECT balance FROM card WHERE number = ?', (self.current_card,))
        current_balance = self.cur.fetchone()[0]

        if amount > current_balance:
            print("Not enough money!\n")
        else:
            # Виконання транзакції
            self.cur.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (amount, self.current_card))
            self.cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (amount, target_card))
            self.conn.commit()
            print("Success!\n")

    def run(self):
        while True:
            print("1. Create an account\n2. Log into account\0. Exit")
            choice = input(">")
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print("\nBye!")
                break

if __name__ == "__main__":
    bank = BankingSystem()
    bank.run()