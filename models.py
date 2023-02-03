import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        if id not in range(len(self.books)):   
            return []
        return self.books[id]

    def api_create(self, data):
        self.books.append(data)
        self.save_all()

    def create(self, data):
        data.pop('csrf_token')
        self.books.append(data)

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def update(self, id, data):
        if data.get('csrf_token'):
            data.pop('csrf_token')
        self.books[id] = data
        self.save_all()

    def api_update(self, id, data):
        book = self.get(id-1)
        if book:
            index = self.books.index(book)
            self.books[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        book = self.get(id-1)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False


books = Books()