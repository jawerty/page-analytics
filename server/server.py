from flask import Flask, request, jsonify
from sqlORM import sqlORM

server = Flask(__name__)
ORM = sqlORM(db='pageAnalytics')
@server.route('/video', methods=["POST"])
def video():

    content = request.json
    parent = content['parentRecommended'] if 'parentRecommended' in list(content.keys()) else None
    rowData = tuple(
                    content['videoURL'],
                    content['videoID'],
                    ','.join(content['keywords']),
                    content['experimentSource'],
                    content['recommededVideo'],
                    parent,
                    content['videoViews']
                    )
    try:
        ORM.insertVideo(data=rowData)
        ORM.insertKeywords(data=content['keywords'])
        result = True
    except:
        result = False

    return jsonify({'result': result}) 

@server.route('/q', methods=["POST"])
def q():

    content = request.json
    rowData = tuple(
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