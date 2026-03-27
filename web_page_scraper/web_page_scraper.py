import requests
from bs4 import BeautifulSoup
import string
import os


# -------------------- ЕТАП 1 --------------------
def get_quote():
    url = input("Input the URL:\n")

    try:
        response = requests.get(url)

        if response.status_code != 200:
            print("Invalid quote resource!")
            return

        data = response.json()

        if "content" in data:
            print(data["content"])
        else:
            print("Invalid quote resource!")

    except:
        print("Invalid quote resource!")


# -------------------- ЕТАП 2 --------------------
def get_movie_info():
    url = input("Input the URL:\n")

    headers = {'Accept-Language': 'en-US,en;q=0.5'}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200 or "title" not in url:
            print("Invalid movie page!")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        description_tag = soup.find('meta', {'name': 'description'})

        if not title_tag or not description_tag:
            print("Invalid movie page!")
            return

        title = title_tag.text.split(" - IMDb")[0]
        description = description_tag['content']

        print({
            "title": title,
            "description": description
        })

    except:
        print("Invalid movie page!")


# -------------------- ЕТАП 3 --------------------
def save_page():
    url = input("Input the URL:\n")

    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open("source.html", "wb") as file:
                file.write(response.content)
            print("Content saved.")
        else:
            print(f"The URL returned {response.status_code}!")

    except:
        print("The URL returned error!")


# -------------------- ЕТАП 4 --------------------
def parse_news_once():
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2022&page=3"
    headers = {'Accept-Language': 'en-US,en;q=0.5'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('article')
    saved_articles = []

    for article in articles:
        type_tag = article.find('span', {'data-test': 'article.type'})

        if type_tag and type_tag.text == "News":
            title_tag = article.find('a', {'data-track-action': 'view article'})
            title = title_tag.text.strip()

            link = "https://www.nature.com" + title_tag['href']

            article_page = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_page.text, 'html.parser')

            body = article_soup.find('div', {'class': lambda x: x and "body" in x})

            if body:
                text = body.text.strip()

                translator = str.maketrans('', '', string.punctuation)
                filename = title.translate(translator).replace(" ", "_") + ".txt"

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)

                saved_articles.append(filename)

    print("Saved articles:", saved_articles)


# -------------------- ЕТАП 5 --------------------
def parse_multiple_pages():
    pages = int(input())
    article_type = input()

    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    base_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2022&page="

    for page in range(1, pages + 1):
        url = base_url + str(page)

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        os.makedirs(f"Page_{page}", exist_ok=True)

        articles = soup.find_all('article')

        for article in articles:
            type_tag = article.find('span', {'data-test': 'article.type'})

            if type_tag and type_tag.text == article_type:
                title_tag = article.find('a', {'data-track-action': 'view article'})
                title = title_tag.text.strip()

                link = "https://www.nature.com" + title_tag['href']

                article_page = requests.get(link, headers=headers)
                article_soup = BeautifulSoup(article_page.text, 'html.parser')

                body = article_soup.find('div', {'class': lambda x: x and "body" in x})

                if body:
                    text = body.text.strip()

                    translator = str.maketrans('', '', string.punctuation)
                    filename = title.translate(translator).replace(" ", "_") + ".txt"

                    filepath = os.path.join(f"Page_{page}", filename)

                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(text)

    print("Saved all articles.")


# -------------------- МЕНЮ --------------------
def main():
    print("Choose stage:")
    print("1 - Quote parser")
    print("2 - IMDb parser")
    print("3 - Save HTML")
    print("4 - Parse Nature News (1 page)")
    print("5 - Parse multiple pages")

    choice = input()

    if choice == "1":
        get_quote()
    elif choice == "2":
        get_movie_info()
    elif choice == "3":
        save_page()
    elif choice == "4":
        parse_news_once()
    elif choice == "5":
        parse_multiple_pages()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()