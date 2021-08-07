import sys
from flask import Flask, request, jsonify
from .sqlORM import sqlORM

server = Flask(__name__)
ORM = sqlORM(db='pageAnalytics')
@server.route('/video', methods=["POST"])
def video():
    content = request.json
    print(content)
    rowData = (
                    content['videoURL'],
                    content['videoID'],
                    ','.join(content['keywords']),
                    content['experimentSource'],
                    int(content['videoViews'])
                    )
    try:
        ORM.insertVideo(data=rowData)
        ORM.insertKeywords(data=content['keywords'])
        result = True
    except:
        print("Whew!", sys.exc_info(), "occurred.")

        result = False
    print(result)

    return jsonify({'result': result}) 

@server.route('/q', methods=["POST"])
def q():
    content = request.json
    rowData = (
                    content['query'],
                    content['experimentType'],
                    ','.join(content['resultKeywords'])
                    )
    try:
        ORM.insertSearch(data=rowData)
        result = True
    except:
        result = False
    
    return jsonify({'result': result})