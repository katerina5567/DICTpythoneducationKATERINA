# Zoo/zoo.py

animals = []  

def show_menu():
    print("Welcome to the Zoo!")
    print("1. Show all animals")
    print("2. Add an animal")
    print("3. Remove an animal")
    print("4. Exit")

while True:
    show_menu()
    choice = input("> ")

    if choice == "1":
        if animals:
            print("Animals in the zoo:")
            for a in animals:
                print(f"- {a}")
        else:
            print("The zoo is empty.")
    elif choice == "2":
        name = input("Enter the name of the animal: ")
        animals.append(name)
        print(f"{name} was added to the zoo!")
    elif choice == "3":
        name = input("Enter the name of the animal to remove: ")
        if name in animals:
            animals.remove(name)
            print(f"{name} was removed from the zoo!")
        else:
            print(f"{name} is not in the zoo.")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")
