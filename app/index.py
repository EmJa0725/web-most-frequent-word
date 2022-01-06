from flask import Flask, request, jsonify
from views import parse_url, create_dictionary
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Bienvenido a la api"

@app.route('/frequent_word', methods=['POST'])
def frequent_word_ul():
    if request.method == 'POST':  
        body = request.get_json() 
        text = parse_url(body['url'])
        top_words = create_dictionary(text, body['top'])  
    
    return jsonify({
            "data": top_words,
        }), 201