from flask import Flask
from flask_restful import Api, Resource
from settings import *
from model import *
from random import randint



app = Flask(__name__)
app.config['SECRET_KEY'] = 23 * randint(0, 1000000000000000000)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

api = Api(app)
db.init_app(app)


class Quote(Resource):

    def get(self):

        return "200"

api.add_resource(Quote, '/api/quote/')



if __name__ == "__main__":
    app.run(debug=True)
