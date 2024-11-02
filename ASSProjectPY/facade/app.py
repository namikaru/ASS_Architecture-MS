import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    response = requests.post('http://mservice2:5001/signup', json=data)
    return jsonify(response.json()), response.status_code

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    response = requests.post('http://mservice2:5001/login', json=data)
    return jsonify(response.json()), response.status_code

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        response = requests.get('http://mservice1:5000/books')
        return jsonify(response.json()), response.status_code
    elif request.method == 'POST':
        data = request.json
        user_info = {
            'title': data['title'],
            'author': data['author'],
            'username': data['username']
        }
        response = requests.post('http://mservice1:5000/add', json=user_info)
        return jsonify(response.json()), response.status_code
    
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://mservice1:5000/add', json=data, headers=headers)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
