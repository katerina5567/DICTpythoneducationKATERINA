def print_help():
    print("Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line")
    print("Special commands: !help !done")


def add_plain():
    text = input("Text: ")
    return text


def add_bold():
    text = input("Text: ")
    return f"**{text}**"


def add_italic():
    text = input("Text: ")
    return f"*{text}*"


def add_inline_code():
    text = input("Text: ")
    return f"`{text}`"


def add_link():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"


def add_header():
    while True:
        try:
            level = int(input("Level: "))
            if 1 <= level <= 6:
                break
            else:
                print("The level should be within the range of 1 to 6")
        except ValueError:
            print("The level should be within the range of 1 to 6")

    text = input("Text: ")
    return f"{'#' * level} {text}\n"


# ВИПРАВЛЕНО: тепер повертає два переноси для нового абзацу
def add_new_line():
    return "\n\n"


def add_list(list_type):
    while True:
        try:
            rows = int(input("Number of rows: "))
            if rows > 0:
                break
            else:
                print("The number of rows should be greater than zero")
        except ValueError:
            print("The number of rows should be greater than zero")

    # ВИПРАВЛЕНО: додаємо початковий \n, щоб список починався з нового рядка
    result = "\n"
    
    for i in range(1, rows + 1):
        row_text = input(f"Row #{i}: ")
        if list_type == "ordered-list":
            result += f"{i}. {row_text}\n"
        else:
            result += f"* {row_text}\n"

    return result


def main():
    markdown = ""

    while True:
        command = input("Choose a formatter: ")

        if command == "!help":
            print_help()

        elif command == "!done":
            with open("output.md", "w", encoding="utf-8") as file:
                file.write(markdown)
            break

        elif command == "plain":
            markdown += add_plain()

        elif command == "bold":
            markdown += add_bold()

        elif command == "italic":
            markdown += add_italic()

        elif command == "inline-code":
            markdown += add_inline_code()

        elif command == "link":
            markdown += add_link()

        elif command == "header":
            markdown += add_header()

        elif command == "new-line":
            markdown += add_new_line()

        elif command in ["ordered-list", "unordered-list"]:
            markdown += add_list(command)

        else:
            print("Unknown formatting type or command")
            continue

        print(markdown)


if __name__ == "__main__":
    main()