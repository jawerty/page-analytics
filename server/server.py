import sys
from flask import Flask, request, jsonify
from mongoORM import MongoORM

server = Flask(__name__)
ORM = MongoORM(database='pageAnalytics', collection='videoRecommendationData')
@server.route('/video', methods=["POST"])
def video() -> jsonify:
    """function to recieve data and input into mongo db"""
    content = request.json
    data: list = content['data']
    try:
        ORM.insertMany(data)
        result: bool = True
    except:
        result: bool = False
    print(result)
    return jsonify({'result': result})


if __name__ == '__main__':
    server.run(debug=True)