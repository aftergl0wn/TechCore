class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author


if __name__ == "__main__":
    book = Book("world", "Nik")
    print(book)
