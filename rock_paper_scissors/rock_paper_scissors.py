import random

# --- Робота з рейтингом ---
print("Enter your name:", end=" ")
name = input()
print(f"Hello, {name}")

rating = 0

try:
    with open("rating.txt", "r") as file:
        for line in file:
            user, score = line.strip().split()
            if user == name:
                rating = int(score)
                break
except FileNotFoundError:
    pass  # якщо файлу немає — починаємо з 0

# --- Зчитування опцій ---
options_input = input()

if options_input.strip() == "":
    options = ["rock", "paper", "scissors"]
else:
    options = options_input.strip().split(",")

print("Okay, let's start")

# --- Основний цикл гри ---
while True:
    user_choice = input()

    if user_choice == "!exit":
        print("Bye!")
        break

    elif user_choice == "!rating":
        print(f"Your rating: {rating}")

    elif user_choice not in options:
        print("Invalid input")

    else:
        computer_choice = random.choice(options)

        if user_choice == computer_choice:
            print(f"There is a draw ({computer_choice})")
            rating += 50
        else:
            # алгоритм визначення переможця
            index = options.index(user_choice)
            rotated = options[index + 1:] + options[:index]
            half = len(rotated) // 2
            losing_options = rotated[:half]

            if computer_choice in losing_options:
                print(f"Sorry, but the computer chose {computer_choice}")
            else:
                print(f"Well done. The computer chose {computer_choice} and failed")
                rating += 100