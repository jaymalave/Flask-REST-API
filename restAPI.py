from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

class Hello(Resource):
    def get(self):
        return jsonify({'message':'this is your stock market polygon api'})
    

api.add_resource(Hello, '/')

if __name__ == '__main__':
    app.run(debug = True)