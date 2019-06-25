from flask import Flask, request, render_template, jsonify

from io import BytesIO
import base64
import numpy as np
from PIL import Image

from nlp import wordcloud, clustering, topic_modeling, sentiment


app = Flask('flask_voicemagic')
app.config.from_pyfile('settings.py')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# report 작성되도록 수정 필요(post data로 audio file 전달)
@app.route('/report', methods=['POST'])
def report():
    return jsonify({
        'wordcloud': wordcloud()[0].tolist(),
        'clustering': clustering()[0].tolist(),
        'topic_modeling': topic_modeling()[0].tolist(),
        'sentiment': sentiment()[0].tolist(),
    })


# 현재 상태를 python pickle로 저장하도록 수정 필요
@app.route('/save', methods=['POST'])
def save():
    return jsonify({
        'wordcloud': wordcloud()[0].tolist(),
        'clustering': clustering()[0].tolist(),
        'topic_modeling': topic_modeling()[0].tolist(),
        'sentiment': sentiment()[0].tolist(),
    })


if __name__ == '__main__':
    app.run('0.0.0.0', 4000, debug=True)
