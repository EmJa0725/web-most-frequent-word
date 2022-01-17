from flask import Flask, request, jsonify
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup
from collections import Counter

app = Flask(__name__)

@app.route("/")
def hello_world():
    response = jsonify(message="Server is running")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/frequent_word', methods=['POST'])
@cross_origin()
def frequent_word_ul():
    if request.method == 'POST':  
        body = request.get_json() 
        text = parse_url(body['url'], body['ignored'])
        top_words = create_dictionary(text, body['top'])  
    
    return jsonify({
            "data": top_words,
        }), 201
    
# Views
def parse_url(url, ignored):
    """Extract data from url and parse each word into a list"""  
    filtered_words = []
    symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/.,"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
            'AppleWebKit/537.36 (KHTML, like Gecko) '\
            'Chrome/75.0.3770.80 Safari/537.36'}
    
    source_text = requests.get(url, headers=headers).content
    soup = BeautifulSoup(source_text, 'html.parser')
    
    # get all content without html tags from page
    text_content = soup.find('body').text
    # Break test into word and convert them into lower case
    words = text_content.lower().split()
    print(ignored)
    # Filter valid words removing numbers and special characters
    for word in words:
        for  symbol in symbols : 
            word = word.replace(symbol, '')
        if len(word) and not word.isnumeric() and word not in ignored:
            if word in ignored: continue
            filtered_words.append(word)
            
    return filtered_words


def create_dictionary(words_list, top):
    """Generate dictionary with counter of every word"""
    word_count = {}
    
    for word in words_list:
        word_count[word] = word_count[word] + 1 if word in word_count else 1

    c = Counter(word_count)
    top = c.most_common(top)
    # Convert tuple to json 
    return [{'word': key, 'count': value} for key,value in top]
