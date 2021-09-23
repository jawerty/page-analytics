import sys
from flask import Flask, request, jsonify, render_template, send_from_directory
from mongoORM import MongoORM

server = Flask(__name__)
ORM = MongoORM(database='pageAnalytics')

@server.route('/dist/<path:path>')
def send_js(path):
    return send_from_directory('react/dist', path)

@server.route('/', methods=["GET"])
def homepage():
    return render_template('index.html')

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


if __name__ == '__main__':
    server.run(debug=True)