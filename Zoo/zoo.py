# Zoo/zoo.py

# ===== Етап 1: Привітання =====
zoo_name = "MyZoo"
print(f"Welcome to {zoo_name}!")
print("Here you can see and manage the animals in our zoo.")

# ===== Етап 2: Створення списку тварин =====
animals = []  # порожній список тварин
print("Currently, there are no animals in the zoo.")

# ===== Етап 3: Додавання та перегляд тварин =====
while True:
    print("\nChoose an action:")
    print("1. Add an animal")
    print("2. Show all animals")
    print("3. Exit")
    
    choice = input("> ")
    
    if choice == "1":
        animal_name = input("Enter animal name: ")
        animals.append(animal_name)
        print(f"{animal_name} has been added to the zoo.")
    elif choice == "2":
        if animals:
            print("Animals in the zoo:")
            for i, animal in enumerate(animals, start=1):
                print(f"{i}. {animal}")
        else:
            print("The zoo is empty.")
    elif choice == "3":
        print("Goodbye! Thanks for visiting the zoo.")
        break
    else:
        print("Invalid choice. Please try again.")
