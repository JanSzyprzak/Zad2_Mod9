from flask import Flask, request, render_template, redirect, url_for, jsonify, abort, make_response

from forms import BookForm
from models import books

app = Flask(__name__)
app.config["SECRET_KEY"] = "bardzo_sekretny_klucz"

@app.route("/books/", methods=["GET", "POST"])
def books_list():
    form = BookForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            books.create(form.data)
            books.save_all()
        return redirect(url_for("books_list"))
    return render_template("books.html", form=form, books=books.all(), error=error)


@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = books.get(book_id - 1)
    form = BookForm(data=book)

    if request.method == "POST":
        if form.validate_on_submit():
            books.update(book_id - 1, form.data)
        return redirect(url_for("books_list"))
    return render_template("book.html", form=form, book_id=book_id)

@app.route("/authors/", methods=["GET"])
def get_authors():
    data = books.all()
    authors_list = [data[i]['author'] for i in range(len(data))]
    return render_template("authors.html", authors_list = sorted(authors_list))

@app.route("/number_of_pages/", methods=["GET"])
def get_number_of_pages():
    data = books.all()
    authors_list = [data[i]['author'] for i in range(len(data))]
    return render_template("authors.html", authors_list = sorted(authors_list))

@app.route("/api/books/", methods=["GET"])
def books_in_json():
    return jsonify(books.all())

@app.route("/api/books/<int:book_id>/", methods=["GET", "POST"])
def book_in_json(book_id):
    book = books.get(book_id - 1)
    if not book:
        abort(404)
    return jsonify({'book':book})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/books/", methods=["POST"])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        abort(400)
    book = {
        'title': request.json['title'],
        'author': request.json['author'],
        'description': request.json.get('description', ""),
        'number_of_pages': request.json.get('number_of_pages', ""),
        'done': False
    }
    books.api_create(book)
    return jsonify({'book': book}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/books/<int:book_id>", methods=['DELETE'])
def delete_book(book_id):
    result = books.delete(book_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

"""
Nie mogę dojść, gdzie jest błąd przy metodzie PUT (pod komentarzem). Robię testy wykonując poniższy request:

PUT http://127.0.0.1:5000/api/books/2

{
    "title": "Poćwicz",
    "author": "Poćwiczy",
    "description": "Poćwiczym",
    "number_of_pages": 100,
    "read": true,
}

Całość wywala się już tutaj:
if not request.json:
        abort(400)

"""


@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = books.get(book_id-1)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    print("tego mi już nie drukuje")
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'number_of_pages' in data and not isinstance(data.get('number_of_pages'), int),
        'read' in data and not isinstance(data.get('read'), bool)
    ]):
        abort(400)
    print("a tego to już w ogóle")  
    book = {
        'title': data.get('title', book['title']),
        'author': data.get('author', book['author']),
        'description': data.get('description', book['description']),
        'number_of_pages': data.get('number_of_pages', book['number_of_pages']),
        'read': data.get('read', book['read'])
    }
    books.update(book_id, book)
    return jsonify({'book': book})

@app.route("/api/books/by_author", methods=["GET"])
def books_by_author():
    data = books.all()
    data = sorted(data, key=lambda x: x['author'])
    return jsonify({'books sorted by author': data})

@app.route("/api/books/by_title", methods=["GET"])
def books_by_title():
    data = books.all()
    data = sorted(data, key=lambda x: x['title'])
    return jsonify({'books sorted by title': data})






if __name__ == "__main__":
    app.run(debug=True)