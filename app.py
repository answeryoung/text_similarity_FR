#! /usr/bin/env python

from flask import Flask, render_template, request, redirect
from text_similarity_utils import spliting_text, topic_matcher, join_sentence
from sequence_referee import sequence_referee


def text_similarity(texts: dict) -> dict:
    r"""
    Function text_similarity(texts) is the driver code.
    Texts are passed in this function as a dict() in the form
    of {"a": str, "b": str}.
    
    1. Each text is split into List[List[str]] where the strings are words,
        and List[str] are sentences
    
    2. For each pair of sentenses, a score is calculated.
    
    3. The average score is then reported.
    
    4. If the number of sentenses are different or the average score is small,
        we look for common words that are not in the stopwords list and we 
        order the list of common words in the order of their descending
        frequency.
    
    5. The texts, splited into senences (List[str]), along with the score and
        common words (topics) are passed out in a dict().
    
    Output schema:
        { "a": List[str], "b": List[str], "score": str, "topics": List[str] }
    """
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
