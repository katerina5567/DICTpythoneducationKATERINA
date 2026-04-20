import random


def get_level():
    while True:
        print("Which level do you want? Enter a number:")
        print("1 - simple operations with numbers 2-9")
        print("2 - integral squares of 11-29")

        level = input()

        if level in ("1", "2"):
            return int(level)
        else:
            print("Incorrect format.")


def generate_question(level):
    if level == 1:
        num1 = random.randint(2, 9)
        num2 = random.randint(2, 9)
        operation = random.choice(["+", "-", "*"])
        print(f"{num1} {operation} {num2}")
        answer = eval(f"{num1}{operation}{num2}")
        return answer
    else:
        num = random.randint(11, 29)
        print(num)
        return num ** 2


def get_user_answer():
    while True:
        try:
            return int(input())
        except ValueError:
            print("Incorrect format.")


def save_result(name, score, level):
    descriptions = {
        1: "simple operations with numbers 2-9",
        2: "integral squares of 11-29"
    }

    with open("results.txt", "a") as file:
        file.write(f"{name}: {score}/5 in level {level} ({descriptions[level]}).\n")

    print('The results are saved in "results.txt".')


def main():
    level = get_level()
    score = 0

    for _ in range(5):
        correct_answer = generate_question(level)
        user_answer = get_user_answer()

        if user_answer == correct_answer:
            print("Right!")
            score += 1
        else:
            print("Wrong!")

    print(f"Your mark is {score}/5.")
    print("Would you like to save your result to the file? Enter yes or no.")

    save = input().lower()

    if save in ("yes", "y"):
        print("What is your name?")
        name = input()
        save_result(name, score, level)


if __name__ == "__main__":
    main()