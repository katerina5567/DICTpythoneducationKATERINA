import random

# Этап 1: Добавляем друзей
num_friends = int(input("Enter the number of friends joining (including you):\n> "))
if num_friends <= 0:
    print("No one is joining for the party")
else:
    friends = {}
    print("Enter the name of every friend (including you), each on a new line:")
    for _ in range(num_friends):
        name = input("> ")
        friends[name] = 0

    # Этап 2: Разделяем счёт поровну
    total_amount = float(input("Enter the total amount:\n> "))
    split_amount = round(total_amount / num_friends, 2)
    for name in friends:
        friends[name] = split_amount

    # Этап 3 и 4: Выбор щасливчика
    use_lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ')
    if use_lucky == "Yes":
        lucky_one = random.choice(list(friends.keys()))
        print(f"{lucky_one} is the lucky one!")
        if num_friends > 1:
            split_amount = round(total_amount / (num_friends - 1), 2)
            for name in friends:
                if name != lucky_one:
                    friends[name] = split_amount
                else:
                    friends[name] = 0
        else:
            # Если только один участник, он сам счастливчик
            friends[lucky_one] = 0
    else:
        print("No one is going to be lucky")

    # Вывод словаря
    print(friends)

