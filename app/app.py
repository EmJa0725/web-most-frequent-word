from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import Counter

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
    
# Views
def parse_url(url):
    """Extract data from url and parse each word into a list"""  
    filtered_words = []
    symbols = "!@#$%^&*()_-+={[}]|\;:\"<>?/.,"
    
    source_text = requests.get(url).text
    soup = BeautifulSoup(source_text, 'html.parser')
    
    # get all content without html tags from page
    text_content = soup.find('body').text
    #print(text_content)
    # Break test into word and convert them into lower case
    words = text_content.lower().split()
    
    # Filter valid words removing numbers and special characters
    for word in words:
        for  symbol in symbols : 
            word = word.replace(symbol, '')
        if len(word) and not word.isnumeric():
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