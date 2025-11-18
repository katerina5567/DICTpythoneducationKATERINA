class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.beans = 120
        self.cups = 9
        self.money = 550
        self.state = "choose_action"
        self.fill_stage = 0

    def print_state(self):
        print("The coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"{self.money} of money")

    def process(self, user_input):
        if self.state == "choose_action":
            if user_input == "buy":
                self.state = "buy"
                print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back – to main menu:")
            elif user_input == "fill":
                self.state = "fill"
                self.fill_stage = 1
                print("Write how many ml of water do you want to add:")
            elif user_input == "take":
                print(f"I gave you {self.money}")
                self.money = 0
            elif user_input == "remaining":
                self.print_state()
            elif user_input == "exit":
                self.state = "exit"
        elif self.state == "buy":
            if user_input == "back":
                self.state = "choose_action"
                return

            if user_input == "1":  # espresso
                w, m, b, price = 250, 0, 16, 4
            elif user_input == "2":  # latte
                w, m, b, price = 350, 75, 20, 7
            elif user_input == "3":  # cappuccino
                w, m, b, price = 200, 100, 12, 6
            else:
                return

            # check resources
            if self.water < w:
                print("Sorry, not enough water!")
            elif self.milk < m:
                print("Sorry, not enough milk!")
            elif self.beans < b:
                print("Sorry, not enough coffee beans!")
            elif self.cups < 1:
                print("Sorry, not enough disposable cups!")
            else:
                print("I have enough resources, making you a coffee!")
                self.water -= w
                self.milk -= m
                self.beans -= b
                self.cups -= 1
                self.money += price

            self.state = "choose_action"

        elif self.state == "fill":
            if self.fill_stage == 1:
                self.water += int(user_input)
                self.fill_stage = 2
                print("Write how many ml of milk do you want to add:")
            elif self.fill_stage == 2:
                self.milk += int(user_input)
                self.fill_stage = 3
                print("Write how many grams of coffee beans do you want to add:")
            elif self.fill_stage == 3:
                self.beans += int(user_input)
                self.fill_stage = 4
                print("Write how many disposable cups of coffee do you want to add:")
            elif self.fill_stage == 4:
                self.cups += int(user_input)
                self.state = "choose_action"

    def is_running(self):
        return self.state != "exit"


machine = CoffeeMachine()

while machine.is_running():
    if machine.state == "choose_action":
        user_input = input("Write action (buy, fill, take, remaining, exit):\n> ")
    else:
        user_input = input("> ")
    machine.process(user_input)
