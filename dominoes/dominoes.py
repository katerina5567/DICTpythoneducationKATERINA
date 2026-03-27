import random

def create_dominoes():
    return [[i, j] for i in range(7) for j in range(i, 7)]

def deal_cards():
    while True:
        stock = create_dominoes()
        random.shuffle(stock)
        
        computer = [stock.pop() for _ in range(7)]
        player = [stock.pop() for _ in range(7)]
        
        # Пошук стартового дубля
        max_double = -1
        status = ""
        snake = []
        
        for i in range(6, -1, -1):
            if [i, i] in computer:
                max_double = i
                status = "player"
                computer.remove([i, i])
                snake.append([i, i])
                break
            elif [i, i] in player:
                max_double = i
                status = "computer"
                player.remove([i, i])
                snake.append([i, i])
                break
        
        if max_double != -1:
            return stock, computer, player, snake, status

def print_interface(stock, computer, player, snake, status):
    print("=" * 70)
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}\n")
    
    # Вивід змійки (Етап 3: скорочення довгих ліній)
    if len(snake) <= 6:
        print("".join(str(p) for p in snake))
    else:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")
    
    print("\nYour pieces:")
    for i, piece in enumerate(player, 1):
        print(f"{i}:{piece}")
    
    print("\nStatus:", end=" ")
    if status == "player":
        print("It's your turn to make a move. Enter your command.")
    elif status == "computer":
        print("Computer is about to make a move. Press Enter to continue...")
    elif status == "win":
        print("The game is over. You won!")
    elif status == "lose":
        print("The game is over. The computer won!")
    elif status == "draw":
        print("The game is over. It's a draw!")

def check_end_game(player, computer, snake):
    if len(player) == 0:
        return "win"
    if len(computer) == 0:
        return "lose"
    
    # Умова нічиї (цифри на кінцях однакові і зустрічаються 8 разів)
    if snake[0][0] == snake[-1][1]:
        num = snake[0][0]
        count = sum(piece.count(num) for piece in snake)
        if count == 8:
            return "draw"
    return None

def get_computer_move(computer, snake):
    # Етап 5: Алгоритм оцінки (Heuristic)
    counts = {i: 0 for i in range(7)}
    for piece in computer + snake:
        for num in piece:
            counts[num] += 1
    
    scores = []
    for i, piece in enumerate(computer):
        score = counts[piece[0]] + counts[piece[1]]
        scores.append((score, i))
    
    # Сортуємо за оцінкою (від більшої до меншої)
    scores.sort(key=lambda x: x[0], reverse=True)
    
    for _, idx in scores:
        piece = computer[idx]
        # Пробуємо праворуч
        if piece[0] == snake[-1][1]:
            return idx + 1
        if piece[1] == snake[-1][1]:
            return idx + 1
        # Пробуємо ліворуч
        if piece[1] == snake[0][0]:
            return -(idx + 1)
        if piece[0] == snake[0][0]:
            return -(idx + 1)
            
    return 0 # Якщо нічого не підійшло

def make_move(pieces, snake, move, stock):
    if move == 0:
        if stock:
            pieces.append(stock.pop())
        return True
    
    idx = abs(move) - 1
    piece = pieces[idx]
    
    if move > 0: # Праворуч
        if piece[0] == snake[-1][1]:
            snake.append(pieces.pop(idx))
        elif piece[1] == snake[-1][1]:
            p = pieces.pop(idx)
            snake.append([p[1], p[0]])
        else:
            return False
    else: # Ліворуч
        if piece[1] == snake[0][0]:
            snake.insert(0, pieces.pop(idx))
        elif piece[0] == snake[0][0]:
            p = pieces.pop(idx)
            snake.insert(0, [p[1], p[0]])
        else:
            return False
    return True

def main():
    stock, computer, player, snake, status = deal_cards()
    
    while True:
        print_interface(stock, computer, player, snake, status)
        
        res = check_end_game(player, computer, snake)
        if res:
            status = res
            print_interface(stock, computer, player, snake, status)
            break

        if status == "player":
            while True:
                try:
                    move = input()
                    if move.lower() == 'exit': return
                    move = int(move)
                    if abs(move) > len(player):
                        raise ValueError
                    
                    if make_move(player, snake, move, stock):
                        status = "computer"
                        break
                    else:
                        print("Illegal move. Please try again.")
                except ValueError:
                    print("Invalid input. Please try again.")
        
        elif status == "computer":
            input()
            # Використання алгоритму з Етапу 5
            move = get_computer_move(computer, snake)
            make_move(computer, snake, move, stock)
            status = "player"

if __name__ == "__main__":
    main()