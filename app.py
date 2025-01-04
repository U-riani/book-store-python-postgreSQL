import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config

app = Flask(__name__)
CORS(app)

# Load configuration
app.config.from_object(Config)

def get_db_connection():
    db_config = app.config['DATABASE']
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM books;")
        books = cur.fetchall()
        books_data = [
            {"id": book[0], "title": book[1], "author": book[2], "pages_num": book[3], "review": book[4]}
            for book in books
        ]
        return jsonify(books_data)
    except psycopg2.Error as e:
        print(f"Error querying the database: {e}")
        return jsonify({"error": "Error fetching data from database"}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/create/', methods=['POST'])
def create():
    title = request.json.get('title')
    author = request.json.get('author')
    pages_num = request.json.get('pages_num', type=int)
    review = request.json.get('review')

    if not title or not author or not pages_num or not review:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()

    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()

    try:
        insert_script = '''INSERT INTO books (title, author, pages_num, review) VALUES (%s, %s, %s, %s);'''
        insert_value = (title, author, pages_num, review)
        cur.execute(insert_script, insert_value)
        conn.commit()
        return jsonify({"message": "Book created successfully"}), 201
    except psycopg2.Error as e:
        print(f"Error inserting into database: {e}")
        return jsonify({"error": "Error inserting data into database"}), 500
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
