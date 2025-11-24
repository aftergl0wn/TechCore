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


class Ebook(Book):
    def __init__(self, title, author, file_size):
        super().__init__(title, author)
        self.file_size = file_size

    def __repr__(self):
        return (
            f"Book(author={self.author}, "
            f"title={self.title}, "
            f"file_size={self.file_size})"
        )


if __name__ == "__main__":
    book = Ebook("world", "Nik1", 50)
    book2 = Book("home", "Tom")
    print(book)
    print(book2)
