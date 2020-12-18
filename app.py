from flask import Flask, render_template, request, redirect
from text_similarity_utils import spliting_text, topic_matcher, join_sentence
from sequence_referee import sequence_referee


def text_similarity(texts: dict) -> dict:
    a = spliting_text(texts["a"])
    b = spliting_text(texts["b"])
    
    texts["a"] = join_sentence(a)
    texts["b"] = join_sentence(b)
    texts["score"] = None
    texts["topics"] = None

    if len(a[0]) == 0 or len(b[0]) == 0:
        return texts
    
    score = 0
    if len(a) == len(b):
        # Assuming no linejunk
        linejunk = None
        for i in range(len(a)):
            cruncher = sequence_referee(linejunk, a[i], b[i])
            score += cruncher.score()
        score /= len(a)
        texts["score"] = "{:.4f}".format(score)
    
    if len(a) != len(b) or score < 0.2:
        topics_dict = topic_matcher(a, b)
        texts["topics"] = sorted(
            topics_dict.keys(), key=lambda item: item[1], reverse=True )
    
    return texts


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        texts = dict(request.form)
        texts = text_similarity(texts)
        if not texts["topics"]:
            return render_template("result_no_topic.html", result=texts)
        else:
            return render_template("result.html", result=texts)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
