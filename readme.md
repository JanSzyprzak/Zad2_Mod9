
Library

1. What is this?
Simple app to store book info including Title, Author, Description, Number of Pages and Read status.

2. How to use it?
Enter /books/ to see list of books (of course empty in the beginning) and form allowing to add new title. To modify item click on title link. You can access books also by entering books/id.

3. Making api requests.
Following requests are available:
GET    api/books/          - pobranie listy książek
POST   api/books/          - dodanie nowej książki
GET    api/books/<id>      - pobranie szczegółów książki dla danego id
DELETE api/books/<id>      - usunięcie książki
PUT    api/books/<id>      - update wybranej książki 

