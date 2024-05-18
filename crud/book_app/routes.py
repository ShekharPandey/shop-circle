from flask import Blueprint, request, jsonify
from book_app.models import db, Books
from datetime import datetime

api = Blueprint("api", __name__)

# Validate book-title values before adding/updating operations
def validate_title(title_data):
    if not isinstance(title_data, str) or len(title_data)>20:
        return  "Title must be a string and it's length should be less than 20 characters."
    return None

# Validate book-author values before adding/updating operations
def validate_author(author_data):
    if not isinstance(author_data, str) or len(author_data)>20:
        return  "Author must be a string and it's length should be less than 20 characters."
    return None

# Validate book-ISBN values before adding operations
def validate_isbn(isbn_data):
    if not isinstance(isbn_data, int) or len(str(isbn_data)) != 13:
        return "ISBN must be 13--digit number."
    
    elif Books.query.filter_by(isbn=isbn_data).first():
        return "ISBN already exists."
    
    return None

# Validate book-date values before adding/updating operations
def validate_date(date_data):
    try:
        datetime.strptime(date_data, "%Y-%m-%d")
    except ValueError:
        return "Published Date must be in the format YYYY-MM-DD."
    
    return None


def validate_fields(data, update=False):
    errors={}


    if "title" in data and data["title"]:
        errors["title"] = validate_title(data.get("title"))
    else:
        errors["title"] = "Title is required"


    if "author" in data and data["author"]:
        errors["author"] = validate_author(data.get("author"))
    else:
        errors["author"] = "Author is required"

    if update is False:
        if "isbn" in data and data["isbn"]:
            errors["isbn"] = validate_isbn(data.get("isbn"))
        else:
            errors["isbn"] = "ISBN is required"

    
    if "published_date" in data and data["published_date"]:
        errors["published_date"] = validate_date(data.get("published_date"))
    else:
        errors["published_date"] = "Published Date is required"

    filtered = {k: v for k, v in errors.items() if v is not None}
    errors.clear()
    errors.update(filtered)
    return errors


# Add Books Endpoint
@api.route("/books", methods=["POST"])
def add_books():
    data = request.get_json()
    errors = validate_fields(data)

    if errors:
        return jsonify(errors), 400

    book_data = Books(
        title=data["title"],
        author=data["author"],
        isbn=data["isbn"],
        published_date=datetime.strptime(data["published_date"], "%Y-%m-%d")
    )
    
    db.session.add(book_data)
    db.session.commit()
    
    return jsonify({"message": "Book's created"}), 201

# Get all Books Endpoint
@api.route("/books", methods=["GET"])
def get_books():
    books_data = Books.query.all()
    books_list = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "published_date": book.published_date.strftime("%Y-%m-%d")
        }
        for book in books_data
    ]
    return jsonify(books_list), 200

# Get Book Endpoint
@api.route("/books/<int:isbn>", methods=["GET"])
def get_book(isbn):
    book = Books.query.filter_by(isbn=isbn).first()
    if book:
        return jsonify(
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "isbn": book.isbn,
                "published_date": book.published_date.strftime("%Y-%m-%d")
            }
        ), 200
    
    else:
        return jsonify({"error": "Book not found"}), 404

# Update Book Endpoint
@api.route("/books/<int:isbn>", methods=["PUT"])
def update_book(isbn):
    book = Books.query.filter_by(isbn=isbn).first()
    if book:
        data = request.get_json()

        errors = validate_fields(data, update=True)

        if errors:
            return jsonify(errors), 400
        
        
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.published_date = datetime.strptime(data["published_date"], "%Y-%m-%d")
        db.session.commit()
        return jsonify({"message": "Book updated"}), 200
    
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete Book Endpoint
@api.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    book = Books.query.filter_by(isbn=isbn).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book's deleted"}), 200
    
    else:
        return jsonify({"error": "Book not found"}), 404