from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import config 
import json
import requests


app = Flask(__name__)

api = Api(app)
key = config.API_KEY
class Hello(Resource):
    def get(self):
        return jsonify({'message':'this is your books api'})

#using google api to retrieve the books data
class SearchBook(Resource):
    def get(self, isbn):
      apiUrl = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
      isbn = isbn
      response = requests.get(apiUrl + isbn)
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


api.add_resource(Hello, '/')
api.add_resource(SearchBook, '/search/<string:isbn>')
api.add_resource(BookShelves, '/<int:uid>/bookshelves')
api.add_resource(BookShelf, '/<int:uid>/bookshelf/<int:shelf>')

if __name__ == '__main__':
    app.run(debug = True)