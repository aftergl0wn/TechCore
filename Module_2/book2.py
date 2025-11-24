class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.author, self.title) == (other.author, other.title)
        return NotImplemented

    def __repr__(self):
        return f"Book(author={self.author}, title={self.title})"


if __name__ == "__main__":
    book1 = Book("world", "Nik")
    book2 = Book("world", "Nik")
    book3 = Book("home", "Tom")
    print(book1)
    print(book1 == book2)
    print(book1 == book3)
