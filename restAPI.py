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


    
    

api.add_resource(Hello, '/')
api.add_resource(SearchBook, '/search/<string:isbn>')

if __name__ == '__main__':
    app.run(debug = True)