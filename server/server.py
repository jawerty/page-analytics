import sys
from flask import Flask, request, jsonify
from mongoORM import MongoORM

server = Flask(__name__)
ORM = MongoORM(database='pageAnalytics')
@server.route('/video', methods=["POST"])
def video() -> jsonify:
    """endpoint to recieve video recommendation data and input into mongo db"""
    content = request.json
    data: list = content['data']
    try:
        ORM.setCollection('videoRecommendationData')
        ORM.insertMany(data)
        result: bool = True
    except:
        result: bool = False
    print(result)
    return jsonify({'result': result})

@server.route('/browserInteraction', methods=["POST"])
def browserInteraction() -> jsonify:
    """endpoint to recieve browser interaction data and input into mongo db"""
    content = request.json
    data: dict = content
    try:
        ORM.setCollection('browserInteractionData')
        ORM.insert(data)
        result: bool = True
    except:
        result: bool = False
    print(result)
    return jsonify({'result': result})

@server.route('/fetchData')
def fetchData() -> jsonify:
    # inplace for when front end graphs are needed
    pass


if __name__ == '__main__':
    server.run(debug=True)