from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from urllib.parse import unquote_plus
from qna import bert_question_answer

app = Flask(__name__)
CORS(app)


@app.route('/answer', methods=['POST'])
def answer_question():
    # Retrieve the question and corpus from the JSON request
    request_json = request.get_json()
    question = request_json['question']
    corpus_base64 = request_json['corpus']
    # Decode the corpus from base64
    corpus = base64.b64decode(corpus_base64).decode('utf-8')
    corpus = unquote_plus(unquote_plus(corpus))

    # Call the function to perform BERT question answering
    answer = bert_question_answer(question, corpus)
    print(question)
    print(corpus[:10])
    # Return the answer as a JSON response
    return {'answer': answer}

if __name__ == '__main__':
    app.run(debug=True)
