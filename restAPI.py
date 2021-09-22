from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import config 
import json
import requests
import sqlite3


app = Flask(__name__)
api = Api(app)
CORS(app)
key = config.API_KEY


class Hello(Resource):
    def get(self):
        return jsonify({'message':'this is your books api'})

#using google api to retrieve the books data
class SearchByISBN(Resource):
    def get(self, isbn):
      apiUrl = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
      isbn = isbn
      response = requests.get(apiUrl + isbn)
      return jsonify(response.json())


#search books by a particular author
class SearchByAuthor(Resource):
      def get(self, author):
          author = author
          apiUrl = "https://www.googleapis.com/books/v1/volumes?q={author}"
          response = requests.get(apiUrl)
          return jsonify(response.json())

#search books by name
class SearchByName(Resource):
      def get(self, name):
          name = name
          apiUrl = "https://www.googleapis.com/books/v1/volumes?q={name}"
          response = requests.get(apiUrl)
          return jsonify(response.json())

#to retrieve all the user's shelves 
class BookShelves(Resource):
    def get(self, uid):
        uid = uid 
        apiUrl = "https://www.googleapis.com/books/v1/users/${uid}/bookshelves"
        response = requests.get(apiUrl)
        return jsonify(response.json())

#to retrieve a particular shelf
class BookShelf(Resource):
    def get(self, uid, shelf):
        uid = uid
        shelf = shelf
        apiUrl = "https://www.googleapis.com/books/v1/users/${uid}/bookshelves/${shelf}"
        response = requests.get(apiUrl)
        return jsonify(response.json())

class MyShelf(Resource):
   def get(self):
       bookList = []
       conn = sqlite3.connect('books.db')
       cursor = conn.cursor()
       for row in cursor.execute('SELECT * FROM Books;'):
           bookList.append({"book_id": row[0], "name": row[1], "author": row[2]})
       return jsonify(bookList)


parser = reqparse.RequestParser()
parser.add_argument('name', type=str)
parser.add_argument('author', type=str)

class AddToShelf(Resource):
    # def get(self, author, book):
    #     author = author
    #     book = book
    #     conn = sqlite3.connect('books.db')
    #     cursor = conn.cursor()
    #     cursor.execute('INSERT INTO BOOKS(name, author) VALUES(?, ?)', (book, author))
    #     conn.commit()
    #     return jsonify({"message": "done"}, 200)
    def post(self):
        args = parser.parse_args()
        name = str(args['name'])
        author = str(args['author'])
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO BOOKS(name, author) VALUES(?, ?)', (name, author))
        conn.commit()
        return jsonify({"message": "done"}, 200)

class DeleteFromShelf(Resource):
      def delete(self, id):
        conn = sqlite3.connect('books.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BOOKS WHERE BookId=?', (id,))
        conn.commit()
        return jsonify({"message": "deleted the book"}, 200)




        

api.add_resource(Hello, '/')
api.add_resource(SearchByISBN, '/search-by-isbn/<string:isbn>')
api.add_resource(BookShelves, '/<int:uid>/bookshelves')
api.add_resource(BookShelf, '/<int:uid>/bookshelf/<int:shelf>')
api.add_resource(SearchByAuthor, '/search-by-author/<string:author>')
api.add_resource(SearchByName, '/search-by-name/<string:name>')
api.add_resource(MyShelf, '/myshelf')
api.add_resource(AddToShelf, '/add-book')
api.add_resource(DeleteFromShelf, '/delete-book/<int:id>')





if __name__ == '__main__':
    app.run(debug = True)