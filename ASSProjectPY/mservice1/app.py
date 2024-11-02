import sqlite3
import pika
from flask import Flask, g, request, render_template, redirect, url_for, jsonify
import requests

app = Flask(__name__)
DATABASE_PATH = 'service1.db'


def get_database_connection():
    database_connection = getattr(g, '_database', None)
    if database_connection is None:
        database_connection = g._database = sqlite3.connect(DATABASE_PATH)
    return database_connection

@app.teardown_appcontext
def close_database_connection(exception):
    database_connection = getattr(g, '_database', None)
    if database_connection is not None:
        database_connection.close()
     
@app.route('/')
def home_page():
    database_connection = get_database_connection()
    cursor = database_connection.execute('SELECT * FROM books')
    books_list = cursor.fetchall()
    return render_template('index.html', books=books_list)

def publish_message(message_content):
    rabbitmq_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue='book_events')
    channel.basic_publish(exchange='', routing_key='book_events', body=message_content)
    rabbitmq_connection.close()
    
@app.route('/add', methods=['POST'])
def add_new_book():
    if request.is_json:
        book_data = request.get_json()
    else:
        book_data = request.form

    book_title = book_data['title']
    book_author = book_data['author']
    user_name = book_data.get('username', 'unknown')

    database_connection = get_database_connection()
    cursor = database_connection.execute('INSERT INTO books (title, author) VALUES (?, ?)', (book_title, book_author))
    database_connection.commit()
    new_book_id = cursor.lastrowid

    publish_message(f'New book added by {user_name}')

    return jsonify({"status": "Book added!", "title": book_title, "author": book_author, "id": new_book_id}), 201

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_existing_book(book_id):
    database_connection = get_database_connection()
    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        database_connection.execute('UPDATE books SET title = ?, author = ? WHERE id = ?', (book_title, book_author, book_id))
        database_connection.commit()
        publish_message(f'Book edited: {book_title} by {book_author}')
        return redirect(url_for('home_page'))
    else:
        cursor = database_connection.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book_details = cursor.fetchone()
        return render_template('edit.html', book=book_details)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book_record(book_id):
    database_connection = get_database_connection()
    database_connection.execute('DELETE FROM books WHERE id = ?', (book_id,))
    database_connection.commit()
    return jsonify({"status": "Book deleted!"}), 200

@app.route('/books')
def list_books():
    database_connection = get_database_connection()
    cursor = database_connection.execute('SELECT * FROM books')
    books_data = cursor.fetchall()
    return jsonify({"books": books_data})

if __name__ == '__main__':
    with app.app_context():
        database_connection = get_database_connection()
        database_connection.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)')
        database_connection.commit()
    app.run(debug=True, host='0.0.0.0', port=5000)
