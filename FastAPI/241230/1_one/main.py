from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books")
def read_books():
    url = "https://paullab.co.kr/bookservice/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    class Book:
        def __init__(self, name, cover, author, price):
            self.name = name
            self.cover = cover
            self.author = author
            self.price = price

        def __repr__(self):
            return f"{self.name}"

        def __str__(self):
            return f"{self.name}"

        def to_html(self):
            return f'<h2>{self.name}</h2>\n<img src="{self.cover}">\n<p>{self.author}</p>\n<p>{self.price_comma()}</p>\n'

        def price_comma(self):
            return format(self.price, ",")

    data = []

    for name, cover, price, author in zip(
        soup.select(".book_name"),
        soup.select(".book_cover"),
        soup.select(".book_info")[::3],
        soup.select(".book_info")[1::3],
    ):
        if (
            price.text.replace("가격: ", "").replace("원", "").replace(",", "")
            == "무료"
        ):
            price = 0
        else:
            price = int(
                price.text.replace("가격: ", "").replace("원", "").replace(",", "")
            )
        data.append(
            Book(
                name.text,
                f'https://paullab.co.kr/bookservice/{cover["src"]}',
                author.text.replace("저자: ", ""),
                price,
            )
        )
    return [{"책 이름": book.name} for book in data]
