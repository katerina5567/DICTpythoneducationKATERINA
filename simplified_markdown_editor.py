markdown = ""


def print_help():
    print("Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line")
    print("Special commands: !help !done")


def plain():
    text = input("Text: ")
    return text


def bold():
    text = input("Text: ")
    return f"**{text}**"


def italic():
    text = input("Text: ")
    return f"*{text}*"


def inline_code():
    text = input("Text: ")
    return f"`{text}`"


def link():
    label = input("Label: ")
    url = input("URL: ")
    return f"[{label}]({url})"


def header():
    while True:
        level = int(input("Level: "))
        if 1 <= level <= 6:
            break
        else:
            print("The level should be within the range of 1 to 6")

    text = input("Text: ")
    return f"{'#' * level} {text}\n"


def new_line():
    return "\n"


def make_list(list_type):
    while True:
        rows = int(input("Number of rows: "))
        if rows > 0:
            break
        else:
            print("The number of rows should be greater than zero")

    result = ""
    for i in range(1, rows + 1):
        text = input(f"Row #{i}: ")
        if list_type == "ordered-list":
            result += f"{i}. {text}\n"
        else:
            result += f"* {text}\n"

    return result


while True:
    command = input("Choose a formatter: ")

    if command == "!help":
        print_help()

    elif command == "!done":
        file = open("output.md", "w", encoding="utf-8")
        file.write(markdown)
        file.close()
        break

    elif command == "plain":
        markdown += plain()

    elif command == "bold":
        markdown += bold()

    elif command == "italic":
        markdown += italic()

    elif command == "inline-code":
        markdown += inline_code()

    elif command == "link":
        markdown += link()

    elif command == "header":
        markdown += header()

    elif command == "new-line":
        markdown += new_line()

    elif command == "ordered-list":
        markdown += make_list("ordered-list")

    elif command == "unordered-list":
        markdown += make_list("unordered-list")

    else:
        print("Unknown formatting type or command")
        continue

    print(markdown)